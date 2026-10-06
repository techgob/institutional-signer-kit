# Registro Verificable del Presupuesto Participativo — demo

Página estática, un solo archivo, sin dependencias ni paso de compilación. Todo el CSS y el
JavaScript van en línea; lo único externo son las tipografías de Google Fonts (IBM Plex Mono e
Inter), con pila de respaldo declarada, así que la página funciona igual si no cargan.

Bilingüe ES/EN con selector en la barra superior. Línea gráfica TechGob, enfoque blockchain:
ciruela, lavanda y lima, sin tarjetas, con la estructura marcada por filetes.

## Contenido

| Archivo | Para qué |
|---|---|
| `index.html` | La página completa |
| `_headers` | Cabeceras de seguridad y caché que aplica Cloudflare Pages |
| `robots.txt` | Indexación abierta |
| `wrangler.toml` | Nombre del proyecto y directorio de salida |

## Subirla a Cloudflare Pages

**Opción A — panel web, sin instalar nada.** En el panel de Cloudflare: Workers & Pages →
Create → Pages → Upload assets. Arrastra esta carpeta (o el `.zip` que la acompaña) y publica.

**Opción B — línea de comandos.**

```sh
npm install -g wrangler
wrangler login
wrangler pages deploy . --project-name=isk-demo
```

La primera ejecución crea el proyecto. Las siguientes publican una versión nueva y Cloudflare
conserva la anterior, así que se puede volver atrás desde el panel.

**Dominio propio.** Pages entrega `isk-demo.pages.dev`. Para servirla en un subdominio de
techgob.cl: Pages → el proyecto → Custom domains → Set up a custom domain. Si el DNS de la zona
está en Cloudflare, el registro se crea solo.

## Procedencia de los datos

Nada en esta página es un valor de ejemplo. Cada dato viene del repositorio
[`techgob/institutional-signer-kit`](https://github.com/techgob/institutional-signer-kit):

- las catorce transiciones, sus firmantes, su evidencia exigida, su base legal y las doce guardas,
  de `docs/maquina-estados.md`;
- los trece criterios de priorización y sus valores permitidos, de
  `data-contract/ingesta_documento_pp.schema.json`;
- las dieciséis inconsistencias y las transiciones que afecta cada una, del campo
  `transiciones_afectadas` de `data-contract/ejemplo_ordenanza_001-2026-MPT.json`;
- las diez transacciones con su ledger y su comisión, de `evidence/hu01/evidencia.json`,
  `evidence/operador/traspaso.json` y `evidence/passkey/passkey.json`;
- los resultados del verificador documental y las seis comprobaciones de conformidad, de
  `verifier/README.md`.

Donde el repositorio no registra un valor, la página muestra `SIN DATO` en lugar de estimarlo. Es
el caso del ledger y la comisión de la transacción `9dd4146f…5e5f`.

## Lo que la página declara como no probado

El contrato de génesis con sus guardas no está desplegado, así que cada hito marca sus guardas
como especificadas y no ejecutadas en red. El relayer con política restringida tampoco está
implementado. La única ingesta validada contra un documento real es la de T0.

## Mantenimiento

La red de pruebas de Stellar se reinicia cada trimestre y borra sus datos. Si los enlaces al
explorador dejan de resolver, hay que rehacer las corridas con los scripts del repositorio y
actualizar los arreglos `TXS` y `CHECKS_DOC` dentro de `index.html`, que están al principio del
bloque `<script>` y son los únicos lugares donde viven esos valores.

Apache-2.0 · TECH GOB CONSULTORA EN TRANSFORMACIÓN DIGITAL Y TECNOLOGÍAS EMERGENTES SpA
