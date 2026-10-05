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

## Conformidad de un operador

`conformidad.py` revisa transacciones ya confirmadas en testnet contra las propiedades del kit.
No usa claves, así que lo puede correr cualquier operador sobre sus propias transacciones.

```sh
pip install -r signer-kit/requirements.txt
python3 verifier/conformidad.py <hash> [<hash> ...]
```

| Comprobación | Qué mira |
|---|---|
| C1 | La transacción se confirmó |
| C2 | La única firma es la de la cuenta que envió y pagó |
| C3 | El rol no es quien envía ni paga |
| C4 | El rol autorizó dentro de la llamada, con su firma en la entrada de autorización |
| C5 | Esa autorización vence en 720 ledgers o menos (alrededor de una hora) |
| C6 | El rol no tiene XLM propio (estado actual, no el del momento de la transacción) |

Termina con código 0 solo si todas las transacciones son conformes. Las corridas registradas y sus
resultados están en `../evidence/transacciones.md`. `test_conformidad.py` prueba C2 a C5 sin red,
sobre sobres reales guardados en `datos_prueba/`.
