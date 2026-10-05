"""Conformidad de un operador: comprueba, sobre una transacción ya confirmada, las propiedades
que el kit promete. Lo puede correr cualquiera, sin claves y sin pedir permiso a TechGob.

  C1  la transacción se confirmó
  C2  la única firma de la transacción es la de la cuenta que la envió y pagó
  C3  el rol no es quien envía ni paga
  C4  el rol autorizó dentro de la llamada, con su propia firma en la entrada de autorización
  C5  esa autorización vence en un plazo acotado (máximo VIGENCIA_MAXIMA ledgers)
  C6  el rol no tiene XLM propio (cuenta clásica: saldo 0 y reserva patrocinada por otro;
      cuenta de contrato: saldo 0 en el contrato del XLM). C6 mira el estado actual del rol,
      no el del momento de la transacción.

Uso: python verifier/conformidad.py <hash> [<hash> ...]
"""
import json
import sys
import urllib.error
import urllib.request

from stellar_sdk import Asset, Keypair, Network, SorobanServer, TransactionBuilder, scval, xdr
from stellar_sdk.address import Address, AddressType
from stellar_sdk.exceptions import BadSignatureError

RPC = "https://soroban-testnet.stellar.org"
HORIZON = "https://horizon-testnet.stellar.org/accounts/"
PASSPHRASE = Network.TESTNET_NETWORK_PASSPHRASE
VIGENCIA_MAXIMA = 720  # unas 1 hora a ~5 s por ledger


def credenciales(entrada: xdr.SorobanAuthorizationEntry):
    c = entrada.credentials
    return c.address or c.address_v2 or (c.address_with_delegates and c.address_with_delegates.address_credentials)


def revisar_sobre(envelope_xdr: str, ledger: int) -> tuple[dict, str | None]:
    """C2 a C5, solo con el sobre de la transacción. Devuelve los resultados y la dirección del rol."""
    sobre = TransactionBuilder.from_xdr(envelope_xdr, PASSPHRASE)
    fuente = sobre.transaction.source.account_id
    firmas = sobre.signatures
    firma_de_fuente = len(firmas) == 1
    if firma_de_fuente:
        try:
            Keypair.from_public_key(fuente).verify(sobre.hash(), firmas[0].signature)
        except BadSignatureError:
            firma_de_fuente = False

    entradas = [credenciales(e) for e in getattr(sobre.transaction.operations[0], "auth", None) or []]
    entradas = [e for e in entradas if e is not None]
    rol = Address.from_xdr_sc_address(entradas[0].address).address if entradas else None
    firmada = bool(entradas) and entradas[0].signature.type != xdr.SCValType.SCV_VOID
    plazo = entradas[0].signature_expiration_ledger.uint32 - ledger if entradas else None
    return {
        "C2 única firma, de quien envía y paga": firma_de_fuente,
        "C3 el rol no envía ni paga": rol is not None and rol != fuente,
        "C4 el rol autorizó dentro de la llamada": firmada,
        f"C5 la autorización vence en {VIGENCIA_MAXIMA} ledgers o menos": plazo is not None and 0 < plazo <= VIGENCIA_MAXIMA,
    }, rol


def rol_sin_xlm(server: SorobanServer, rol: str, fuente: str) -> bool:
    if Address(rol).type == AddressType.ACCOUNT:
        try:
            cuenta = json.load(urllib.request.urlopen(HORIZON + rol, timeout=20))
        except urllib.error.HTTPError:
            return False
        saldo = next(b["balance"] for b in cuenta["balances"] if b["asset_type"] == "native")
        return float(saldo) == 0 and cuenta.get("sponsor") not in (None, rol)
    xlm = Asset.native().contract_id(PASSPHRASE)
    tx = (TransactionBuilder(server.load_account(fuente), PASSPHRASE, base_fee=100)
          .append_invoke_contract_function_op(xlm, "balance", [scval.to_address(rol)])
          .set_timeout(60).build())
    sim = server.simulate_transaction(tx)
    return sim.error is None and scval.from_int128(xdr.SCVal.from_xdr(sim.results[0].xdr)) == 0


def revisar(server: SorobanServer, tx_hash: str) -> dict:
    res = server.get_transaction(tx_hash)
    if res.status.value != "SUCCESS":
        return {"hash": tx_hash, "C1 confirmada": False, "conforme": False}
    checks, rol = revisar_sobre(res.envelope_xdr, res.ledger)
    fuente = TransactionBuilder.from_xdr(res.envelope_xdr, PASSPHRASE).transaction.source.account_id
    checks = {"C1 confirmada": True, **checks, "C6 el rol no tiene XLM propio": bool(rol) and rol_sin_xlm(server, rol, fuente)}
    return {"hash": tx_hash, "rol": rol, "envia_y_paga": fuente, **checks, "conforme": all(checks.values())}


if __name__ == "__main__":
    server = SorobanServer(RPC)
    informes = [revisar(server, h) for h in sys.argv[1:]]
    print(json.dumps(informes, ensure_ascii=False, indent=2))
    sys.exit(0 if informes and all(i["conforme"] for i in informes) else 1)
