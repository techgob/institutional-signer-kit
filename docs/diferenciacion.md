# Diferenciación frente a lo que ya existe en Stellar

Consulta hecha el 7 de octubre de 2026 con Raven (Stellar Docs, Scout y Lumenloop). Los montos y
estados de proyectos de terceros son los que esas fuentes registran a esa fecha y pueden cambiar.
Donde una fuente no permitió verificar algo, se dice.

## La pregunta que hará un revisor

Separar a quien firma de quien paga ya es posible en Stellar con piezas oficiales y con
servicios existentes. Un revisor va a preguntar por qué hace falta este kit. La respuesta corta:
el kit se apoya en esas piezas y agrega lo que una institución pública necesita para que el
arreglo sea aceptable ante su contraloría. Las secciones siguientes lo detallan.

## Piezas oficiales y servicios existentes

| Pieza | Qué hace, según la fuente | Relación con el kit | Fuente |
|---|---|---|---|
| Transacciones fee-bump | Una cuenta distinta paga la comisión de una transacción ya firmada | Alternativa clásica para separar pagador y firmante. Con fee-bump la institución firma la transacción completa como cuenta de origen; con las entradas de autorización de Soroban que usa el kit firma solo la invocación que autoriza, acotada por nonce y ledger de vencimiento | [Guía oficial](https://developers.stellar.org/docs/build/guides/transactions/fee-bump-transactions) |
| Reservas patrocinadas | Otra cuenta cubre la reserva mínima de una cuenta | El kit ya las usa: la cuenta del rol se crea con 0 XLM y reserva patrocinada (HU-01, paso 0) y el traspaso de operador mueve el patrocinio (T-1) | [Guía oficial](https://developers.stellar.org/docs/build/guides/transactions/sponsored-reserves) · `evidence/transacciones.md` |
| OpenZeppelin Relayer | Marco de código abierto (AGPL-3.0) para enviar transacciones de Stellar, incluidas invocaciones de Soroban. Quien lo opera controla el firmante y financia las cuentas que pagan. Su plugin Channels agrega envío en paralelo y fee-bump automático | Base candidata para la pieza 2. Su política para Stellar no permite restringir contratos ni funciones; el plugin Channels sí trae un tope de gasto por período. Detalle con archivo y línea en la sección siguiente | [Docs: OpenZeppelin Relayer](https://developers.stellar.org/docs/tools/openzeppelin-relayer) |
| Stellar Channels (servicio administrado) | OpenZeppelin opera el pool de cuentas de canal y cubre las comisiones bajo una política de uso razonable. Reemplaza a Launchtube, que SDF discontinuó | Para una institución pública, depender del pagador de un tercero sin acuerdo formal no resuelve la trazabilidad ni la continuidad; por eso el kit define un operador identificable y su traspaso | [Docs: herramientas](https://developers.stellar.org/docs/tools#openzeppelin-relayer) |
| Cuentas inteligentes de OpenZeppelin | Bibliotecas de cuentas de contrato con reglas de contexto, firmantes y políticas | Candidato fuerte para la firma por rol y ciclo en una versión posterior. La ADR-001 ya prevé reutilizar módulos auditados de OpenZeppelin antes de mainnet | Charla "Building Stellar Smart Accounts With OpenZeppelin Libraries" (Lumenloop, 2026-04-24) · `docs/adr-001-contratos-soroban.md` |

## OpenZeppelin Relayer: qué se puede restringir

Revisión del código fuente del 7 de octubre de 2026, en dos repositorios:
[OpenZeppelin/openzeppelin-relayer](https://github.com/OpenZeppelin/openzeppelin-relayer) en el
commit `fe0bea6f` (abreviado **OZR**) y
[OpenZeppelin/relayer-plugin-channels](https://github.com/OpenZeppelin/relayer-plugin-channels) en
el commit `c7cf073b` (abreviado **CH**). Las líneas corresponden a esos commits.

| Lo que necesita la pieza 2 | En el núcleo del relayer | En el plugin Channels |
|---|---|---|
| Lista de contratos permitidos | No existe. La política de Stellar solo tiene `min_balance`, `max_fee`, `timeout_seconds`, `concurrent_transactions`, `allowed_tokens`, `fee_payment_strategy`, `slippage_percentage`, `fee_margin_percentage` y `swap_config` (OZR `src/models/relayer/mod.rs:607-629`; tabla en OZR `docs/stellar.mdx:92-102`). Al validar una invocación, el código dice "Contract invocations are allowed by default" y no usa la política (`_policy`) (OZR `src/domain/transaction/stellar/validation.rs:603-609`) | No existe. `LIMITED_CONTRACTS` reparte la capacidad del pool de cuentas de canal y los contratos no listados conservan acceso completo (OZR `docs/plugins/channels.mdx:190-191`, `:195-199`, `:213`) |
| Lista de funciones permitidas | No encontré ninguna opción ni validación por nombre de función | No encontré ninguna opción ni validación por nombre de función |
| Tope por transacción | `max_fee` de la política (OZR `validation.rs:216-226`). Solo encontré llamadas desde el flujo en que el usuario paga en tokens (`fee_payment_strategy: User`): OZR `src/domain/relayer/stellar/gas_abstraction.rs:306`, `:422`, `:636`, `:797`, con la exigencia de esa estrategia en `:198-201` y `:516-519`. En un fee-bump el tope lo manda quien hace la solicitud (OZR `src/domain/transaction/stellar/prepare/fee_bump.rs:100-105`; `docs/stellar.mdx:293`) | `MAX_FEE` (OZR `docs/plugins/channels.mdx:186`) |
| Tope de gasto por período | No encontré nada equivalente | Sí: `FEE_LIMIT` por clave de API y `FEE_RESET_PERIOD_SECONDS` para reiniciar el conteo (CH `src/plugin/config.ts:65-77`; OZR `docs/plugins/channels.mdx:187-188`). Al superarse responde `FEE_LIMIT_EXCEEDED` con estado 429 (CH `src/plugin/fee-tracking.ts:63-77`), y se comprueba antes de enviar (CH `src/plugin/handler.ts:160`, `:263`) |
| Validación de la transacción antes de pagar | Solo cuando paga el usuario: la validación "gasless" (OZR `validation.rs:810-824`) corre en fee-bump únicamente con `fee_payment_strategy: User` (OZR `fee_bump.rs:51-56`). Ahí rechaza `CreateContract` y `UploadContractWasm` (OZR `validation.rs:610-619`) y que el relayer aparezca como firmante requerido (`:627-651`) | No encontré validación de contrato o función en `src/plugin/handler.ts` ni en `src/plugin/validation.ts` |

**Conclusión.** Ni el núcleo ni Channels permiten hoy decir "este pagador solo paga la función
`registrar` del contrato X". Channels resuelve el tope de gasto por período. El relayer admite
plugins propios en TypeScript, invocados en `/api/v1/plugins/{plugin-id}/call{route}`
(OZR `docs/plugins/index.mdx:272`) y con almacenamiento clave-valor persistente
(OZR `docs/plugins/index.mdx:16`, `:123`).

**Propuesta para la pieza 2 (inferencia nuestra, no probada).** Un plugin propio que decodifique la
invocación, la compare con una lista de contrato y función, lleve el conteo de gasto y frecuencia
en el almacenamiento clave-valor y recién entonces envíe por el relayer o por Channels. Para que la
restricción valga, los clientes no pueden tener acceso directo a la API del relayer: solo al
plugin. El SOW pide tope de gasto por rol y registro de rechazos (`docs/statement-of-work.md`,
pieza 2); con Channels, el tope por rol equivaldría a una clave de API por rol. Queda por medir si
esto cuesta menos que un relayer propio dentro de las 35 horas de desarrollo que el SOW asigna a E1.

## Proyectos del ecosistema más cercanos

| Proyecto | Qué hace | Financiamiento SCF registrado | Diferencia con el kit |
|---|---|---|---|
| Smart Account Kit | SDK en TypeScript para cuentas inteligentes de OpenZeppelin con passkeys WebAuthn, reglas de contexto y clientes de políticas | Scout: sin SCF | Herramienta general para billeteras. No modela roles institucionales, ciclos ni operador |
| SoroPass | SDK mínimo de passkeys y componentes para crear, firmar y recuperar cuentas inteligentes | Lumenloop: SCF #44, Build, USD 95 000, "Awarded". Scout lo marca sin SCF. Las fuentes no coinciden | Resuelve la experiencia de usuario de passkeys; el kit usa passkeys solo como mecanismo de rotación por ciclo |
| Latch | Incorporación de direcciones C (cuentas inteligentes) sin pasar por una dirección G, sobre OpenZeppelin | Scout: SCF #41, USD 120 000 | Resuelve cómo fondear una cuenta inteligente; el kit busca que la institución nunca tenga saldo |
| Teken | Aplicación de multifirma sobre contratos Soroban | Scout y Lumenloop: SCF #28, Activation Award, USD 29 500 | La multifirma por rol y ciclo está fuera del alcance de esta etapa (G9, segunda iteración) |
| Simple Signer | Firmador de transacciones en el navegador compatible con varias billeteras | Scout: SCF #9, USD 10 000 | Otro problema: firma de usuarios finales, sin separación de pagador |

Ninguno de estos proyectos, según lo que registran las fuentes consultadas, aborda la restricción
que da origen al kit: una entidad pública que no puede comprar ni custodiar XLM y que necesita
una cadena de evidencia verificable por terceros. Esto es una observación sobre las fuentes
consultadas y no prueba que no exista otro proyecto similar.

## Lo que el kit agrega

1. **Firma por rol y ciclo.** La clave pertenece al cargo y al período. Probado en testnet con
   cuenta clásica de 0 XLM y con cuenta de contrato con passkey que rota por ciclo.
2. **Relayer con política restringida.** No implementado; es parte de la instaward. Ver la nota
   sobre OpenZeppelin Relayer más arriba.
3. **Trazabilidad entre comisión y autorización.** Probada sin claves en `verifier/conformidad.py`.
   Ninguna de las piezas anteriores la ofrece como verificación independiente.
4. **Autorización portátil.** Probada en testnet: una entrada publicada como XDR la transmitió un
   tercero, y el reenvío de una entrada usada fue rechazado.
5. **Aplicación a un proceso legal real.** La máquina de estados del presupuesto participativo
   peruano, construida a partir de documentos de Tocache y La Punta.

## Criterios de Instawards

Según el resumen que Lumenloop guarda del taller "What SDF Looks For in an Instawards
Application?" (SDF, 23 de septiembre de 2026): premios de USD 1 000 a 5 000 para builders en etapa
temprana dentro de capítulos de embajadores, con sprints de 30 días; el programa escala hasta
USD 15 000 en tres rondas, y financia prototipos e infraestructura, no marketing ni incentivos a
usuarios. Solo se consultó ese resumen, no la grabación completa.

| Criterio | Estado en este repositorio |
|---|---|
| Monto entre USD 1 000 y 5 000 | Cumple: USD 5 000 (`docs/statement-of-work.md`, 4.2) |
| Sprint de 30 días | Cumple: plan de 30 días (sección 5 del SOW) |
| Pertenencia a un capítulo de embajadores | Pendiente: DEP-01 "por_solicitar"; capítulo y Chapter Lead "[por confirmar]" en el SOW |
| Prototipo e infraestructura, no marketing | El presupuesto no tiene marketing. Conviene confirmar con el capítulo que el trabajo de campo (USD 600) se acepta |
| Escala hasta USD 15 000 en tres rondas | La sección 7 del SOW describe una siguiente iteración de USD 8 000. Si se piensa como otra instaward, supera el tope por premio; conviene aclarar a qué programa apunta |

## Pendiente de verificar

- La grabación completa del taller de Instawards.
- Que el plugin propuesto para la pieza 2 funcione como se describe; no se escribió ni se probó.
