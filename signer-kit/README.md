# Signer Kit

El componente. Pendiente de implementación en el día 2 de la preparación.

Dos piezas:

- `sign-auth-entry`: la clave de rol firma la entrada de autorización de una invocación específica, sin ser origen de la transacción ni pagar comisión.
- `relayer`: el operador recibe la entrada firmada, la inyecta en una transacción de la que es origen, paga la comisión y la transmite. Solo acepta invocaciones a contratos y funciones autorizados, con tope de gasto.

Criterios de aceptación en `../planning/sprint_S00_preparacion_postulacion.json`, historia HU-01.
