# Transacciones en testnet

Cada afirmación técnica de este repositorio debe poder comprobarse en un explorador. Esta tabla se completa a medida que se ejecuta.

| # | Qué demuestra | Red | Hash de la transacción | Enlace | Fecha |
|---|---|---|---|---|---|
| 1 | Una clave de rol sin saldo firma la autorización de una invocación; una cuenta distinta paga la comisión y transmite | testnet | `43a023a8…8dfb` | [stellar.expert](https://stellar.expert/explorer/testnet/tx/43a023a86b5e1c2080c9b287c50d7ffd740f8770a121d8ab6746797a8baa8dfb) | 2026-10-03 |
| 2 | Una autorización firmada por el rol y publicada como XDR, transmitida por un tercero distinto del operador | testnet | `3494c854…236d` | [stellar.expert](https://stellar.expert/explorer/testnet/tx/3494c8549398be7a24e0765d27e2479c42d8e289cbcd033867f229e56a02236d) | 2026-10-03 |
| 3 | Apertura del ciclo del presupuesto participativo 2027 de Tocache | testnet | `[pendiente]` | `[pendiente]` | `[pendiente]` |
| 4 | Rechazo de un ciclo duplicado con la misma clave de ubigeo, número y año | testnet | `[pendiente]` | `[pendiente]` | `[pendiente]` |

## Detalle de HU-01

Corrida de `signer-kit/hu01.py` contra el contrato de ejemplo
[`CDGCV3TD…BL27`](https://stellar.expert/explorer/testnet/contract/CDGCV3TDCJCKR3LO3V6ACWVC4PIHIKJJOF5COR5VJTO6RDLVZ4TSBL27).
El resumen que generó el script está en `hu01/evidencia.json` y la entrada B publicada en
`hu01/autorizacion_B.xdr`.

| Paso | Qué demuestra | Resultado | Transacción | Comisión |
|---|---|---|---|---|
| 0 | El operador crea la cuenta del rol con saldo 0 y patrocina su reserva | éxito | [`9dd4146f…5e5f`](https://stellar.expert/explorer/testnet/tx/9dd4146fe5a3cee9985a87b5618159965087a55aae53ebbfaa9b2ee3918c5e5f) | la paga el operador |
| CA-01-1 (fila 1) | El rol firma la entrada A; el operador la transmite y paga | éxito | [`43a023a8…8dfb`](https://stellar.expert/explorer/testnet/tx/43a023a86b5e1c2080c9b287c50d7ffd740f8770a121d8ab6746797a8baa8dfb) | 13 672 stroops, operador |
| CA-01-2 (fila 2) | El rol firma la entrada B y la publica como XDR; un tercero la transmite y paga | éxito | [`3494c854…236d`](https://stellar.expert/explorer/testnet/tx/3494c8549398be7a24e0765d27e2479c42d8e289cbcd033867f229e56a02236d) | 13 672 stroops, tercero |
| CA-01-3 | El tercero reenvía la entrada A ya usada | rechazada: `nonce already exists for address` | [`2b777c4a…4503`](https://stellar.expert/explorer/testnet/tx/2b777c4a056607b62a72f1219c749f0368dc209243754aed25ebe3d28da04503) | 10 097 stroops, tercero |

Saldo XLM del rol al terminar la corrida: 0.

CA-01-2 usa una entrada distinta de CA-01-1 porque el nonce hace cada entrada de un solo uso.
La explicación está en `../signer-kit/README.md`.

## Nota sobre la permanencia de estos enlaces

La red de pruebas de Stellar se reinicia una vez por trimestre y borra todos los datos. Si un enlace de esta tabla deja de resolver, el script de reproducción permite regenerar la transacción en minutos. Por eso se registra también la fecha: un enlace caído después de un reinicio anunciado no invalida la evidencia, solo exige rehacerla.

## Cuentas usadas

| Rol | Clave pública | Función |
|---|---|---|
| Rol institucional (corrida de HU-01) | `GA73IU5SLHFAV3MTNQKNXU5A65YCZMGC4ZWR7AR65VWP4QYTHXCT277V` | Firma la autorización. Saldo: cero, reserva patrocinada por el operador |
| Operador | `GDDZ3HMMIJWNP3MCM7NXZ325NYYCSFWPQ6SZIHMUVHSF73CJHKEUUQKM` | Paga la comisión y transmite |
| Tercero | `GAJOFFTN767ZGII3NT6YKBKWEIF3XIMGPSSORZK6HMKVZSEJ3XZ7DZUS` | Retransmite la autorización firmada |

Ninguna clave privada se versiona en este repositorio.
