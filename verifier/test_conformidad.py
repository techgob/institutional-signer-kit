"""Pruebas sin red de las comprobaciones C2 a C5, sobre sobres reales guardados de testnet."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from conformidad import revisar_sobre  # noqa: E402

DATOS = Path(__file__).resolve().parent / "datos_prueba"


def sobre(nombre: str):
    ledger, envelope = (DATOS / f"{nombre}.xdr").read_text().split()
    return revisar_sobre(envelope, int(ledger))


class Conformidad(unittest.TestCase):
    def test_rol_clasico_conforme(self):
        checks, rol = sobre("conforme")  # CA-01-1
        self.assertTrue(all(checks.values()), checks)
        self.assertTrue(rol.startswith("G"))

    def test_rol_con_passkey_conforme(self):
        checks, rol = sobre("passkey")  # P-4
        self.assertTrue(all(checks.values()), checks)
        self.assertTrue(rol.startswith("C"))

    def test_operacion_sin_autorizacion_del_rol_no_es_conforme(self):
        checks, rol = sobre("no_conforme")  # T-1, firmada por dos operadores, sin rol
        self.assertIsNone(rol)
        self.assertFalse(any(checks.values()), checks)


if __name__ == "__main__":
    unittest.main()
