# Transacciones en testnet

Cada afirmación técnica de este repositorio debe poder comprobarse en un explorador. Esta tabla se completa a medida que se ejecuta.

| # | Qué demuestra | Red | Hash de la transacción | Enlace | Fecha |
|---|---|---|---|---|---|
| 1 | Una clave de rol sin saldo firma la autorización de una invocación; una cuenta distinta paga la comisión y transmite | testnet | `8ba16039…7e5f` | [stellar.expert](https://stellar.expert/explorer/testnet/tx/8ba160396082e0ac29dc0324e96a119a90f99c2e9fd9a10aa2941746c14e7e5f) | 2026-10-04 |
| 2 | Una autorización firmada por el rol y publicada como XDR, transmitida por un tercero distinto del operador | testnet | `fb284c5b…b8dd` | [stellar.expert](https://stellar.expert/explorer/testnet/tx/fb284c5b28ce79738db571107c0f8ce0906fd7d48bb39b09e1282d0c2a64b8dd) | 2026-10-04 |
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
| CA-01-1 (fila 1) | El rol firma la entrada A; el operador la transmite y paga | éxito | [`8ba16039…7e5f`](https://stellar.expert/explorer/testnet/tx/8ba160396082e0ac29dc0324e96a119a90f99c2e9fd9a10aa2941746c14e7e5f) | 13 677 stroops, operador |
| CA-01-2 (fila 2) | El rol firma la entrada B para la misma invocación y la publica como XDR; un tercero la transmite y paga | éxito | [`fb284c5b…b8dd`](https://stellar.expert/explorer/testnet/tx/fb284c5b28ce79738db571107c0f8ce0906fd7d48bb39b09e1282d0c2a64b8dd) | 13 677 stroops, tercero |
| CA-01-3 | El tercero reenvía la entrada A ya usada | rechazada: `Error(Auth, ExistingValue)`, nonce consumido | [`ac8f406c…0542`](https://stellar.expert/explorer/testnet/tx/ac8f406c08dac361b07efffb92deae0cf9b85e2044ffa50f953137eb7a7f0542) | 10 097 stroops, tercero |

Saldo XLM del rol al terminar la corrida: 0.

A y B autorizan la misma invocación: mismo contrato, función y argumentos (la huella está en `hu01/evidencia.json`). Solo cambia el nonce, y por eso cada entrada sirve una vez.
La creación de la cuenta del rol (paso 0) es del 3 de octubre en hora de Lima, que el explorador muestra como 2026-10-04 04:13 UTC. Las demás transacciones son del 4 de octubre, entre las 23:18 y las 23:19 UTC.
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
