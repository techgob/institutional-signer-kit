# Institutional Signer Kit

**Una entidad pública firma en Stellar sin tener ni un XLM.**

[English](README.md) · [Statement of Work](docs/statement-of-work.md) · Apache-2.0

---

## El problema

Ninguna municipalidad peruana puede comprar, custodiar ni rendir cuentas de un criptoactivo solo para pagar comisiones de red. Hacerlo exige un proceso de contratación, una partida presupuestal, reglas de custodia de claves y rendición ante la Contraloría, y choca con el principio de unidad de caja del sistema de tesorería. El costo administrativo de habilitar el pago supera en órdenes de magnitud al pago mismo.

Ahí mueren la mayoría de los pilotos de blockchain público, antes de discutir arquitectura.

## Qué resuelve

Soroban lo resuelve en el protocolo: las entradas de autorización se firman de forma independiente del sobre de la transacción, así que quien autoriza y quien paga pueden ser cuentas distintas.

Este repositorio empaqueta esa propiedad como componente reutilizable:

- **firma por rol y ciclo**, con claves que pertenecen a cargos y períodos, no a personas;
- **relayer con política restringida**, que solo puede transmitir invocaciones autorizadas y con tope de gasto;
- **trazabilidad entre comisión y autorización**, que permite auditar al operador;
- **autorización portátil**, publicada, de modo que cualquier tercero puede transmitirla. El operador opera el registro y no puede censurarlo.

Para la entidad: saldo cero en XLM, ninguna partida presupuestal, ninguna custodia de activos, y una autorización acotada en objeto y plazo.

## La prueba

| | |
|---|---|
| Separación firmante-pagador en testnet | [`8ba16039…7e5f`](https://stellar.expert/explorer/testnet/tx/8ba160396082e0ac29dc0324e96a119a90f99c2e9fd9a10aa2941746c14e7e5f) |
| Autorización del rol publicada como XDR y transmitida por un tercero | [`fb284c5b…b8dd`](https://stellar.expert/explorer/testnet/tx/fb284c5b28ce79738db571107c0f8ce0906fd7d48bb39b09e1282d0c2a64b8dd) |
| Video de demostración (2 min) | `[enlace]` |

## Validado en un caso real

Dos municipalidades peruanas que ejecutan el presupuesto participativo obligatorio por ley, elegidas como extremos opuestos:

| | Tocache (provincial) | La Punta (distrital) |
|---|---|---|
| Publicación | Sin actas ni informes finales | Cinco ciclos completos en línea |
| Firma | Manuscrita y luego escaneada | Siete certificados digitales |
| Presupuesto de inversión 2025 | S/ 41,3 M | S/ 2,7 M |
| Ejecución 2025 | 74,9 % | 90,9 % |

A ninguna le falta capacidad de gasto. A las dos les falta una cadena de evidencia que conecte lo que los vecinos acordaron con lo que efectivamente se hizo.

## Cómo ejecutarlo

```bash
pip install "jsonschema[format]"

# contrato de datos: 7 casos de prueba, todos deben pasar
python3 data-contract/validar_ingesta.py --pruebas

# validar una ordenanza real contra el esquema
python3 data-contract/validar_ingesta.py data-contract/ejemplo_ordenanza_001-2026-MPT.json
```

El segundo comando reporta la ordenanza como `observado` y lista las 16 inconsistencias halladas en el documento real. Ese es el resultado esperado: el validador bloquea el anclaje mientras la huella no se verifique contra la fuente oficial.

## Mapa del repositorio

| Ruta | Contenido |
|---|---|
| `signer-kit/` | El componente: firma de autorizaciones y relayer |
| `contracts/` | Contratos Soroban: génesis del ciclo y guardas |
| `data-contract/` | Esquema JSON con reglas de admisión por campo, validador en dos capas y casos de prueba |
| `planning/` | El plan de sprint como datos validados, no como prosa |
| `evidence/` | Huellas y enlaces de documentos oficiales y transacciones |
| `docs/` | Statement of Work, máquina de estados, regla de protección de datos, decisiones de arquitectura |

## Estado

**Hecho, autofinanciado (unas 45 horas de diseño):** máquina de estados derivada artículo por artículo de las normas de ambas municipalidades; contrato de datos con reglas de admisión por campo; validador en dos capas con 7 casos de prueba; análisis forense de los documentos de ambas entidades; prueba de concepto en testnet de la separación firmante-pagador.

**Lo que financia esta instaward:** Signer Kit v1 empaquetado y documentado; registro del ciclo T0 a T8 en testnet con sus guardas; ingesta v2 con los dos perfiles de documento; verificador ciudadano; investigación de usuario en ambas municipalidades.

**Fuera de alcance por ahora:** tokenización, sustitución de proyectos, multifirma por rol y ciclo, perfil del Programa del Vaso de Leche, mainnet y auditoría externa.

## Protección de datos por diseño

Solo se ancla lo que es público por mandato legal. Nunca datos personales. Las claves pertenecen a roles y ciclos, no a personas. El esquema lo hace cumplir de forma estructural: rechaza campos no declarados y falla si un nombre de campo sugiere un dato personal. Ver [docs/proteccion-datos.md](docs/proteccion-datos.md).

## Licencia y créditos

Apache-2.0. Ver [AUTHORS.md](AUTHORS.md).

Desarrollado por [TechGob](https://techgob.cl) — TECH GOB CONSULTORA EN TRANSFORMACIÓN DIGITAL Y TECNOLOGÍAS EMERGENTES SpA, Chile.
