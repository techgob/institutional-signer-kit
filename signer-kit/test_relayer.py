"""Pruebas sin red de los rechazos del relayer (pieza 2), contra la interfaz de docs/pieza2-interfaz.md.

La solicitud es la invocación real de CA-01-1 guardada en verifier/datos_prueba/conforme.xdr. Las tres
pruebas de rechazo están marcadas como esperadas a fallar mientras signer-kit/relayer.py no exista;
cuando el relayer las haga pasar, unittest las reporta como "unexpected success" y hay que quitar la marca.
"""
import hashlib
import importlib
import json
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest import mock

from stellar_sdk import Network, TransactionBuilder, xdr
from stellar_sdk.address import Address

sys.path.insert(0, str(Path(__file__).resolve().parent))

DATOS = Path(__file__).resolve().parent.parent / "verifier" / "datos_prueba"
CONTRATO = "CDGCV3TDCJCKR3LO3V6ACWVC4PIHIKJJOF5COR5VJTO6RDLVZ4TSBL27"  # contrato de ejemplo invocado en CA-01-1
OTRO_CONTRATO = "CD7T3FZ4WBVNXTQKFDFEIZ5INVYNP6COK2J4VH47U6I6CHWU5X7NMGUY"  # cuenta-passkey, aquí solo como contrato distinto
ROL = "GA73IU5SLHFAV3MTNQKNXU5A65YCZMGC4ZWR7AR65VWP4QYTHXCT277V"
VENCE = 5026764  # ledger en que vence la firma de la entrada de CA-01-1
COMISION_ESTIMADA = 23824  # comisión máxima de la transacción preparada en CA-01-1
COMISION_COBRADA = 13677  # lo que cobró la red en CA-01-1
AHORA = datetime(2026, 11, 10, 15, 0, tzinfo=timezone.utc)


def solicitud_ca_01_1() -> dict:
    _, envelope = (DATOS / "conforme.xdr").read_text().split()
    operacion = TransactionBuilder.from_xdr(envelope, Network.TESTNET_NETWORK_PASSPHRASE).transaction.operations[0]
    return {"version": 1, "funcion_host": operacion.host_function.to_xdr(), "entradas": [e.to_xdr() for e in operacion.auth]}


def politica(permitidos: list, tope: int = 300000) -> dict:
    return {
        "version": 1,
        "red": "testnet",
        "periodo_segundos": 86400,
        "vigencia_maxima_ledgers": 720,
        "comision_maxima_stroops": 50000,
        "permitidos": permitidos,
        "roles": {ROL: {"tope_stroops": tope, "max_solicitudes": 20}},
    }


class SolicitudDePrueba(unittest.TestCase):
    """Sin marca: si esto falla, las pruebas de rechazo fallarían por un error propio y no por falta del relayer."""

    def test_la_solicitud_trae_contrato_funcion_y_entrada_firmada_por_el_rol(self):
        solicitud = solicitud_ca_01_1()
        invocacion = xdr.HostFunction.from_xdr(solicitud["funcion_host"]).invoke_contract
        self.assertEqual(Address.from_xdr_sc_address(invocacion.contract_address).address, CONTRATO)
        self.assertEqual(invocacion.function_name.sc_symbol, b"registrar")
        (entrada,) = [xdr.SorobanAuthorizationEntry.from_xdr(e) for e in solicitud["entradas"]]
        credenciales = entrada.credentials.address or entrada.credentials.address_v2
        self.assertEqual(Address.from_xdr_sc_address(credenciales.address).address, ROL)
        self.assertNotEqual(credenciales.signature.type, xdr.SCValType.SCV_VOID)
        self.assertEqual(credenciales.signature_expiration_ledger.uint32, VENCE)
        self.assertEqual(entrada.root_invocation.function.contract_fn, invocacion)


class Rechazos(unittest.TestCase):
    def setUp(self):
        self._carpeta = tempfile.TemporaryDirectory()
        self.registro = Path(self._carpeta.name)
        self.red = mock.Mock(spec=["ultimo_ledger", "estimar_comision", "transmitir"])
        self.red.ultimo_ledger.return_value = VENCE - 100
        self.red.estimar_comision.return_value = COMISION_ESTIMADA

    def tearDown(self):
        self._carpeta.cleanup()

    def procesar(self, pol: dict) -> dict:
        relayer = importlib.import_module("relayer")
        return relayer.Relayer(pol, self.registro, self.red, lambda: AHORA).procesar(solicitud_ca_01_1())

    def comprobar_rechazo(self, resultado: dict, codigo: str) -> dict:
        self.assertEqual(resultado["estado"], "rechazada")
        self.assertEqual(resultado["codigo"], codigo)
        self.red.transmitir.assert_not_called()
        self.assertEqual(list(self.registro.glob("publicadas/*")), [])
        (linea,) = [json.loads(l) for l in (self.registro / "rechazos.jsonl").read_text().splitlines()]
        self.assertEqual(linea["codigo"], codigo)
        self.assertEqual(linea["fecha"], "2026-11-10T15:00:00Z")
        self.assertEqual(linea["rol"], ROL)
        self.assertEqual(linea["contrato"], CONTRATO)
        self.assertEqual(linea["funcion"], "registrar")
        return linea

    @unittest.expectedFailure  # signer-kit/relayer.py todavía no existe
    def test_rechaza_contrato_no_permitido(self):
        resultado = self.procesar(politica([{"contrato": OTRO_CONTRATO, "funciones": ["registrar"]}]))
        linea = self.comprobar_rechazo(resultado, "CONTRATO_NO_PERMITIDO")
        self.assertEqual(linea["detalle"], {"contrato": CONTRATO})
        self.assertEqual(self.red.method_calls, [])  # se rechaza sin tocar la red

    @unittest.expectedFailure  # signer-kit/relayer.py todavía no existe
    def test_rechaza_funcion_no_permitida(self):
        resultado = self.procesar(politica([{"contrato": CONTRATO, "funciones": ["rotar"]}]))
        linea = self.comprobar_rechazo(resultado, "FUNCION_NO_PERMITIDA")
        self.assertEqual(linea["detalle"], {"contrato": CONTRATO, "funcion": "registrar", "permitidas": ["rotar"]})
        self.assertEqual(self.red.method_calls, [])  # se rechaza sin tocar la red

    @unittest.expectedFailure  # signer-kit/relayer.py todavía no existe
    def test_rechaza_invocacion_que_supera_el_tope_de_gasto(self):
        # Una transacción anterior del mismo rol, seis horas antes, dentro del período de 24 horas.
        anterior = json.dumps({
            "fecha": "2026-11-10T09:00:00Z", "rol": ROL, "contrato": CONTRATO, "funcion": "registrar",
            "solicitud_sha256": hashlib.sha256(b"solicitud anterior").hexdigest(),
            "entradas_sha256": [hashlib.sha256(b"entrada anterior").hexdigest()],
            "xdr_publicado": "publicadas/anterior.xdr", "comision_estimada_stroops": COMISION_ESTIMADA,
            "estado": "SUCCESS", "hash": "8ba160396082e0ac29dc0324e96a119a90f99c2e9fd9a10aa2941746c14e7e5f",
            "enlace": "https://stellar.expert/explorer/testnet/tx/8ba160396082e0ac29dc0324e96a119a90f99c2e9fd9a10aa2941746c14e7e5f",
            "transmite_y_paga": "GDDZ3HMMIJWNP3MCM7NXZ325NYYCSFWPQ6SZIHMUVHSF73CJHKEUUQKM",
            "comision_stroops": COMISION_COBRADA, "ledger": 5026465,
        }) + "\n"
        (self.registro / "comisiones.jsonl").write_text(anterior)

        # 13 677 consumidos + 23 824 estimados = 37 501, más que el tope de 30 000.
        resultado = self.procesar(politica([{"contrato": CONTRATO, "funciones": ["registrar"]}], tope=30000))
        linea = self.comprobar_rechazo(resultado, "TOPE_DE_GASTO")
        self.assertEqual(linea["detalle"], {
            "consumido_stroops": COMISION_COBRADA,
            "comision_estimada_stroops": COMISION_ESTIMADA,
            "tope_stroops": 30000,
            "periodo_segundos": 86400,
        })
        self.assertEqual((self.registro / "comisiones.jsonl").read_text(), anterior)  # el rechazo no suma consumo


if __name__ == "__main__":
    unittest.main()
