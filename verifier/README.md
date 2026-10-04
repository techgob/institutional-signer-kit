# Verificador local

Comprueba, sin consultar la cadena, que un documento y su carga admitida son los que se
comprometieron.

```sh
python3 data-contract/validar_ingesta.py data-contract/ejemplo_ordenanza_001-2026-MPT.json
python3 verifier/verificar.py <ordenanza.pdf> \
  data-contract/carga_admitida_T0_ejemplo_ordenanza_001-2026-MPT.json \
  data-contract/transaccion_T0_ejemplo_ordenanza_001-2026-MPT.json
python3 -m unittest discover verifier
```

El tercer argumento acepta también el compromiso en hexadecimal.

1. `huella_pdf_coincide`: SHA-256 del PDF contra `archivo.sha256` de la carga admitida.
2. `compromiso_canonico_coincide`: SHA-256 de la carga en forma canónica contra el compromiso
   esperado. La forma canónica se importa de `data-contract/validar_ingesta.py`, así que el
   validador y el verificador no pueden divergir.

## Resultado con la ordenanza 001-2026-MPT

Con el PDF de la ordenanza recibido el 3 de octubre de 2026 y la carga del ejemplo del
repositorio, el compromiso coincide (`ef397780…b455`) y la huella no. El PDF da `2bc20e2a…7c97`
(4 290 931 bytes) y la carga declara `ec76ae49…dc24` (4 283 322 bytes). Es la inconsistencia
INC-01 que ya registra el contrato de ingesta: falta la huella de la descarga directa del portal.
