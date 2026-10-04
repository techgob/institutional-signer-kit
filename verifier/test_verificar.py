import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from verificar import canonico, verificar


class VerificadorTest(unittest.TestCase):
    def setUp(self):
        self.dir = Path(tempfile.mkdtemp())
        self.pdf = self.dir / "doc.pdf"
        self.pdf.write_bytes(b"%PDF-1.7 ordenanza de prueba")
        self.carga = {"archivo": {"sha256": hashlib.sha256(self.pdf.read_bytes()).hexdigest()}, "evento": {"t": "T0"}}
        self.ruta_carga = self.dir / "carga.json"
        self.ruta_carga.write_text(json.dumps(self.carga, indent=2), encoding="utf-8")
        self.compromiso = hashlib.sha256(canonico(self.carga)).hexdigest()

    def test_documento_y_carga_integros_verifican(self):
        r = verificar(self.pdf, self.ruta_carga, self.compromiso)
        self.assertTrue(r["huella_pdf_coincide"]["ok"])
        self.assertTrue(r["compromiso_canonico_coincide"]["ok"])

    def test_pdf_alterado_falla_la_huella(self):
        self.pdf.write_bytes(b"%PDF-1.7 ordenanza alterada")
        r = verificar(self.pdf, self.ruta_carga, self.compromiso)
        self.assertFalse(r["huella_pdf_coincide"]["ok"])
        self.assertTrue(r["compromiso_canonico_coincide"]["ok"])

    def test_carga_alterada_falla_el_compromiso(self):
        self.carga["evento"]["t"] = "T1"
        self.ruta_carga.write_text(json.dumps(self.carga), encoding="utf-8")
        r = verificar(self.pdf, self.ruta_carga, self.compromiso)
        self.assertFalse(r["compromiso_canonico_coincide"]["ok"])

    def test_el_formato_del_archivo_no_cambia_el_compromiso(self):
        self.ruta_carga.write_text(json.dumps(self.carga, separators=(",", ":")), encoding="utf-8")
        r = verificar(self.pdf, self.ruta_carga, self.compromiso)
        self.assertTrue(r["compromiso_canonico_coincide"]["ok"])


if __name__ == "__main__":
    unittest.main()
