#![no_std]
//! Contrato de ejemplo para HU-01. No es el contrato de génesis: solo exige la firma de una
//! clave de rol y deja constancia de la huella que esa clave autorizó.
use soroban_sdk::{contract, contractevent, contractimpl, Address, BytesN, Env};

#[contractevent]
pub struct Registrado {
    #[topic]
    pub rol: Address,
    pub huella: BytesN<32>,
}

#[contract]
pub struct Ejemplo;

#[contractimpl]
impl Ejemplo {
    /// La clave de rol autoriza el registro de una huella. Quien transmite y paga la
    /// comisión puede ser cualquier otra cuenta.
    pub fn registrar(env: Env, rol: Address, huella: BytesN<32>) {
        rol.require_auth();
        Registrado { rol, huella }.publish(&env);
    }
}

#[cfg(test)]
mod test {
    use super::*;
    use soroban_sdk::{testutils::Address as _, Env};

    #[test]
    fn registrar_exige_la_firma_del_rol() {
        let env = Env::default();
        let id = env.register(Ejemplo, ());
        let cliente = EjemploClient::new(&env, &id);
        let rol = Address::generate(&env);
        let huella = BytesN::from_array(&env, &[7; 32]);
        assert!(cliente.try_registrar(&rol, &huella).is_err());
        env.mock_all_auths();
        cliente.registrar(&rol, &huella);
    }
}
