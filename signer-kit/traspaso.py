"""Traspaso de operador: otra organización asume el pago sin tocar el contrato ni la clave del rol.

  T-1  el operador entrante transfiere a su nombre el patrocinio de la reserva de la cuenta del rol
       (operación RevokeSponsorship del operador saliente, dentro de BeginSponsoringFutureReserves
       del entrante; firman los dos)
  T-2  el rol firma una invocación y el operador entrante la transmite y paga

El operador saliente no aparece después de T-1. El contrato y la clave del rol son los mismos de HU-01.
Uso: python signer-kit/traspaso.py <contract_id> <alias_operador_saliente> <alias_operador_entrante>
"""
import hashlib
import json
import sys
import time
import urllib.request

from stellar_sdk import SorobanServer, TransactionBuilder

from hu01 import HORIZON, PASSPHRASE, RPC, SALIDA, clave, entrada_firmada, esperar, resumen, saldo_xlm, transmitir


def patrocinador(cuenta: str) -> str | None:
    return json.load(urllib.request.urlopen(HORIZON + cuenta, timeout=20)).get("sponsor")


def transferir_patrocinio(server, saliente, entrante, rol: str):
    cuenta = server.load_account(entrante.public_key)
    tx = (
        TransactionBuilder(cuenta, PASSPHRASE, base_fee=100)
        .append_begin_sponsoring_future_reserves_op(sponsored_id=saliente.public_key)
        .append_revoke_account_sponsorship_op(account_id=rol, source=saliente.public_key)
        .append_end_sponsoring_future_reserves_op(source=saliente.public_key)
        .set_timeout(120)
        .build()
    )
    tx.sign(entrante)
    tx.sign(saliente)
    return esperar(server, server.send_transaction(tx).hash)


def main(contrato: str, alias_saliente: str, alias_entrante: str) -> None:
    server = SorobanServer(RPC)
    rol, saliente, entrante = clave("tg-rol"), clave(alias_saliente), clave(alias_entrante)
    antes = patrocinador(rol.public_key)
    print(f"patrocinador de la reserva del rol antes: {antes}")
    filas = [resumen("T-1 el operador entrante asume el patrocinio de la reserva del rol",
                     transferir_patrocinio(server, saliente, entrante, rol.public_key), entrante)]
    despues = patrocinador(rol.public_key)
    print(f"patrocinador después: {despues}")

    huella = hashlib.sha256(str(time.time()).encode()).digest()
    entradas = entrada_firmada(server, entrante, contrato, rol, huella)
    _, res = transmitir(server, entrante, contrato, rol, huella, entradas)
    filas.append(resumen("T-2 el operador entrante transmite y paga una firma del rol", res, entrante))

    ok = (antes == saliente.public_key and despues == entrante.public_key
          and all(f["estado"] == "SUCCESS" for f in filas))
    SALIDA.mkdir(exist_ok=True)
    (SALIDA / "traspaso.json").write_text(json.dumps({
        "contrato": contrato,
        "rol": rol.public_key,
        "rol_saldo_xlm_al_final": saldo_xlm(rol.public_key),
        "operador_saliente": saliente.public_key,
        "operador_entrante": entrante.public_key,
        "patrocinador_antes": antes,
        "patrocinador_despues": despues,
        "huella_invocada": huella.hex(),
        "transacciones": filas,
        "criterios_cumplidos": ok,
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print("TRASPASO VERIFICADO" if ok else "TRASPASO NO VERIFICADO")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main(*sys.argv[1:4])
