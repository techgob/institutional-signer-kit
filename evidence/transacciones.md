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

## Traspaso de operador

Corrida de `signer-kit/traspaso.py` del 5 de octubre de 2026, mismo contrato y misma clave de rol
que HU-01. Un segundo operador asume el pago sin que cambie nada en el contrato ni en la clave del
rol. El resumen está en `operador/traspaso.json`.

| Paso | Qué demuestra | Resultado | Transacción | Comisión |
|---|---|---|---|---|
| T-1 | El operador entrante pasa a patrocinar la reserva de la cuenta del rol (el saliente revoca su patrocinio dentro de `BeginSponsoringFutureReserves` del entrante; firman los dos) | éxito | [`56d28359…f9c8`](https://stellar.expert/explorer/testnet/tx/56d283596d0dfc3d158b7de4c8eb034b1dba30c06659789ac800826434fcf9c8) | 300 stroops, operador entrante |
| T-2 | El rol firma y el operador entrante transmite y paga | éxito | [`60d81df7…3c97`](https://stellar.expert/explorer/testnet/tx/60d81df7b9b131b1fd919eebf5b79368d4486f39a9ed3fd0bcbeca4258333c97) | 13 673 stroops, operador entrante |

Patrocinador de la reserva del rol antes de T-1: `GDDZ3HMM…UQKM`. Después: `GCL4OWVD…6NKO`.
Si el operador saliente desaparece sin firmar T-1, la cuenta del rol sigue funcionando; su reserva
solo queda patrocinada por él.

## Rotación por ciclo con passkey

Corrida de `signer-kit/passkey.py` del 5 de octubre de 2026. El rol es la cuenta de contrato
[`CD7T3FZ4…MGUY`](https://stellar.expert/explorer/testnet/contract/CD7T3FZ4WBVNXTQKFDFEIZ5INVYNP6COK2J4VH47U6I6CHWU5X7NMGUY)
(`contracts/cuenta-passkey`), controlada por una passkey P-256 con formato WebAuthn. La dirección
queda fija en el registro y la passkey cambia de ciclo. Paga todo el operador entrante. El resumen
está en `passkey/passkey.json`.

| Paso | Qué demuestra | Resultado | Transacción | Comisión |
|---|---|---|---|---|
| P-1 | La passkey del ciclo 1 autoriza un registro | éxito | [`75ef39a5…5f64`](https://stellar.expert/explorer/testnet/tx/75ef39a5e718d1e689952af6e096f2e510baa25f359c5b96c9de275c5f2b5f64) | 15 061 stroops, operador |
| P-2 | La passkey del ciclo 1 autoriza la rotación a la del ciclo 2 | éxito | [`1afc57e3…8756`](https://stellar.expert/explorer/testnet/tx/1afc57e34014fc2bd49549d31604e5900e246253b382fbe6095afb7cd6ac8756) | 17 316 stroops, operador |
| P-3 | La passkey del ciclo 1 intenta otro registro | rechazada: `failed secp256r1 verification` en `__check_auth` | [`ab6e2d83…e8a6`](https://stellar.expert/explorer/testnet/tx/ab6e2d83df750351a050c2eb5f206474303b35c13b114c1a2d464b3fdc79e8a6) | 11 510 stroops, operador |
| P-4 | La passkey del ciclo 2 autoriza un registro con la misma dirección de rol | éxito | [`39dcbe88…7fb2`](https://stellar.expert/explorer/testnet/tx/39dcbe8820165d0f0048c32db3da41e61adb03dd50f8bb46901a07eaf95c7fb2) | 15 061 stroops, operador |

Las passkeys de esta corrida se generan en software con el mismo formato que entrega un
autenticador WebAuthn. Falta probar la ceremonia con un autenticador real en el navegador; lo que
ocurre en la red es lo mismo.

## Relayer con política restringida

Corrida de `signer-kit/relayer.py` del 7 de octubre de 2026, con `RedTestnet` y el operador
`tg-operador`. El rol `GA73…277V` firma una entrada nueva en cada solicitud y el relayer la compara
con la política antes de pagar. Los registros que dejó el relayer están en `relayer/`
(`comisiones.jsonl`, `rechazos.jsonl` y el XDR publicado antes de transmitir).

| Paso | Política | Resultado | Transacción | Comisión |
|---|---|---|---|---|
| R-1 | `registrar` permitida, tope 300 000 stroops | aceptada | [`544f62f8…dbb8`](https://stellar.expert/explorer/testnet/tx/544f62f8f97aa32284a3a59dd80a35ecbb28b6686a12dd2c6ecd1da37e18dbb8) | 13 666 stroops cobrados (23 811 estimados), operador |
| R-2 | solo `rotar` permitida | rechazada antes de tocar la red: `FUNCION_NO_PERMITIDA` | no se envía | 0 |
| R-3 | `registrar` permitida, tope 30 000 stroops | rechazada: `TOPE_DE_GASTO` (13 666 consumidos + 23 811 estimados) | no se envía | 0 |

R-1 dio conforme en `verifier/conformidad.py` (C1 a C6). Los rechazos no generan transacción: la
prueba es la línea de `relayer/rechazos.jsonl` y que el operador no pagó nada por ellos.

## Conformidad

`verifier/conformidad.py` revisa una transacción confirmada contra las propiedades del kit, sin
claves. Lo puede correr cualquier operador sobre sus propias transacciones. El 5 de octubre dieron
conforme CA-01-1, CA-01-2, T-2, P-1 y P-4, y el 7 de octubre R-1. T-1 y P-3 dieron no conforme, como corresponde.

## Nota sobre la permanencia de estos enlaces

La red de pruebas de Stellar se reinicia periódicamente y borra todos los datos. Si un enlace de esta tabla deja de resolver, el script de reproducción permite regenerar la transacción en minutos. Por eso se registra también la fecha: un enlace caído después de un reinicio anunciado no invalida la evidencia, solo exige rehacerla.

Según la documentación oficial, los reinicios de testnet suelen ocurrir de 2 a 4 veces por año, a
las 17:00 UTC, y se anuncian con al menos dos semanas de anticipación en el
[Stellar Dashboard](https://dashboard.stellar.org). **El próximo programado es el 16 de diciembre
de 2026** ([stellar/stellar-docs](https://github.com/stellar/stellar-docs), commit `7a90bb8e`,
`docs/networks/README.mdx:62-66`, consultado el 7 de octubre de 2026). Si el sprint empieza el 2 de
noviembre, termina antes de esa fecha, pero cualquier revisión posterior al 16 de diciembre
encontrará rotos los enlaces de esta página.

Lo que sobrevive al reinicio porque está en este repositorio: los resúmenes de cada corrida
(`hu01/evidencia.json`, `operador/traspaso.json`, `passkey/passkey.json`), con hashes, ledgers y
comisiones, y la entrada B publicada (`hu01/autorizacion_B.xdr`). Para repetir las corridas hay que
volver a desplegar antes los contratos que los scripts reciben como argumento.

## Cuentas usadas

| Rol | Clave pública | Función |
|---|---|---|
| Rol institucional (corrida de HU-01) | `GA73IU5SLHFAV3MTNQKNXU5A65YCZMGC4ZWR7AR65VWP4QYTHXCT277V` | Firma la autorización. Saldo: cero. Reserva patrocinada por el operador hasta T-1, desde entonces por el operador entrante |
| Operador (saliente desde T-1) | `GDDZ3HMMIJWNP3MCM7NXZ325NYYCSFWPQ6SZIHMUVHSF73CJHKEUUQKM` | Paga la comisión y transmite |
| Operador entrante | `GCL4OWVDZ6USNCOJS4VGXOEEISS3TXUMFF425D3IS6CJ4FUQFIG66NKO` | Paga y transmite desde T-1; paga la corrida de passkey |
| Tercero | `GAJOFFTN767ZGII3NT6YKBKWEIF3XIMGPSSORZK6HMKVZSEJ3XZ7DZUS` | Retransmite la autorización firmada |
| Rol con passkey | `CD7T3FZ4WBVNXTQKFDFEIZ5INVYNP6COK2J4VH47U6I6CHWU5X7NMGUY` | Cuenta de contrato; la autoriza la passkey del ciclo vigente |

Ninguna clave privada se versiona en este repositorio.
