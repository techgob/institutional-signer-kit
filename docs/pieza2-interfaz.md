# Pieza 2: interfaz del relayer con política restringida

Interfaz del camino (b) de `docs/pieza2-evaluacion.md`, escrita antes de la implementación y sin
depender de ella: una versión posterior como plugin de OpenZeppelin Relayer tendría que respetar
la misma entrada, las mismas respuestas, los mismos códigos de rechazo y los mismos registros.

Requisitos que cubre: lista de contratos y funciones permitidos, tope de gasto por rol, límite de
frecuencia y registro de rechazos (`docs/statement-of-work.md:118`); registro de cada comisión con
la entrada que la originó (`:119`); publicación de la entrada como XDR antes de transmitir
(`:120`); tres pruebas automatizadas de rechazo (`:128`). El README del kit ya describe la pieza
(`signer-kit/README.md:8`) y dice que la lista permitida y el tope no están implementados
(`:16-17`).

Cuando un campo es nuevo y no sale del código actual, se marca como **nuevo**.

## 1. Formas de uso

### Biblioteca (la usan las pruebas)

```python
from relayer import Relayer

relayer = Relayer(politica, registro, red, reloj)
resultado = relayer.procesar(solicitud)
```

| Parámetro | Tipo | Qué es |
|---|---|---|
| `politica` | `dict` | Contenido del archivo de política (sección 5) |
| `registro` | `pathlib.Path` | Carpeta donde viven `comisiones.jsonl`, `rechazos.jsonl` y `publicadas/` (sección 6) |
| `red` | objeto con tres métodos | Todo acceso a la red pasa por aquí; las pruebas lo reemplazan por un doble |
| `reloj` | función sin argumentos que devuelve un `datetime` con zona UTC | Fecha de cada registro y ventana del período |

Métodos de `red`:

| Método | Devuelve | De dónde sale hoy |
|---|---|---|
| `ultimo_ledger()` | `int`, secuencia del último ledger | `signer-kit/hu01.py:92` (`server.get_latest_ledger().sequence`) |
| `estimar_comision(funcion_host, entradas)` | `int`, comisión en stroops de la transacción preparada | `signer-kit/hu01.py:96-99`: arma la invocación, adjunta las entradas y la prepara; la comisión es la de la transacción preparada |
| `transmitir(funcion_host, entradas)` | `dict` con `estado`, `hash`, `enlace`, `transmite_y_paga`, `comision_stroops`, `ledger` | `signer-kit/passkey.py:89-94` (firma como operador y envía), `signer-kit/hu01.py:104-110` (espera) y `:113-125` (arma ese mismo `dict`) |

`funcion_host` es un `xdr.HostFunction` y `entradas` una lista de `xdr.SorobanAuthorizationEntry`,
ya decodificados.

### Comando del kit

```sh
python signer-kit/relayer.py --politica politica.json --registro registro/ --operador <alias> solicitud.json
```

- `--operador`: alias de la CLI de Stellar con la clave del operador; la clave nunca se lee del
  repositorio (`signer-kit/hu01.py:9`, `:32-34`).
- Imprime el resultado (sección 3) como JSON.
- Código de salida: `0` aceptada, `2` rechazada, `3` fallida en la red, `1` error de ejecución.
  **Nuevo.**

### Ruta HTTP (opcional)

`POST /v1/invocaciones` con la solicitud como cuerpo JSON. Misma respuesta que el comando.
Estados HTTP: `200` aceptada o fallida, `400` `ENTRADA_INVALIDA`, `403` `CONTRATO_NO_PERMITIDO`,
`FUNCION_NO_PERMITIDA` y `ROL_NO_PERMITIDO`, `422` `COMISION_EXCESIVA`, `429` `TOPE_DE_GASTO` y
`LIMITE_DE_FRECUENCIA`. **Nuevo.** El 429 para el tope sigue el mismo criterio que el plugin
Channels de OpenZeppelin (ver `docs/diferenciacion.md`).

## 2. Solicitud

```json
{
  "version": 1,
  "funcion_host": "<XDR en base64 de un HostFunction>",
  "entradas": ["<XDR en base64 de un SorobanAuthorizationEntry firmado>"]
}
```

| Campo | Qué es | De dónde sale hoy |
|---|---|---|
| `version` | Versión de este formato; hoy solo `1` | **Nuevo** |
| `funcion_host` | La invocación que el rol autorizó: contrato, función y argumentos | La arma `signer-kit/hu01.py:76-80` (contrato `:77`, función `:78`, argumentos `:79`) y, en forma genérica, `signer-kit/passkey.py:77`. Es el `host_function` de la operación de la transacción |
| `entradas` | Entradas de autorización firmadas por el rol | Las firma `signer-kit/hu01.py:93` (clave clásica) o `signer-kit/passkey.py:68-71` (passkey). `signer-kit/hu01.py:150` ya las serializa en base64, una por línea |

El rol no viaja aparte: se lee de las credenciales de la entrada, igual que el verificador
(`verifier/conformidad.py:30-32` y `:49`).

## 3. Respuesta

### Aceptada (o fallida en la red)

```json
{
  "estado": "aceptada",
  "rol": "GA73IU5SLHFAV3MTNQKNXU5A65YCZMGC4ZWR7AR65VWP4QYTHXCT277V",
  "contrato": "CDGCV3TDCJCKR3LO3V6ACWVC4PIHIKJJOF5COR5VJTO6RDLVZ4TSBL27",
  "funcion": "registrar",
  "xdr_publicado": "publicadas/<solicitud_sha256>.xdr",
  "comision_estimada_stroops": 23824,
  "transaccion": {
    "estado": "SUCCESS",
    "hash": "8ba16039…7e5f",
    "enlace": "https://stellar.expert/explorer/testnet/tx/8ba16039…7e5f",
    "transmite_y_paga": "GDDZ3HMMIJWNP3MCM7NXZ325NYYCSFWPQ6SZIHMUVHSF73CJHKEUUQKM",
    "comision_stroops": 13677,
    "ledger": 5026465
  }
}
```

Si la red confirma la transacción con error, `estado` es `"fallida"` y `transaccion.estado` trae el
estado que devolvió la red. La comisión igual se cobra y se registra.

| Campo | De dónde sale hoy |
|---|---|
| `rol` | `verifier/conformidad.py:49`; valor de ejemplo en `evidence/hu01/evidencia.json:3` |
| `contrato`, `funcion` | `signer-kit/hu01.py:77-78`; valor de ejemplo en `evidence/hu01/evidencia.json:2` |
| `xdr_publicado` | Formato de `signer-kit/hu01.py:149-150`; ruta **nueva** |
| `comision_estimada_stroops` | Comisión de la transacción preparada (`signer-kit/hu01.py:99`); campo **nuevo** |
| `transaccion.*` | Mismos nombres que `signer-kit/hu01.py:117-122` y `evidence/hu01/evidencia.json:11-16` |

### Rechazada

```json
{
  "estado": "rechazada",
  "codigo": "FUNCION_NO_PERMITIDA",
  "motivo": "La función registrar no está permitida para el contrato CDGC…BL27",
  "detalle": {"contrato": "CDGC…BL27", "funcion": "registrar", "permitidas": ["rotar"]}
}
```

Una solicitud rechazada no publica XDR, no se transmite y no suma al consumo del rol.

## 4. Códigos de rechazo y orden de evaluación

El relayer evalúa en este orden y se detiene en el primer rechazo. Las cinco primeras
comprobaciones no usan la red. Las tres siguientes la usan solo a través de `red`, que en las
pruebas es un doble: por eso todas las pruebas corren sin conexión.

| Orden | Código | Motivo | `detalle` | Usa la red |
|---|---|---|---|---|
| 1 | `ENTRADA_INVALIDA` | La solicitud no cumple el formato (ver razones abajo) | `razon` | No |
| 2 | `CONTRATO_NO_PERMITIDO` | El contrato invocado no está en `permitidos` | `contrato` | No |
| 3 | `FUNCION_NO_PERMITIDA` | El contrato está permitido, la función no | `contrato`, `funcion`, `permitidas` | No |
| 4 | `ROL_NO_PERMITIDO` | El rol que firmó no está en `roles`, así que no tiene tope asignado | `rol` | No |
| 5 | `LIMITE_DE_FRECUENCIA` | El rol ya alcanzó `max_solicitudes` dentro del período | `solicitudes_en_periodo`, `max_solicitudes`, `periodo_segundos` | No |
| 6 | `ENTRADA_INVALIDA` | La firma ya venció o vence más allá de `vigencia_maxima_ledgers` | `razon`, `vence_en_ledgers` | Sí: `ultimo_ledger()` |
| 7 | `COMISION_EXCESIVA` | La comisión estimada supera `comision_maxima_stroops` | `comision_estimada_stroops`, `comision_maxima_stroops` | Sí: `estimar_comision()` |
| 8 | `TOPE_DE_GASTO` | Lo consumido en el período más la comisión estimada supera `tope_stroops` del rol | `consumido_stroops`, `comision_estimada_stroops`, `tope_stroops`, `periodo_segundos` | Sí: usa la estimación anterior |

`ROL_NO_PERMITIDO` no estaba en la lista original de códigos. Se agrega porque el tope es por rol y
un rol sin entrada en la política no tiene tope contra el cual comparar.

Razones de `ENTRADA_INVALIDA`:

| `razon` | Qué se comprobó | Antecedente en el código actual |
|---|---|---|
| `formato` | Falta un campo, `version` no es `1` o un XDR no se decodifica | **Nuevo** |
| `funcion_host_no_invocacion` | La función de host no es una invocación de contrato (crear contrato o subir WASM no se pagan) | **Nuevo**. OpenZeppelin Relayer hace el mismo rechazo (ver `docs/diferenciacion.md`) |
| `sin_autorizacion_de_rol` | Ninguna entrada trae credenciales de dirección | `verifier/conformidad.py:47-48` descarta las entradas sin credenciales de dirección; C3 exige que el rol no sea quien envía (`:54`) |
| `mas_de_un_rol` | Las entradas vienen de más de un rol; esta versión admite uno solo | **Nuevo** |
| `invocacion_distinta` | La invocación firmada en la entrada no coincide con `funcion_host` | **Nuevo** |
| `sin_firma` | La firma de la entrada está vacía | `verifier/conformidad.py:50` (C4) |
| `vencida` o `vigencia_excesiva` | `vence_en_ledgers <= 0` o mayor que `vigencia_maxima_ledgers` | `verifier/conformidad.py:51` y `:56` (C5); hoy el kit firma con 300 ledgers (`signer-kit/hu01.py:27-28`) |

El relayer no verifica la firma criptográfica de la entrada: lo hace la red al simular y al
ejecutar, también para las cuentas de contrato con passkey (`contracts/cuenta-passkey`).

## 5. Archivo de política

```json
{
  "version": 1,
  "red": "testnet",
  "periodo_segundos": 86400,
  "vigencia_maxima_ledgers": 720,
  "comision_maxima_stroops": 50000,
  "permitidos": [
    {"contrato": "CDGCV3TDCJCKR3LO3V6ACWVC4PIHIKJJOF5COR5VJTO6RDLVZ4TSBL27", "funciones": ["registrar"]}
  ],
  "roles": {
    "GA73IU5SLHFAV3MTNQKNXU5A65YCZMGC4ZWR7AR65VWP4QYTHXCT277V": {"tope_stroops": 300000, "max_solicitudes": 20}
  }
}
```

| Campo | Qué es | De dónde sale hoy |
|---|---|---|
| `version` | Versión del formato | **Nuevo** |
| `red` | Red a la que se envía; define RPC y passphrase | `signer-kit/hu01.py:23-24` (testnet fija hoy) |
| `periodo_segundos` | Ventana móvil hacia atrás desde `reloj()` para el tope y la frecuencia | **Nuevo** |
| `vigencia_maxima_ledgers` | Plazo máximo aceptado para la firma de la entrada | `verifier/conformidad.py:27` (720) |
| `comision_maxima_stroops` | Tope por transacción, comparado con la comisión estimada | **Nuevo**. Las comisiones cobradas en testnet van de 10 097 a 17 316 stroops (`evidence/transacciones.md:22-24`, `:57-60`). La estimada es mayor que la cobrada: en CA-01-1 la transacción preparada fijó 23 824 stroops como máximo (`verifier/datos_prueba/conforme.xdr`) y la red cobró 13 677 |
| `permitidos[].contrato` | Contrato permitido | Valor de ejemplo: `evidence/hu01/evidencia.json:2` |
| `permitidos[].funciones` | Funciones permitidas de ese contrato | Valor de ejemplo: `signer-kit/hu01.py:78` |
| `roles` | Mapa de dirección del rol a sus límites | Dirección de ejemplo: `evidence/hu01/evidencia.json:3`. Las cuentas de contrato con passkey usan su dirección `C…` (`evidence/transacciones.md`, sección de passkey) |
| `roles.*.tope_stroops` | Gasto máximo del rol en el período | **Nuevo** |
| `roles.*.max_solicitudes` | Transacciones máximas del rol en el período | **Nuevo** |

La política no contiene claves. La del operador llega por `--operador`.

## 6. Registros

Los tres viven bajo la carpeta `registro`. Los dos primeros son JSON Lines: un objeto por línea,
solo se agregan líneas, nunca se reescriben.

### `comisiones.jsonl`

Una línea por cada transacción enviada, aceptada o fallida. Es la fuente del consumo y de la
frecuencia de cada rol, y lo que lee el verificador de conformidad (pieza 3).

```json
{"fecha": "2026-11-10T15:00:00Z", "rol": "GA73…277V", "contrato": "CDGC…BL27", "funcion": "registrar", "solicitud_sha256": "…", "entradas_sha256": ["…"], "xdr_publicado": "publicadas/….xdr", "comision_estimada_stroops": 23824, "estado": "SUCCESS", "hash": "8ba16039…7e5f", "enlace": "https://stellar.expert/explorer/testnet/tx/8ba16039…7e5f", "transmite_y_paga": "GDDZ…UQKM", "comision_stroops": 13677, "ledger": 5026465}
```

| Campo | De dónde sale hoy |
|---|---|
| `fecha` | `reloj()` en ISO 8601 UTC con la forma `AAAA-MM-DDTHH:MM:SSZ`; **nuevo** (las evidencias actuales anotan la fecha a mano en `evidence/transacciones.md`) |
| `rol`, `contrato`, `funcion` | Ver sección 3 |
| `solicitud_sha256` | SHA-256 en hexadecimal de `funcion_host` y las `entradas`, unidos por saltos de línea; **nuevo**, mismo uso de `hashlib` que `signer-kit/hu01.py:12` y `:133` |
| `entradas_sha256` | SHA-256 de cada entrada en XDR: enlaza la comisión con la entrada que la originó (`docs/statement-of-work.md:119`); **nuevo** |
| `xdr_publicado` | Ver sección 3 |
| `comision_estimada_stroops` | Ver sección 3 |
| `estado`, `hash`, `enlace`, `transmite_y_paga`, `comision_stroops`, `ledger` | `signer-kit/hu01.py:117-122`; mismos nombres que `evidence/hu01/evidencia.json:11-16`. El verificador toma `hash` (`verifier/conformidad.py:76`) |

Consumo del rol en el período: suma de `comision_stroops` de sus líneas con `fecha` dentro de la
ventana. Frecuencia: cantidad de esas líneas.

### `rechazos.jsonl`

Una línea por cada solicitud rechazada.

```json
{"fecha": "2026-11-10T15:00:00Z", "codigo": "CONTRATO_NO_PERMITIDO", "motivo": "…", "solicitud_sha256": "…", "rol": "GA73…277V", "contrato": "CDGC…BL27", "funcion": "registrar", "detalle": {"contrato": "CDGC…BL27"}}
```

`rol`, `contrato` y `funcion` van en `null` cuando la solicitud no llegó a decodificarse. Todo el
archivo es **nuevo**: hoy el kit no registra rechazos (`signer-kit/README.md:16-17`).

### `publicadas/<solicitud_sha256>.xdr`

Las entradas firmadas, una por línea en base64, escritas antes de transmitir
(`docs/statement-of-work.md:120`). Mismo formato que `signer-kit/hu01.py:149-150`. Cualquier
tercero puede transmitirlas, como en CA-01-2 (`evidence/transacciones.md:23`).

## 7. Pruebas

`signer-kit/test_relayer.py` contiene las tres pruebas de rechazo que pide el SOW
(`docs/statement-of-work.md:128`): contrato no permitido, función no permitida y tope de gasto
superado. Usan como solicitud la invocación real de CA-01-1 guardada en
`verifier/datos_prueba/conforme.xdr` y un doble de `red`; ninguna toca la red. Comprueban el código
de rechazo, que no se transmitió ni se publicó nada, la línea agregada a `rechazos.jsonl` y, en las
dos primeras, que no se llamó a la red. El CI las corre en el job `contrato-de-datos`.

Mientras `signer-kit/relayer.py` no exista, las tres están marcadas con
`@unittest.expectedFailure` y el CI sigue en verde. Cuando el relayer las haga pasar, unittest las
reporta como "unexpected success" y el CI falla: es la señal para quitar la marca. Una cuarta
prueba, sin marca, comprueba que la solicitud de prueba se arma bien, para que las otras tres no
fallen por un error propio.
