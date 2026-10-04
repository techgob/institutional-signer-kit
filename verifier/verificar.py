"""Verificador local de dos comprobaciones, sin cadena.

Recibe el PDF de una ordenanza, la carga admitida publicada y el compromiso esperado, y comprueba:
  1. huella_pdf_coincide         SHA-256 del PDF == archivo.sha256 de la carga admitida
  2. compromiso_canonico_coincide SHA-256 de la carga en forma canónica == compromiso esperado

La forma canónica es la misma del validador de ingesta (data-contract/validar_ingesta.py):
JSON con claves ordenadas, sin espacios, UTF-8 sin escapar.

Uso:
  python verifier/verificar.py <documento.pdf> <carga_admitida.json> <transaccion.json | compromiso_hex>
"""
import hashlib
import json
import sys
from pathlib import Path

# La forma canónica se importa del validador de ingesta para que exista una sola definición.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "data-contract"))
from validar_ingesta import canonico  # noqa: E402


def sha256_archivo(ruta: Path) -> str:
    h = hashlib.sha256()
    with ruta.open("rb") as f:
        for bloque in iter(lambda: f.read(1 << 20), b""):
            h.update(bloque)
    return h.hexdigest()


def compromiso_esperado(argumento: str) -> str:
    ruta = Path(argumento)
    if ruta.is_file():
        return json.loads(ruta.read_text(encoding="utf-8"))["compromiso_sha256"]
    return argumento.strip().lower()


def verificar(pdf: Path, carga_ruta: Path, esperado: str) -> dict:
    carga = json.loads(carga_ruta.read_text(encoding="utf-8"))
    huella_pdf = sha256_archivo(pdf)
    huella_declarada = (carga.get("archivo") or {}).get("sha256")
    compromiso = hashlib.sha256(canonico(carga)).hexdigest()
    return {
        "huella_pdf_coincide": {
            "ok": huella_pdf == huella_declarada,
            "calculada": huella_pdf,
            "declarada_en_carga": huella_declarada,
        },
        "compromiso_canonico_coincide": {
            "ok": compromiso == esperado,
            "calculado": compromiso,
            "esperado": esperado,
        },
    }


def main(argv: list[str]) -> int:
    if len(argv) != 4:
        print(__doc__)
        return 2
    resultado = verificar(Path(argv[1]), Path(argv[2]), compromiso_esperado(argv[3]))
    for nombre, r in resultado.items():
        print(f"{'OK  ' if r['ok'] else 'FALLA'} {nombre}")
        for k, v in r.items():
            if k != "ok":
                print(f"      {k}: {v}")
    todo = all(r["ok"] for r in resultado.values())
    print("VERIFICADO" if todo else "NO VERIFICADO")
    return 0 if todo else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
