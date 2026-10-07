# Pieza 2: plugin sobre OpenZeppelin Relayer o relayer propio

Evaluación del 7 de octubre de 2026 para decidir cómo construir el relayer con política
restringida dentro de E1. Las referencias a código de terceros usan estos commits:
[OpenZeppelin/openzeppelin-relayer](https://github.com/OpenZeppelin/openzeppelin-relayer)
`fe0bea6f` (**OZR**, versión 1.8.0),
[OpenZeppelin/relayer-plugin-channels](https://github.com/OpenZeppelin/relayer-plugin-channels)
`c7cf073b` (**CH**) y
[OpenZeppelin/openzeppelin-relayer-sdk](https://github.com/OpenZeppelin/openzeppelin-relayer-sdk)
`076489ec` (**SDK**). Las horas son estimaciones propias a partir de las tareas listadas; no hay
una fuente externa que las respalde.

## Qué exige E1

La pieza 2 comparte las 35 horas de desarrollo de E1 (`docs/statement-of-work.md:257`) con otros
seis frentes de construcción (`:117-123`): `sign-auth-entry` genérico, registro de comisiones
(pieza 3), publicación de cada entrada como XDR (pieza 4), soporte para los dos tipos de rol,
comandos de traspaso y verificación, y las guías. De la pieza 2 el SOW pide lista de contratos y
funciones permitidos, tope de gasto por rol, límite de frecuencia y registro de rechazos (`:118`),
y tres pruebas automatizadas de rechazo: contrato no permitido, función no permitida y tope de gasto
superado (`:128`).

Si la pieza 2 se lleva más de la mitad de las 35 horas, el resto de E1 queda comprometido.

## Lo que el kit ya tiene

| Pieza existente | Dónde | Sirve para |
|---|---|---|
| Construcción genérica de la invocación (contrato, función, argumentos) | `signer-kit/passkey.py:74-78` | Rearmar la invocación que autorizó el rol |
| Envío: adjunta la entrada firmada, prepara (simula), firma como operador y transmite | `signer-kit/passkey.py:89-94`; `signer-kit/hu01.py:96-101` | Núcleo del relayer |
| Espera de confirmación | `signer-kit/hu01.py:104-110` | Confirmar antes de registrar la comisión |
| Comisión cobrada leída del resultado | `signer-kit/hu01.py:113-125` | Registro de comisiones (pieza 3) y conteo del tope |
| Publicación de la entrada como XDR antes de transmitir | `signer-kit/hu01.py:150` | Pieza 4 |
| Lectura de las credenciales de una entrada de autorización | `verifier/conformidad.py:30` | Identificar el rol que autorizó |
| Verificación C1 a C6 de una transacción confirmada | `verifier/conformidad.py:35-90` | Prueba de aceptación de E1 |

SDK de Python en uso: `stellar-sdk==16.1.0` (`signer-kit/requirements.txt`), con licencia
Apache-2.0 según sus metadatos de paquete (`License-Expression: Apache-2.0`).

## Camino (a): plugin propio sobre OpenZeppelin Relayer, con o sin Channels

### Lo que ya existe

- El relayer acepta una invocación de contrato con entradas de autorización ya firmadas: operación
  `invoke_contract` con `auth` de tipo `xdr` (OZR `docs/stellar.mdx:277`, `:425-445`, `:514-522`).
  El relayer arma la transacción con su propia cuenta como origen y la transmite.
- Plugins en TypeScript invocados en `/api/v1/plugins/{plugin-id}/call{route}` (OZR
  `docs/plugins/index.mdx:272`), con `params`, `headers` y `route` en el contexto (`:106-125`),
  acceso al relayer con `api.useRelayer(...).sendTransaction(...)` (`:74-76`) y errores 4xx con
  `code` y `details` (`:327-334`).
- Almacenamiento clave-valor por plugin con vencimiento y bloqueo (`kv.set` con `ttlSec`,
  `kv.withLock`), guardado en el mismo Redis del relayer (OZR `docs/plugins/index.mdx:553-576`).
- Channels acepta el par `func` y `auth` y arma la transacción por su cuenta (OZR
  `docs/plugins/channels.mdx:435-461`); trae tope de gasto por clave de API y período
  (CH `src/plugin/config.ts:65-77`, `src/plugin/fee-tracking.ts:63-77`).

### Lo que hay que escribir

| Tarea | Horas estimadas |
|---|---|
| Levantar relayer y Redis (requisitos: OZR `docs/quickstart.mdx:9-12`), configurar el relayer de testnet, el firmante y la clave de API | 3 a 5 |
| Esqueleto del plugin, declaración en la configuración, dependencias de TypeScript | 1 a 2 |
| Decodificar la función de host para obtener contrato y función, e identificar el rol en la entrada | 2 a 3 |
| Tope por rol y límite de frecuencia con `kv.withLock` | 2 a 3 |
| Estimar la comisión antes de enviar, simulando desde el plugin: la política `max_fee` del relayer no se aplica cuando paga el relayer (ver `docs/diferenciacion.md`) | 2 a 3 |
| Envío con `sendTransaction`, espera y lectura de la comisión cobrada | 2 a 3 |
| Registro de rechazos y una ruta para exportarlo al verificador en Python | 2 a 3 |
| Pruebas del plugin con contexto simulado (OZR `docs/plugins/index.mdx:231-260`) y su integración continua con Node | 3 a 5 |
| **Total sin Channels** | **17 a 27** |
| Channels: crear y fondear las cuentas de canal y la cuenta que paga | +2 a 4 |

Channels no resuelve el tope por rol: su límite es por clave de API (CH `src/plugin/config.ts:65-77`).
Para usarlo como tope por rol haría falta una clave de API por rol. Su ventaja principal es el envío
en paralelo, que este volumen no necesita.

### Riesgos

- **Licencia.** El relayer es AGPL-3.0 (OZR `LICENSE`). El SDK que importa todo plugin
  (OZR `docs/plugins/index.mdx:42`, `:107`) es `AGPL-3.0-or-later` (SDK `package.json:5`). Channels
  declara MIT en `package.json:38` y en su README (`README.md:1263-1265`), pero su archivo `LICENSE`
  es el texto de la AGPL-3.0: la licencia efectiva no está clara. Un plugin que importa el SDK
  probablemente quede como obra derivada de un componente AGPL. Requiere revisión legal antes de
  decidir con qué licencia se publica.
- **Operación.** Suma un servicio en Rust, Redis y Node a un kit escrito en Python. El SOW prevé
  traspasar la operación al laboratorio de la SGTD (`docs/statement-of-work.md`, sección 7), que
  tendría que operar esa pila.
- **Cambios de versión.** Entre el 20 de febrero y el 19 de agosto de 2026 salieron las versiones
  1.4.0 a 1.8.0 (OZR `CHANGELOG.md:3-128`).
- **Puerta única.** La restricción solo vale si los clientes no pueden llamar a la API del relayer
  directamente; hay que administrar las claves de API para que solo el plugin la use.
- **No verificado.** Si el resultado de `sendTransaction` informa la comisión cobrada; si no la
  informa, hay que consultarla por RPC.

## Camino (b): relayer propio mínimo en Python

### Lo que ya existe

Todo lo de la tabla "Lo que el kit ya tiene". El envío, la espera, la lectura de la comisión, la
publicación del XDR y la lectura de credenciales ya están escritos y probados en testnet
(`evidence/transacciones.md`).

### Lo que hay que escribir

| Tarea | Horas estimadas |
|---|---|
| Entrada de la solicitud (función de host y entradas firmadas en XDR), decodificación de contrato y función, identificación del rol | 2 a 3 |
| Lista permitida en un archivo de configuración; tope por rol y límite de frecuencia en SQLite (biblioteca estándar) con transacciones | 3 a 4 |
| Estimar la comisión con la transacción preparada antes de firmar; firmar, enviar y registrar la comisión cobrada con la entrada que la originó | 2 a 3 |
| Registro de rechazos y publicación del XDR antes de enviar | 1 a 2 |
| Comando del kit o servicio HTTP mínimo (biblioteca estándar) | 1 a 2 |
| Tres pruebas de rechazo con `unittest`, sin red, porque los rechazos ocurren antes de enviar; una corrida en testnet del caso aceptado | 3 a 4 |
| **Total** | **12 a 18** |

### Riesgos

- **Seguridad propia.** El código que custodia la clave del operador es nuestro; no hay KMS ni
  componentes auditados. En E1 corre en testnet, pero mainnet exige revisarlo
  (`docs/adr-001-contratos-soroban.md` ya condiciona mainnet a una auditoría).
- **Robustez.** Sin envío en paralelo ni reintentos con fee-bump. Con el volumen de un ciclo de
  presupuesto participativo alcanza con enviar en serie, pero hay que documentarlo.
- **Pregunta del revisor.** "¿Por qué no OpenZeppelin Relayer?" La respuesta está en este documento
  y en `docs/diferenciacion.md`.
- **Migración futura.** Si más adelante se adopta el relayer de OpenZeppelin, habrá que reescribir
  la política como plugin. Se reduce manteniendo la misma interfaz y los mismos códigos de rechazo.

### Licencia

Apache-2.0 sin cambios: el relayer usa solo el SDK de Python, que también es Apache-2.0.

## Comparación

| | (a) Plugin sobre OpenZeppelin | (b) Relayer propio |
|---|---|---|
| Horas estimadas | 17 a 27 (19 a 31 con Channels) | 12 a 18 |
| Horas que quedan para el resto de E1 | 8 a 18 (4 a 16 con Channels) | 17 a 23 |
| Lenguajes y servicios nuevos | TypeScript, Node, Redis, servicio en Rust | Ninguno |
| Pruebas de rechazo sin red | Sí, con contexto simulado | Sí, con `unittest` |
| Licencia | AGPL en el SDK y el relayer; requiere revisión legal | Apache-2.0 |
| Custodia de la clave del operador | Keystore local, Google Cloud KMS o Turnkey, según la guía de OpenZeppelin Relayer en la documentación de Stellar | Lo que escribamos |

## Recomendación

**Camino (b) para E1.** Cabe con margen en las 35 horas, reutiliza código ya probado en testnet,
mantiene el kit en un solo lenguaje y en Apache-2.0, y las tres pruebas de rechazo corren en la
integración continua actual sin red. El camino (a) es viable, pero se lleva entre la mitad y casi
todas las horas de E1 y trae una pregunta de licencia sin resolver.

Para no cerrar la puerta a (a): definir la interfaz del relayer (rutas, entrada, respuesta y
códigos de rechazo) independiente de la implementación, de modo que una iteración posterior pueda
implementarla como plugin de OpenZeppelin cuando la operación pase a la SGTD o el volumen lo
justifique. Esa interfaz no está escrita todavía.
