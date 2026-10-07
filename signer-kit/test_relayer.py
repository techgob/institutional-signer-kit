"""Pruebas sin red del relayer (pieza 2), contra la interfaz de docs/pieza2-interfaz.md.

La solicitud es la invocación real de CA-01-1 guardada en verifier/datos_prueba/conforme.xdr. La red es
un doble: ninguna prueba transmite ni usa claves.
"""
import hashlib
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
from relayer import Relayer  # noqa: E402

DATOS = Path(__file__).resolve().parent.parent / "verifier" / "datos_prueba"
CONTRATO = "CDGCV3TDCJCKR3LO3V6ACWVC4PIHIKJJOF5COR5VJTO6RDLVZ4TSBL27"  # contrato de ejemplo invocado en CA-01-1
OTRO_CONTRATO = "CD7T3FZ4WBVNXTQKFDFEIZ5INVYNP6COK2J4VH47U6I6CHWU5X7NMGUY"  # cuenta-passkey, aquí solo como contrato distinto
ROL = "GA73IU5SLHFAV3MTNQKNXU5A65YCZMGC4ZWR7AR65VWP4QYTHXCT277V"
OTRO_ROL = "GAJOFFTN767ZGII3NT6YKBKWEIF3XIMGPSSORZK6HMKVZSEJ3XZ7DZUS"  # el tercero de HU-01, aquí solo como rol distinto
VENCE = 5026764  # ledger en que vence la firma de la entrada de CA-01-1
COMISION_ESTIMADA = 23824  # comisión máxima de la transacción preparada en CA-01-1
COMISION_COBRADA = 13677  # lo que cobró la red en CA-01-1
AHORA = datetime(2026, 11, 10, 15, 0, tzinfo=timezone.utc)
TRANSACCION_CA_01_1 = {  # evidence/hu01/evidencia.json, primera transacción
    "estado": "SUCCESS",
    "hash": "8ba160396082e0ac29dc0324e96a119a90f99c2e9fd9a10aa2941746c14e7e5f",
    "enlace": "https://stellar.expert/explorer/testnet/tx/8ba160396082e0ac29dc0324e96a119a90f99c2e9fd9a10aa2941746c14e7e5f",
    "transmite_y_paga": "GDDZ3HMMIJWNP3MCM7NXZ325NYYCSFWPQ6SZIHMUVHSF73CJHKEUUQKM",
    "comision_stroops": COMISION_COBRADA,
    "ledger": 5026465,
}


def solicitud_ca_01_1() -> dict:
    _, envelope = (DATOS / "conforme.xdr").read_text().split()
    operacion = TransactionBuilder.from_xdr(envelope, Network.TESTNET_NETWORK_PASSPHRASE).transaction.operations[0]
    return {"version": 1, "funcion_host": operacion.host_function.to_xdr(), "entradas": [e.to_xdr() for e in operacion.auth]}


def politica(permitidos: list, tope: int = 300000, max_solicitudes: int = 20, comision_maxima: int = 50000,
             rol: str = ROL) -> dict:
    return {
        "version": 1,
        "red": "testnet",
        "periodo_segundos": 86400,
        "vigencia_maxima_ledgers": 720,
        "comision_maxima_stroops": comision_maxima,
        "permitidos": permitidos,
        "roles": {rol: {"tope_stroops": tope, "max_solicitudes": max_solicitudes}},
    }


REGISTRAR = [{"contrato": CONTRATO, "funciones": ["registrar"]}]


def comision_anterior(fecha: str, comision: int) -> str:
    """Una línea de comisiones.jsonl de una transacción anterior del mismo rol."""
    return json.dumps({
        "fecha": fecha, "rol": ROL, "contrato": CONTRATO, "funcion": "registrar",
        "solicitud_sha256": hashlib.sha256(b"solicitud anterior").hexdigest(),
        "entradas_sha256": [hashlib.sha256(b"entrada anterior").hexdigest()],
        "xdr_publicado": "publicadas/anterior.xdr", "comision_estimada_stroops": COMISION_ESTIMADA,
        **TRANSACCION_CA_01_1, "comision_stroops": comision,
    }) + "\n"


class SolicitudDePrueba(unittest.TestCase):
    """Si esto falla, las demás pruebas fallarían por un error propio y no por el relayer."""

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


class ConRegistro(unittest.TestCase):
    def setUp(self):
        self._carpeta = tempfile.TemporaryDirectory()
        self.registro = Path(self._carpeta.name)
        self.red = mock.Mock(spec=["ultimo_ledger", "estimar_comision", "transmitir"])
        self.red.ultimo_ledger.return_value = VENCE - 100
        self.red.estimar_comision.return_value = COMISION_ESTIMADA
        self.red.transmitir.return_value = dict(TRANSACCION_CA_01_1)

    def tearDown(self):
        self._carpeta.cleanup()

    def procesar(self, pol: dict) -> dict:
        return Relayer(pol, self.registro, self.red, lambda: AHORA).procesar(solicitud_ca_01_1())

    def lineas(self, nombre: str) -> list:
        return [json.loads(linea) for linea in (self.registro / nombre).read_text().splitlines()]


class Rechazos(ConRegistro):
    def comprobar_rechazo(self, resultado: dict, codigo: str) -> dict:
        self.assertEqual(resultado["estado"], "rechazada")
        self.assertEqual(resultado["codigo"], codigo)
        self.red.transmitir.assert_not_called()
        self.assertEqual(list(self.registro.glob("publicadas/*")), [])
        (linea,) = self.lineas("rechazos.jsonl")
        self.assertEqual(linea["codigo"], codigo)
        self.assertEqual(linea["fecha"], "2026-11-10T15:00:00Z")
        self.assertEqual(linea["rol"], ROL)
        self.assertEqual(linea["contrato"], CONTRATO)
        self.assertEqual(linea["funcion"], "registrar")
        self.assertEqual(linea["detalle"], resultado["detalle"])
        return linea

    def test_rechaza_contrato_no_permitido(self):
        resultado = self.procesar(politica([{"contrato": OTRO_CONTRATO, "funciones": ["registrar"]}]))
        linea = self.comprobar_rechazo(resultado, "CONTRATO_NO_PERMITIDO")
        self.assertEqual(linea["detalle"], {"contrato": CONTRATO})
        self.assertEqual(self.red.method_calls, [])  # se rechaza sin tocar la red

    def test_rechaza_funcion_no_permitida(self):
        resultado = self.procesar(politica([{"contrato": CONTRATO, "funciones": ["rotar"]}]))
        linea = self.comprobar_rechazo(resultado, "FUNCION_NO_PERMITIDA")
        self.assertEqual(linea["detalle"], {"contrato": CONTRATO, "funcion": "registrar", "permitidas": ["rotar"]})
        self.assertEqual(self.red.method_calls, [])  # se rechaza sin tocar la red

    def test_rechaza_invocacion_que_supera_el_tope_de_gasto(self):
        anterior = comision_anterior("2026-11-10T09:00:00Z", COMISION_COBRADA)  # seis horas antes, dentro del período
        (self.registro / "comisiones.jsonl").write_text(anterior)

        # 13 677 consumidos + 23 824 estimados = 37 501, más que el tope de 30 000.
        resultado = self.procesar(politica(REGISTRAR, tope=30000))
        linea = self.comprobar_rechazo(resultado, "TOPE_DE_GASTO")
        self.assertEqual(linea["detalle"], {
            "consumido_stroops": COMISION_COBRADA,
            "comision_estimada_stroops": COMISION_ESTIMADA,
            "tope_stroops": 30000,
            "periodo_segundos": 86400,
        })
        self.assertEqual((self.registro / "comisiones.jsonl").read_text(), anterior)  # el rechazo no suma consumo

    def test_rechaza_rol_que_no_esta_en_la_politica(self):
        resultado = self.procesar(politica(REGISTRAR, rol=OTRO_ROL))
        linea = self.comprobar_rechazo(resultado, "ROL_NO_PERMITIDO")
        self.assertEqual(linea["detalle"], {"rol": ROL})
        self.assertEqual(self.red.method_calls, [])

    def test_rechaza_por_limite_de_frecuencia(self):
        (self.registro / "comisiones.jsonl").write_text(comision_anterior("2026-11-10T14:00:00Z", COMISION_COBRADA))
        resultado = self.procesar(politica(REGISTRAR, max_solicitudes=1))
        linea = self.comprobar_rechazo(resultado, "LIMITE_DE_FRECUENCIA")
        self.assertEqual(linea["detalle"], {"solicitudes_en_periodo": 1, "max_solicitudes": 1, "periodo_segundos": 86400})
        self.assertEqual(self.red.method_calls, [])

    def test_rechaza_comision_estimada_excesiva(self):
        resultado = self.procesar(politica(REGISTRAR, comision_maxima=20000))
        linea = self.comprobar_rechazo(resultado, "COMISION_EXCESIVA")
        self.assertEqual(linea["detalle"], {"comision_estimada_stroops": COMISION_ESTIMADA, "comision_maxima_stroops": 20000})
        self.red.estimar_comision.assert_called_once()

    def test_rechaza_firma_vencida(self):
        self.red.ultimo_ledger.return_value = VENCE  # la firma vale hasta este ledger: ya no entra en el siguiente
        resultado = self.procesar(politica(REGISTRAR))
        linea = self.comprobar_rechazo(resultado, "ENTRADA_INVALIDA")
        self.assertEqual(linea["detalle"], {"razon": "vencida", "vence_en_ledgers": 0})
        self.red.estimar_comision.assert_not_called()


class Aceptada(ConRegistro):
    def test_acepta_publica_transmite_y_registra_la_comision(self):
        # Una transacción de hace 25 horas, fuera del período: no cuenta para el tope ni para la frecuencia.
        vieja = comision_anterior("2026-11-09T14:00:00Z", 999999)
        (self.registro / "comisiones.jsonl").write_text(vieja)
        solicitud = solicitud_ca_01_1()
        sha = hashlib.sha256("\n".join([solicitud["funcion_host"], *solicitud["entradas"]]).encode()).hexdigest()

        resultado = self.procesar(politica(REGISTRAR, tope=30000, max_solicitudes=1))

        self.assertEqual(resultado, {
            "estado": "aceptada", "rol": ROL, "contrato": CONTRATO, "funcion": "registrar",
            "xdr_publicado": f"publicadas/{sha}.xdr", "comision_estimada_stroops": COMISION_ESTIMADA,
            "transaccion": TRANSACCION_CA_01_1,
        })
        self.assertEqual((self.registro / f"publicadas/{sha}.xdr").read_text(), "\n".join(solicitud["entradas"]))
        self.assertEqual([c[0] for c in self.red.method_calls], ["ultimo_ledger", "estimar_comision", "transmitir"])
        funcion_host, entradas = self.red.transmitir.call_args.args
        self.assertEqual(funcion_host.to_xdr(), solicitud["funcion_host"])
        self.assertEqual([e.to_xdr() for e in entradas], solicitud["entradas"])

        anterior, nueva = self.lineas("comisiones.jsonl")
        self.assertEqual(nueva, {
            "fecha": "2026-11-10T15:00:00Z", "rol": ROL, "contrato": CONTRATO, "funcion": "registrar",
            "solicitud_sha256": sha,
            "entradas_sha256": [hashlib.sha256(e.encode()).hexdigest() for e in solicitud["entradas"]],
            "xdr_publicado": f"publicadas/{sha}.xdr", "comision_estimada_stroops": COMISION_ESTIMADA,
            **TRANSACCION_CA_01_1,
        })
        self.assertFalse((self.registro / "rechazos.jsonl").exists())


if __name__ == "__main__":
    unittest.main()
