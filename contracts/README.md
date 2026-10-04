[README.md](https://github.com/user-attachments/files/32424497/README.md)

# Contratos Soroban

Pendiente. Lo financia la instaward.

Contrato de génesis del ciclo con tres guardas:

- **G1**: sin ordenanza registrada no existe ciclo, y ninguna transición posterior es posible.
- **G2**: la clave del ciclo combina código de ubicación geográfica, número de norma y año fiscal. Dos municipalidades distintas emiten ordenanzas con el mismo número el mismo año.
- **G6**: el contrato calcula si un registro es retroactivo comparando la fecha declarada del acto con la marca de tiempo del ledger, en lugar de confiar en el dato enviado.

La decisión de usar contratos, y lo que cuesta, está en `../docs/adr-001-contratos-soroban.md`.

## `ejemplo/`

Contrato mínimo para la prueba de HU-01, ajeno al registro del ciclo. Su única función,
`registrar(rol, huella)`, exige la firma del rol (`require_auth`) y emite un evento con la huella.
Sirve para demostrar que el rol autoriza y otra cuenta paga. Se compila con
`cargo test && stellar contract build` desde esa carpeta.
