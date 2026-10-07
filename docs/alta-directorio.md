# Alta del proyecto en los directorios del ecosistema

Consulta del 7 de octubre de 2026. A esa fecha el proyecto no figura en ninguno de los dos
directorios (Raven: `scout.resolveProject` sin coincidencias; `lumenloop.search_directory` solo
devolvió proyectos parecidos por similitud). Las rutas de abajo salen del código fuente de cada
directorio; no se pudo abrir ninguno de los dos sitios desde el entorno donde se hizo la consulta.

Ninguna de las dos altas se ha enviado. Ambas publican información del proyecto, así que las
decide el equipo.

## Lumenloop

Lumenloop mantiene su directorio en el repositorio público
[lumenloop/stellar-ecosystem-db](https://github.com/lumenloop/stellar-ecosystem-db), un archivo
YAML por proyecto en `projects/`. Referencias al commit `468b3ca5`:

- Se pide abriendo un issue o con un PR que agregue o modifique el YAML del proyecto en
  `projects/`; los cambios externos se importan por webhook (`README.md:107-112`).
- El YAML debe seguir el formato del README, con título, descripción, sitio y enlaces
  verificados, y el proyecto no puede girar solo en torno a un token
  (`CONTRIBUTING.md:27-39`).
- Proceso: fork, rama, PR con descripción clara; un mantenedor lo revisa (`CONTRIBUTING.md:50-64`).

Borrador de `projects/institutional-signer-kit.yaml`, con el mismo esquema que los archivos
existentes. Categoría y etiquetas son una propuesta: la categoría es una de las cinco que usa el
repositorio y las etiquetas salen del vocabulario de Lumenloop (`get_project_tags_vocabulary`).
Faltan redes sociales, porque el repositorio no las declara.

```yaml
title: Institutional Signer Kit
other_names: null
parent: null
description: Open-source kit that lets a public institution authorize Soroban contract calls without ever holding XLM. Signing keys belong to offices and terms, a separate account pays the fees, every fee is traceable to the signed authorization behind it, and signed authorizations can be submitted by any third party. Proven on testnet and validated against Peru's participatory budget process.
links:
  website:
    - signerkit.govtechpe.work
  blog: []
  x: []
  linkedin: []
  discord: []
  telegram: []
  youtube:
    - youtu.be/Pel8UScd8x4
  instagram: []
  reddit: []
  tiktok: []
  linktree: []
  github:
    - github.com/techgob/institutional-signer-kit
attributes:
  category: Developer Tooling
  tags:
    - Wallet Infra
  operating_region:
    - Latin America & Caribbean
  based_in: Chile
images: null
mainnet:
  audits: []
  tokens: []
```

La descripción omite a propósito el relayer con política restringida, porque todavía no está
implementado. Antes de enviarlo conviene confirmar el sitio web y si el video debe ir en
`youtube`, que en otros archivos apunta a un canal y no a un video.

## Stellar Light

Stellar Light tiene un formulario público en `/submit` (repositorio
[Stellar-Light/stellarlight](https://github.com/Stellar-Light/stellarlight), commit `e1f1ff1b`):

- Campos: nombre, sitio web, descripción corta, categoría y repositorios de GitHub
  (`src/app/(frontend)/submit/page.tsx:23-32`). La descripción debe tener entre 10 y 1000
  caracteres (`:40-46`).
- Categorías posibles: Infrastructure, Tooling, Partner Integration, User-Facing App, Asset,
  Protocol/Contract y Anchor (`:393-401`).
- El formulario envía a `/api/intake` (`:93`) y crea el proyecto como no verificado, pendiente de
  aprobación de un administrador (`:177`; `docs/COLLECTIONS.md:215-219`).

Stellar Light también importa proyectos desde el repositorio de Lumenloop mediante una
sincronización que lanza un administrador (`docs/COLLECTIONS.md:221-225`;
`src/app/api/sync/lumenloop/route.ts:72`). Con el alta en Lumenloop el proyecto podría llegar
también a Stellar Light, aunque no se sabe cada cuánto se corre esa sincronización.

## Orden sugerido

1. PR a Lumenloop con el YAML, que alimenta a los dos directorios.
2. Si en unos días no aparece en Stellar Light, el formulario `/submit`.
