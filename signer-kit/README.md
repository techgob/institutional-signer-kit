# Signer Kit

El componente. La prueba de concepto de HU-01 está en `hu01.py`; el empaquetado como v1 lo financia la instaward.

Dos piezas:

- `sign-auth-entry`: la clave de rol firma la entrada de autorización de una invocación específica, sin ser origen de la transacción ni pagar comisión.
- `relayer`: el operador recibe la entrada firmada, la inyecta en una transacción de la que es origen, paga la comisión y la transmite. Solo acepta invocaciones a contratos y funciones autorizados, con tope de gasto.

Criterios de aceptación en `../planning/sprint_S00_preparacion_postulacion.json`, historia HU-01.

## HU-01: prueba de concepto

`hu01.py` ejecuta en testnet los tres criterios de HU-01 contra el contrato de ejemplo de
`../contracts/ejemplo`. Las dos piezas existen como funciones: `entrada_firmada` es
`sign-auth-entry` y `transmitir` es el `relayer`. El relayer con lista permitida, tope de gasto y
límite de frecuencia está en `relayer.py` (sección "Relayer con política restringida" más abajo).

```sh
cd contracts/ejemplo && cargo test && stellar contract build && cd ../..
stellar keys generate tg-operador --network testnet --fund
stellar keys generate tg-tercero --network testnet --fund
stellar keys generate tg-rol            # sin fondos: el script crea la cuenta con saldo 0
stellar contract deploy --wasm contracts/ejemplo/target/wasm32v1-none/release/ejemplo.wasm   --source-account tg-operador --network testnet
pip install -r signer-kit/requirements.txt
python signer-kit/hu01.py <contract_id>
```

El script lee las claves de la CLI de Stellar y no las escribe en ningún archivo. Deja la entrada
publicada en `signer-kit/salida/autorizacion_B.xdr` y el resumen en `signer-kit/salida/evidencia.json`.
La corrida registrada está en `../evidence/transacciones.md` y `../evidence/hu01/`.

### Una clave sin cuenta no puede autorizar

Una dirección clásica que no existe en el ledger falla al autenticar
(`Error(Auth, InvalidAction)`, "trying to get non-existing value for account"). El script usa una
solución nativa de Stellar: el operador crea la cuenta del rol con saldo inicial 0 y patrocina su
reserva mínima (`BeginSponsoringFutureReserves`). El rol firma esa creación una vez y nunca recibe
ni guarda XLM. La alternativa sería una cuenta de contrato, que no necesita cuenta clásica.

### Por qué hay dos entradas

El nonce de cada entrada de autorización la hace de un solo uso. Si el operador ya transmitió
una entrada, un tercero no puede transmitir la misma: la red la rechaza. Por eso la corrida usa
dos entradas firmadas por el rol para la misma invocación, con nonces distintos. La A la transmite el operador (CA-01-1), la B se publica como
XDR y la transmite un tercero (CA-01-2), y el reenvío de A es el que la red rechaza (CA-01-3).

## Traspaso de operador

`traspaso.py` cambia el operador que paga sin tocar el contrato ni la clave del rol. El operador
entrante pasa a patrocinar la reserva de la cuenta del rol en una transacción que firman los dos
(el saliente revoca su patrocinio dentro de `BeginSponsoringFutureReserves` del entrante). Después
el rol firma y el entrante transmite y paga.

```sh
stellar keys generate tg-operador2 --network testnet --fund
python signer-kit/traspaso.py <contract_id> tg-operador tg-operador2
```

Del lado del operador, el traspaso es eso: una cuenta propia con fondos, el kit apuntando a ella y
esa transacción. Si el operador saliente desaparece sin firmar, la cuenta del rol sigue
funcionando; su reserva solo queda patrocinada por él. El contrato no lleva una lista de pagadores:
cualquier cuenta puede pagar, y por eso un tercero puede transmitir si el operador falla.

## Rotación por ciclo con passkey

`passkey.py` usa como rol una cuenta de contrato (`../contracts/cuenta-passkey`) controlada por una
passkey P-256 en formato WebAuthn. La dirección de la cuenta es la identidad del rol en el registro
y no cambia; la passkey se rota al cerrar cada ciclo. Esta cuenta no necesita cuenta clásica ni
reserva.

```sh
cd contracts/cuenta-passkey && cargo test && stellar contract build && cd ../..
python signer-kit/passkey.py <contract_id> tg-operador2
```

El script despliega la cuenta con la passkey del ciclo 1, registra, rota a la del ciclo 2, deja en
la red el rechazo de la passkey vieja y registra con la nueva. Las passkeys se generan en software
y quedan en `signer-kit/salida/passkeys/`, que no se versiona. Falta probar la ceremonia con un
autenticador real en el navegador.

## Relayer con política restringida

`relayer.py` recibe la invocación que autorizó un rol, la compara con un archivo de política y, si
pasa, publica las entradas como XDR, firma como origen, paga y transmite. La interfaz, los códigos
de rechazo y el formato de la política y de los registros están en `../docs/pieza2-interfaz.md`.

```sh
python signer-kit/relayer.py --politica politica.json --registro registro/ --operador tg-operador solicitud.json
```

La solicitud lleva la función de host y las entradas firmadas en XDR (sección 2 de la interfaz).
Cada envío queda en `registro/comisiones.jsonl`, cada rechazo en `registro/rechazos.jsonl` y las
entradas transmitidas en `registro/publicadas/`. Para revisar una transacción enviada, pasa su
`hash` a `../verifier/conformidad.py`.

`test_relayer.py` prueba sin red, sobre la invocación real de CA-01-1 y con un doble de la red, los
rechazos por contrato, función, rol, frecuencia, firma vencida, comisión estimada y tope de gasto,
y un caso aceptado. La corrida en testnet del 7 de octubre de 2026 (R-1 a R-3) está en
`../evidence/transacciones.md`.

Límites de esta versión:

- Solo testnet, y envía en serie: sin envío en paralelo ni reintentos con fee-bump.
- Una solicitud admite entradas de un solo rol. La política se aplica a la invocación raíz; las
  subinvocaciones que el rol autorice dentro de ella no se revisan.
- Si la transacción se envía pero la confirmación no llega en 60 segundos (`esperar` de `hu01.py`),
  el comando sale con código 1, el mensaje de error trae el hash y la comisión no queda en
  `comisiones.jsonl`: hay que agregarla a mano después de confirmarla.
- No hay todavía un `sign-auth-entry` genérico: para armar una solicitud hay que firmar la entrada
  como lo hacen `hu01.py` o `passkey.py` y serializar la función de host y la entrada en base64.

## Usarlo con un contrato propio

El contrato tiene que exigir la firma del rol con `rol.require_auth()` en la función que se
invoca, como hace `../contracts/ejemplo`. Hoy los tres scripts invocan `registrar(rol, huella)`;
para otra función hay que cambiar el nombre y los argumentos en `invocacion`. Generalizarlo es
parte del empaquetado como v1. El relayer ya acepta cualquier contrato y función que la política
permita.

Para comprobar que tus transacciones cumplen lo que el kit promete, pásalas por
`../verifier/conformidad.py` (ver `../verifier/README.md`).
