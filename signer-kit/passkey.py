"""Rotación por ciclo con passkey: la identidad del rol se queda, la clave cambia.

El rol es una cuenta de contrato (contracts/cuenta-passkey) controlada por una passkey P-256 con
formato WebAuthn. Su dirección es la que queda en el registro; la passkey se reemplaza al cerrar el
ciclo. El operador transmite y paga todo; la cuenta del rol no tiene saldo ni reserva.

  P-0  el operador despliega la cuenta del rol con la passkey del ciclo 1
  P-1  la passkey del ciclo 1 autoriza un registro
  P-2  la passkey del ciclo 1 autoriza la rotación a la passkey del ciclo 2
  P-3  la passkey del ciclo 1 intenta otro registro y la red lo rechaza
  P-4  la passkey del ciclo 2 autoriza un registro con la misma dirección de rol

Las passkeys se simulan en software (mismo formato que entrega un autenticador WebAuthn) y se
guardan en signer-kit/salida, que no se versiona. Lo que se prueba es la parte en la red.
Uso: python signer-kit/passkey.py <contract_id_registro> <alias_operador>
"""
import base64
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.utils import decode_dss_signature
from stellar_sdk import SorobanServer, TransactionBuilder, scval, xdr
from stellar_sdk.auth import authorize_entry
from stellar_sdk.exceptions import PrepareTransactionException

from hu01 import PASSPHRASE, RPC, SALIDA, VIGENCIA_LEDGERS, clave, esperar, resumen

WASM = Path(__file__).resolve().parents[1] / "contracts/cuenta-passkey/target/wasm32v1-none/release/cuenta_passkey.wasm"
N_P256 = 0xFFFFFFFF00000000FFFFFFFFFFFFFFFFBCE6FAADA7179E84F3B9CAC2FC632551
RP_ID = "techgob.example"


def passkey(nombre: str) -> ec.EllipticCurvePrivateKey:
    ruta = SALIDA / "passkeys" / f"{nombre}.pem"
    if not ruta.exists():
        ruta.parent.mkdir(parents=True, exist_ok=True)
        k = ec.generate_private_key(ec.SECP256R1())
        ruta.write_bytes(k.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8,
                                         serialization.NoEncryption()))
    return serialization.load_pem_private_key(ruta.read_bytes(), None)


def publica(k) -> bytes:
    return k.public_key().public_bytes(serialization.Encoding.X962, serialization.PublicFormat.UncompressedPoint)


def firma_webauthn(k, carga: bytes) -> xdr.SCVal:
    """Lo que devolvería navigator.credentials.get() con la carga de Soroban como desafío."""
    datos_aut = hashlib.sha256(RP_ID.encode()).digest() + bytes([0x05]) + (1).to_bytes(4, "big")  # UP + UV
    desafio = base64.urlsafe_b64encode(carga).rstrip(b"=").decode()
    datos_cli = json.dumps({"type": "webauthn.get", "challenge": desafio, "origin": f"https://{RP_ID}",
                            "crossOrigin": False}, separators=(",", ":")).encode()
    r, s = decode_dss_signature(k.sign(datos_aut + hashlib.sha256(datos_cli).digest(), ec.ECDSA(hashes.SHA256())))
    s = min(s, N_P256 - s)  # Soroban exige la forma low-S
    return scval.to_struct({
        "datos_autenticador": scval.to_bytes(datos_aut),
        "datos_cliente": scval.to_bytes(datos_cli),
        "firma": scval.to_bytes(r.to_bytes(32, "big") + s.to_bytes(32, "big")),
    })


def firmar_entrada(entrada: xdr.SorobanAuthorizationEntry, k, hasta: int) -> xdr.SorobanAuthorizationEntry:
    """La passkey firma el hash de la preimagen de autorización, igual que una clave clásica."""
    return authorize_entry(entrada, lambda pre: firma_webauthn(k, hashlib.sha256(pre.to_xdr_bytes()).digest()),
                           hasta, PASSPHRASE)


def invocacion(server, operador, contrato: str, funcion: str, args):
    cuenta = server.load_account(operador.public_key)
    return (TransactionBuilder(cuenta, PASSPHRASE, base_fee=100)
            .append_invoke_contract_function_op(contract_id=contrato, function_name=funcion, parameters=args)
            .set_timeout(120).build())


def entrada_sin_firmar(server, operador, contrato, funcion, args):
    sim = server.simulate_transaction(invocacion(server, operador, contrato, funcion, args))
    if sim.error:
        raise RuntimeError(f"simulación fallida: {sim.error}")
    (e,) = [xdr.SorobanAuthorizationEntry.from_xdr(a) for a in sim.results[0].auth]
    return e


def transmitir(server, operador, contrato, funcion, args, entrada):
    tx = invocacion(server, operador, contrato, funcion, args)
    tx.transaction.operations[0].auth = [entrada]
    tx = server.prepare_transaction(tx)
    tx.sign(operador)
    return tx, esperar(server, server.send_transaction(tx).hash)


def desplegar(alias_operador: str, clave_publica: bytes) -> str:
    salida = subprocess.run(
        ["stellar", "contract", "deploy", "--wasm", str(WASM), "--source", alias_operador, "--network", "testnet",
         "--", "--clave", clave_publica.hex()],
        capture_output=True, text=True, encoding="utf-8", check=True)
    return salida.stdout.strip().splitlines()[-1]


def main(registro: str, alias_operador: str) -> None:
    server = SorobanServer(RPC)
    operador = clave(alias_operador)
    k1, k2 = passkey("ciclo-1"), passkey("ciclo-2")
    filas = []

    cuenta_rol = desplegar(alias_operador, publica(k1))
    print(f"P-0 cuenta del rol desplegada: {cuenta_rol}")
    rol = scval.to_address(cuenta_rol)

    def registrar(k, nombre):
        args = [rol, scval.to_bytes(hashlib.sha256(f"{nombre}{time.time()}".encode()).digest())]
        hasta = server.get_latest_ledger().sequence + VIGENCIA_LEDGERS
        e = firmar_entrada(entrada_sin_firmar(server, operador, registro, "registrar", args), k, hasta)
        _, res = transmitir(server, operador, registro, "registrar", args, e)
        filas.append(resumen(nombre, res, operador))
        return res

    r1 = registrar(k1, "P-1 la passkey del ciclo 1 autoriza un registro")

    args = [scval.to_bytes(publica(k2))]
    hasta = server.get_latest_ledger().sequence + VIGENCIA_LEDGERS
    e = firmar_entrada(entrada_sin_firmar(server, operador, cuenta_rol, "rotar", args), k1, hasta)
    _, r2 = transmitir(server, operador, cuenta_rol, "rotar", args, e)
    filas.append(resumen("P-2 la passkey del ciclo 1 autoriza la rotación al ciclo 2", r2, operador))

    # P-3: la simulación ya rechaza la passkey vieja. Para dejar el rechazo en la red se envía
    # con los recursos de la misma invocación firmada por la passkey nueva.
    args = [rol, scval.to_bytes(hashlib.sha256(f"P-3{time.time()}".encode()).digest())]
    hasta = server.get_latest_ledger().sequence + VIGENCIA_LEDGERS
    base = entrada_sin_firmar(server, operador, registro, "registrar", args)
    vieja = firmar_entrada(base, k1, hasta)
    try:
        transmitir(server, operador, registro, "registrar", args, vieja)
        raise SystemExit("ERROR: la passkey del ciclo 1 no fue rechazada en simulación")
    except PrepareTransactionException as ex:
        print(f"simulación con la passkey vieja rechazada: {str(ex)[:160]}")
    guia = invocacion(server, operador, registro, "registrar", args)
    guia.transaction.operations[0].auth = [firmar_entrada(base, k2, hasta)]
    guia = server.prepare_transaction(guia)
    tx = invocacion(server, operador, registro, "registrar", args)
    tx.transaction.operations[0].auth = [vieja]
    tx.transaction.soroban_data = guia.transaction.soroban_data
    tx.transaction.fee = guia.transaction.fee
    tx.sign(operador)
    r3 = esperar(server, server.send_transaction(tx).hash)
    filas.append(resumen("P-3 la passkey del ciclo 1 intenta registrar (debe fallar)", r3, operador))

    r4 = registrar(k2, "P-4 la passkey del ciclo 2 autoriza un registro con la misma dirección")

    ok = [r.status.value for r in (r1, r2, r3, r4)] == ["SUCCESS", "SUCCESS", "FAILED", "SUCCESS"]
    SALIDA.mkdir(exist_ok=True)
    (SALIDA / "passkey.json").write_text(json.dumps({
        "contrato_registro": registro,
        "cuenta_rol": cuenta_rol,
        "passkey_ciclo_1": publica(k1).hex(),
        "passkey_ciclo_2": publica(k2).hex(),
        "operador": operador.public_key,
        "transacciones": filas,
        "criterios_cumplidos": ok,
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print("ROTACIÓN VERIFICADA" if ok else "ROTACIÓN NO VERIFICADA")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main(*sys.argv[1:3])
