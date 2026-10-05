#![no_std]
//! Cuenta de contrato para una clave de rol con passkey (WebAuthn, curva secp256r1).
//!
//! La dirección de la cuenta es la identidad del rol en el registro y no cambia. La clave
//! pública que la controla sí puede cambiar: `rotar` reemplaza la passkey del ciclo que termina
//! por la del ciclo que empieza, autorizado por la passkey vigente. Desde ese momento la passkey
//! anterior ya no autoriza nada.
use soroban_sdk::{
    auth::{Context, CustomAccountInterface},
    contract, contracterror, contractevent, contractimpl, contracttype,
    crypto::Hash,
    symbol_short, Bytes, BytesN, Env, Symbol, Vec,
};

const CLAVE: Symbol = symbol_short!("clave");

/// Lo que entrega un autenticador WebAuthn al firmar: datos del autenticador, el JSON del
/// cliente (que contiene el desafío) y la firma P-256 en forma compacta r || s.
#[contracttype]
pub struct FirmaWebAuthn {
    pub datos_autenticador: Bytes,
    pub datos_cliente: Bytes,
    pub firma: BytesN<64>,
}

#[contracterror]
#[derive(Copy, Clone, Debug, Eq, PartialEq)]
#[repr(u32)]
pub enum Error {
    DesafioNoCoincide = 1,
    UsuarioNoPresente = 2,
    DatosAutenticadorCortos = 3,
}

#[contractevent]
pub struct ClaveRotada {
    pub nueva: BytesN<65>,
}

#[contract]
pub struct CuentaPasskey;

#[contractimpl]
impl CuentaPasskey {
    pub fn __constructor(env: Env, clave: BytesN<65>) {
        env.storage().instance().set(&CLAVE, &clave);
    }

    /// Cambia la passkey que controla la cuenta. Solo la passkey vigente puede autorizarlo.
    pub fn rotar(env: Env, nueva: BytesN<65>) {
        env.current_contract_address().require_auth();
        env.storage().instance().set(&CLAVE, &nueva);
        ClaveRotada { nueva }.publish(&env);
    }

    pub fn clave(env: Env) -> BytesN<65> {
        env.storage().instance().get(&CLAVE).unwrap()
    }
}

#[contractimpl]
impl CustomAccountInterface for CuentaPasskey {
    type Signature = FirmaWebAuthn;
    type Error = Error;

    fn __check_auth(env: Env, carga: Hash<32>, f: FirmaWebAuthn, _ctx: Vec<Context>) -> Result<(), Error> {
        // Byte 32 de los datos del autenticador: bandera UP (el usuario estuvo presente).
        if f.datos_autenticador.len() < 37 {
            return Err(Error::DatosAutenticadorCortos);
        }
        if f.datos_autenticador.get_unchecked(32) & 0x01 == 0 {
            return Err(Error::UsuarioNoPresente);
        }
        // El desafío firmado tiene que ser exactamente la carga de esta autorización.
        if !contiene_desafio(&f.datos_cliente, &carga.to_array()) {
            return Err(Error::DesafioNoCoincide);
        }
        // WebAuthn firma sha256(datos_autenticador || sha256(datos_cliente)).
        let mut mensaje = f.datos_autenticador.clone();
        mensaje.append(&env.crypto().sha256(&f.datos_cliente).into());
        let resumen = env.crypto().sha256(&mensaje);
        let clave: BytesN<65> = env.storage().instance().get(&CLAVE).unwrap();
        env.crypto().secp256r1_verify(&clave, &resumen, &f.firma);
        Ok(())
    }
}

/// Busca `"challenge":"<base64url de la carga>"` dentro del JSON del cliente.
fn contiene_desafio(json: &Bytes, carga: &[u8; 32]) -> bool {
    const ABC: &[u8; 64] = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_";
    const PREFIJO: &[u8] = b"\"challenge\":\"";
    let mut buscado = [0u8; 13 + 43 + 1];
    buscado[..13].copy_from_slice(PREFIJO);
    let (mut bits, mut n, mut k) = (0u32, 0u32, 13usize);
    for b in carga {
        bits = (bits << 8) | *b as u32;
        n += 8;
        while n >= 6 {
            n -= 6;
            buscado[k] = ABC[((bits >> n) & 63) as usize];
            k += 1;
        }
    }
    buscado[k] = ABC[((bits << (6 - n)) & 63) as usize];
    buscado[k + 1] = b'"';
    let largo = json.len() as usize;
    if largo < buscado.len() {
        return false;
    }
    'pos: for i in 0..=(largo - buscado.len()) {
        for (j, c) in buscado.iter().enumerate() {
            if json.get_unchecked((i + j) as u32) != *c {
                continue 'pos;
            }
        }
        return true;
    }
    false
}

#[cfg(test)]
mod test {
    use super::*;
    use soroban_sdk::Env;

    #[test]
    fn reconoce_el_desafio_en_base64url() {
        let env = Env::default();
        let carga = [0xfbu8; 32]; // fuerza los caracteres - y _ del alfabeto url
        let bien = Bytes::from_slice(&env, b"{\"type\":\"webauthn.get\",\"challenge\":\"-_v7-_v7-_v7-_v7-_v7-_v7-_v7-_v7-_v7-_v7-_s\",\"origin\":\"x\"}");
        let otra = Bytes::from_slice(&env, b"{\"challenge\":\"-_v7-_v7-_v7-_v7-_v7-_v7-_v7-_v7-_v7-_v7-_t\"}");
        assert!(contiene_desafio(&bien, &carga));
        assert!(!contiene_desafio(&otra, &carga));
    }

    #[test]
    fn rotar_cambia_la_clave_y_exige_la_autorizacion_de_la_cuenta() {
        let env = Env::default();
        let c1 = BytesN::from_array(&env, &[1u8; 65]);
        let c2 = BytesN::from_array(&env, &[2u8; 65]);
        let id = env.register(CuentaPasskey, (c1.clone(),));
        let cuenta = CuentaPasskeyClient::new(&env, &id);
        assert_eq!(cuenta.clave(), c1);
        assert!(cuenta.try_rotar(&c2).is_err()); // sin autorización de la propia cuenta
        env.mock_all_auths();
        cuenta.rotar(&c2);
        assert_eq!(env.auths()[0].0, id);
        assert_eq!(cuenta.clave(), c2);
    }
}
