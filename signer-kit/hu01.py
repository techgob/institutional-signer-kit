"""HU-01: una clave de rol sin XLM autoriza una invocación y otra cuenta paga y transmite.

Demuestra en testnet los tres criterios de aceptación:
  CA-01-1  el operador transmite la entrada A firmada por el rol y paga la comisión
  CA-01-2  un tercero transmite la entrada B, firmada por el rol para la misma invocación y
           publicada como XDR
  CA-01-3  reenviar la entrada A ya usada es rechazado por la red (nonce consumido)

Las claves se leen de la CLI de Stellar (`stellar keys show`), nunca del repositorio.
Uso: python signer-kit/hu01.py <contract_id>
"""
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

from stellar_sdk import Keypair, Network, SorobanServer, TransactionBuilder, scval, xdr
from stellar_sdk.auth import authorize_entry
from stellar_sdk.exceptions import PrepareTransactionException

RPC = "https://soroban-testnet.stellar.org"
PASSPHRASE = Network.TESTNET_NETWORK_PASSPHRASE
EXPLORER = "https://stellar.expert/explorer/testnet/tx/"
HORIZON = "https://horizon-testnet.stellar.org/accounts/"
# Vigencia de la firma del rol, en ledgers (~5 s cada uno): unos 25 minutos.
VIGENCIA_LEDGERS = 300
SALIDA = Path(__file__).resolve().parent / "salida"


def clave(alias: str) -> Keypair:
    secreto = subprocess.run(["stellar", "keys", "show", alias], capture_output=True, text=True, check=True)
    return Keypair.from_secret(secreto.stdout.strip())


def existe_en_la_red(cuenta: str) -> bool:
    import urllib.request
    try:
        urllib.request.urlopen(HORIZON + cuenta, timeout=20)
        return True
    except Exception:
        return False


def saldo_xlm(cuenta: str) -> str | None:
    import urllib.request
    try:
        datos = json.load(urllib.request.urlopen(HORIZON + cuenta, timeout=20))
    except Exception:
        return None
    return next(b["balance"] for b in datos["balances"] if b["asset_type"] == "native")


def crear_rol_patrocinado(server, operador: Keypair, rol: Keypair):
    """Una cuenta clásica tiene que existir en la red para autorizar. El operador la crea con
    saldo 0 y patrocina su reserva mínima, así el rol nunca recibe ni guarda XLM."""
    cuenta = server.load_account(operador.public_key)
    tx = (
        TransactionBuilder(cuenta, PASSPHRASE, base_fee=100)
        .append_begin_sponsoring_future_reserves_op(sponsored_id=rol.public_key)
        .append_create_account_op(destination=rol.public_key, starting_balance="0")
        .append_end_sponsoring_future_reserves_op(source=rol.public_key)
        .set_timeout(120)
        .build()
    )
    tx.sign(operador)
    tx.sign(rol)
    return esperar(server, server.send_transaction(tx).hash)


def invocacion(server, fuente: Keypair, contrato: str, rol: Keypair, huella: bytes):
    cuenta = server.load_account(fuente.public_key)
    return (
        TransactionBuilder(cuenta, PASSPHRASE, base_fee=100)
        .append_invoke_contract_function_op(
            contract_id=contrato,
            function_name="registrar",
            parameters=[scval.to_address(rol.public_key), scval.to_bytes(huella)],
        )
        .set_timeout(120)
        .build()
    )


def entrada_firmada(server, fuente: Keypair, contrato: str, rol: Keypair, huella: bytes):
    """Simula la invocación, toma la entrada de autorización que pide el rol y la firma."""
    sim = server.simulate_transaction(invocacion(server, fuente, contrato, rol, huella))
    if sim.error:
        raise RuntimeError(f"simulación fallida: {sim.error}")
    entradas = [xdr.SorobanAuthorizationEntry.from_xdr(e) for e in sim.results[0].auth]
    hasta = server.get_latest_ledger().sequence + VIGENCIA_LEDGERS
    return [authorize_entry(e, rol, hasta, PASSPHRASE) for e in entradas]


def transmitir(server, fuente: Keypair, contrato: str, rol: Keypair, huella: bytes, entradas):
    tx = invocacion(server, fuente, contrato, rol, huella)
    tx.transaction.operations[0].auth = entradas
    tx = server.prepare_transaction(tx)
    tx.sign(fuente)
    return tx, esperar(server, server.send_transaction(tx).hash)


def esperar(server, tx_hash: str):
    for _ in range(30):
        res = server.get_transaction(tx_hash)
        if res.status.value != "NOT_FOUND":
            return res
        time.sleep(2)
    raise TimeoutError(tx_hash)


def resumen(nombre: str, res, fuente: Keypair) -> dict:
    cobrado = xdr.TransactionResult.from_xdr(res.result_xdr).fee_charged.int64 if res.result_xdr else None
    fila = {
        "paso": nombre,
        "estado": res.status.value,
        "hash": res.transaction_hash,
        "enlace": EXPLORER + res.transaction_hash,
        "transmite_y_paga": fuente.public_key,
        "comision_stroops": cobrado,
        "ledger": res.ledger,
    }
    print(json.dumps(fila, ensure_ascii=False))
    return fila


def main(contrato: str) -> None:
    server = SorobanServer(RPC)
    rol, operador, tercero = clave("tg-rol"), clave("tg-operador"), clave("tg-tercero")
    corrida = str(time.time()).encode()
    # A y B autorizan la misma invocación (mismo contrato, función y argumentos); solo cambia el nonce.
    huella = hashlib.sha256(corrida).digest()
    filas = []

    # Paso 0: si la cuenta del rol no existe, el operador la crea con saldo 0 y reserva patrocinada.
    if not existe_en_la_red(rol.public_key):
        filas.append(resumen("Paso 0 operador crea el rol con saldo 0 (reserva patrocinada)",
                             crear_rol_patrocinado(server, operador, rol), operador))
    print(f"saldo XLM del rol: {saldo_xlm(rol.public_key)}")

    # CA-01-1: el rol firma A, el operador la transmite y paga.
    entradas_a = entrada_firmada(server, operador, contrato, rol, huella)
    tx_a, res_a = transmitir(server, operador, contrato, rol, huella, entradas_a)
    filas.append(resumen("CA-01-1 operador transmite A", res_a, operador))

    # CA-01-2: el rol firma B y la publica; el tercero la toma del archivo y la transmite.
    SALIDA.mkdir(exist_ok=True)
    publicada = SALIDA / "autorizacion_B.xdr"
    publicada.write_text("\n".join(e.to_xdr() for e in entrada_firmada(server, operador, contrato, rol, huella)))
    entradas_b = [xdr.SorobanAuthorizationEntry.from_xdr(l) for l in publicada.read_text().splitlines()]
    _, res_b = transmitir(server, tercero, contrato, rol, huella, entradas_b)
    filas.append(resumen("CA-01-2 tercero transmite B publicada", res_b, tercero))

    # CA-01-3: el tercero reenvía A. La simulación ya lo rechaza; para dejar la prueba en la red
    # se envía igual, con los recursos de la transacción A original.
    try:
        transmitir(server, tercero, contrato, rol, huella, entradas_a)
        raise SystemExit("ERROR: el reenvío de A no fue rechazado en simulación")
    except PrepareTransactionException as e:
        print(f"simulación del reenvío rechazada: {str(e)[:160]}")
    reenvio = invocacion(server, tercero, contrato, rol, huella)
    reenvio.transaction.operations[0].auth = entradas_a
    reenvio.transaction.soroban_data = tx_a.transaction.soroban_data
    reenvio.transaction.fee = tx_a.transaction.fee
    reenvio.sign(tercero)
    res_r = esperar(server, server.send_transaction(reenvio).hash)
    filas.append(resumen("CA-01-3 tercero reenvía A (debe fallar)", res_r, tercero))

    ok = res_a.status.value == "SUCCESS" and res_b.status.value == "SUCCESS" and res_r.status.value == "FAILED"
    (SALIDA / "evidencia.json").write_text(json.dumps({
        "contrato": contrato,
        "rol": rol.public_key,
        "rol_saldo_xlm_al_final": saldo_xlm(rol.public_key),
        "huella_invocada": huella.hex(),
        "operador": operador.public_key,
        "tercero": tercero.public_key,
        "transacciones": filas,
        "criterios_cumplidos": ok,
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print("CRITERIOS CUMPLIDOS" if ok else "CRITERIOS NO CUMPLIDOS")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main(sys.argv[1])
