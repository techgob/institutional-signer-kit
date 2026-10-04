# Signer Kit

El componente. La prueba de concepto de HU-01 está en `hu01.py`; el empaquetado como v1 lo financia la instaward.

Dos piezas:

- `sign-auth-entry`: la clave de rol firma la entrada de autorización de una invocación específica, sin ser origen de la transacción ni pagar comisión.
- `relayer`: el operador recibe la entrada firmada, la inyecta en una transacción de la que es origen, paga la comisión y la transmite. Solo acepta invocaciones a contratos y funciones autorizados, con tope de gasto.

Criterios de aceptación en `../planning/sprint_S00_preparacion_postulacion.json`, historia HU-01.

## HU-01: prueba de concepto

`hu01.py` ejecuta en testnet los tres criterios de HU-01 contra el contrato de ejemplo de
`../contracts/ejemplo`. Las dos piezas existen como funciones: `entrada_firmada` es
`sign-auth-entry` y `transmitir` es el `relayer`. La lista de contratos y funciones permitidos y
el tope de gasto del relayer todavía no están implementados.

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
dos entradas firmadas por el rol. La A la transmite el operador (CA-01-1), la B se publica como
XDR y la transmite un tercero (CA-01-2), y el reenvío de A es el que la red rechaza (CA-01-3).
