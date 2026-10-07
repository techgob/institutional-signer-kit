# Revisión de la postulación, como la leería un evaluador del capítulo

Revisión del 7 de octubre de 2026 sobre `docs/statement-of-work.md`, `docs/diferenciacion.md` y el
`README.md`, en el estado de la rama del PR #11 (commit `2e0034c`). Las reglas citadas están
resumidas en `docs/instawards-reglas.md`. Es una lectura crítica hecha a propósito: no reemplaza la
opinión del Chapter Lead.

Los puntos van ordenados por gravedad. Primero lo que impide postular, después lo que con más
probabilidad lleva a un rechazo o a un recorte, y al final lo que debilita la postulación sin
bloquearla.

## Con qué se compara

Proyectos que recibieron Instawards según Raven (Lumenloop). Las fechas son las de registro en
Lumenloop.

| Proyecto | Qué hizo en el sprint | Fuente |
|---|---|---|
| ArcusX (Chile) | Marketplace de trabajos con pago en USDC retenido. Empezó con 70 usuarios y 20 tareas publicadas; en la semana 2 pasaba los 300 miembros. Metas por semana y avances presentados en sesiones públicas | Videos del canal de Tellus Cooperative, [inicio](https://www.youtube.com/watch?v=H9N3xA8eRII) (4 de mayo de 2026) y [sesión 3](https://www.youtube.com/watch?v=eh6VoTKQaj8) (25 de mayo de 2026) |
| SozuPay (Chile) | En cuatro semanas, una prueba de concepto completa: panel para una ONG, Stellar Disbursement Platform, billeteras con passkeys, SEP-10 y SEP-24, y cuentas inteligentes con delegación de comisiones. ONG piloto: Mujeres 2000 | [blog.telluscoop.com](https://blog.telluscoop.com/p/instawards-stellar-chile-sozupay) (4 de junio de 2026), según el resumen de Lumenloop |
| Cohorte de julio en Türkiye | 13 proyectos con USD 5 000 cada uno; cada uno despliega una aplicación con contrato Soroban dirigida a un problema puntual | [Artículo](https://x.com/i/article/2084575817380630528) (4 de agosto de 2026) |
| Segunda cohorte en Türkiye | 10 proyectos, USD 50 000 en total | [Artículo](https://x.com/i/article/2089650839166042112) (18 de agosto de 2026) |

En todos se repite lo mismo: un solo producto, un entregable que se puede mostrar al cierre y un
avance visible dentro del capítulo semana a semana.

## Los cinco puntos más débiles

### 1. No hay capítulo ni Chapter Lead (bloquea la postulación)

**Qué se ve.** El SOW deja en "[por confirmar]" el contacto, el capítulo y el Chapter Lead
(`docs/statement-of-work.md:16-18`). El plan marca el referido como "por_solicitar" (DEP-01).

**Por qué pesa.** Instawards no tiene postulación abierta. La oportunidad la abre un Chapter Lead,
la postulación tiene que nombrarlo y se exige participación activa en el capítulo: "goes beyond
joining a Discord or attending a single event" (reglas de Instawards, secciones 1, 4 y 7). Los dos
receptores chilenos llegaron con un recorrido previo dentro del programa de Tellus Cooperative, con
sesiones públicas de avance.

**Qué cambiar.**
- Entrar ya al capítulo que corresponda. Para Chile, las señales están en
  `docs/instawards-capitulo.md`; hay una llamada comunitaria de Stellar Chile el 9 de octubre.
- Mostrar la demo en una actividad del capítulo y revisar el alcance con el Chapter Lead antes de
  enviar nada. Es el paso 2 del proceso oficial.
- Agregar al SOW una fila "Participación en el capítulo", con fechas y enlaces, y completar los tres
  campos pendientes.
- Hasta que esto exista, la fecha de inicio del 2 de noviembre (`:25`) no es realista.

### 2. El alcance no corresponde a USD 5 000 ni a 30 días

**Qué se ve.**
- Cuatro entregables y 190 horas (`:238`): kit empaquetado, contrato con seis guardas, ingesta de
  seis ciclos de dos municipalidades, trabajo de campo, verificador ciudadano en vivo y una nota
  para mainnet (`:113-215`).
- Varios criterios de aceptación dependen de terceros, como requerimientos firmados por dos oficinas
  municipales y documentos que todavía hay que pedir (`:189`, `:411`).
- La siguiente iteración se plantea por USD 8 000 (`:381`).

**Por qué pesa.**
- Las reglas piden "a scope that matches the requested award amount", que se pueda cumplir en 30
  días y que el avance se mida contra entregables acordados (secciones 5 y 6).
- Los receptores comparables cierran un solo producto en el sprint.
- El premio siguiente no es una iteración de USD 8 000: son hasta dos premios más, con un tope
  acumulado de USD 15 000 (secciones 6 y 8).
- El trabajo de campo (USD 600) no aparece entre los usos que SDF mencionó en su taller:
  infraestructura y prototipos.

**Qué cambiar.**
- **Primer sprint, USD 5 000:** que sea el plan B que el propio SOW ya tiene (`:294`): E1 más T0 a
  T4 con G1, G2, G6 y G7, el certificado de hito y la apertura real del ciclo de Tocache en testnet.
  Todo eso se puede verificar al cierre y no depende de terceros.
- **Dos sprints siguientes:** ingesta e investigación de usuario (E3) y verificador ciudadano con
  medición de comisiones (E4). Así la sección 7 calza con el tope de USD 15 000.
- **Trabajo de campo:** sacarlo del primer presupuesto, o confirmar con el Chapter Lead que se acepta.

### 3. El SOW no refleja lo que ya está en el repositorio

**Qué se ve.**
- El SOW dice que la pieza 2 "no está implementada" y que "lo financia esta instaward" (`:50`, `:118`,
  `:397`, `:436`). El recorrido muestra lo mismo (`demo/index.html:568`).
- Pero la rama del PR #11 ya tiene `signer-kit/relayer.py` y nueve pruebas que pasan.
- El plan S00 se propuso no adelantar trabajo que debía financiar la instaward
  (`planning/sprint_S00_preparacion_postulacion.json:58`).
- Hay otras diferencias:
  - El SOW cubre hasta T8 y el plan llega a T9.
  - El riesgo de "reinicio trimestral de testnet" (`:413`) no coincide con la documentación oficial,
    que da 2 a 4 reinicios al año. El próximo es el 16 de diciembre, después del cierre del sprint
    el 4 de diciembre.

**Por qué pesa.** La definición de terminado del propio SOW exige que cada enlace muestre lo que el
texto afirma (`:374`). Un evaluador que abre el repositorio ve una parte del E1 ya hecha y puede
leerlo de dos formas: como un documento desactualizado o como una petición de fondos por trabajo
terminado.

**Qué cambiar.**
- Pasar la pieza 2 a "Punto de partida" como trabajo autofinanciado, con sus horas sumadas a las
  ~45 declaradas.
- Marcar "4 de 4 piezas" una vez hecha la corrida en testnet.
- Reasignar las horas de E1 a lo que sigue pendiente: `sign-auth-entry` genérico, empaquetado y
  guías.
- Actualizar la etiqueta del recorrido, decidir entre T8 y T9 y corregir la fila del riesgo de
  testnet.

### 4. La forma de pago y el reparto entre las partes no están resueltos

**Qué se ve.**
- El presupuesto está en USD con una tarifa fija de USD 20 por hora (`:238`).
- La postulante es TechGob SpA (`:14`) y el desarrollo lo hace otra persona (`:15`).
- El acuerdo de aportes es una plantilla sin firmar (`docs/acuerdo-aportes-y-distribucion.md`).

**Por qué pesa.**
- El premio se paga en XLM al precio del día programado para el pago, así que el monto en USD puede
  bajar entre la aprobación y el cobro.
- Antes de pagar, SDF exige KYC (sección 7).
- Una organización o un equipo postula con un solo representante, y las reglas no prevén repartir el
  pago entre dos partes (reglas generales, 1.1 y 1.2).
- Cuándo se paga lo define un plan acordado después de la aprobación, no el SOW.

**Qué cambiar.**
- Decidir quién postula (TechGob como organización, con el desarrollador como parte del equipo) y
  quién la representa.
- Firmar el acuerdo de aportes antes de enviar. Debe decir quién recibe el XLM, cuándo y a qué precio
  se convierte, y en qué plazo se paga a la otra parte.
- Tener listos los documentos de KYC (y de KYB, si postula TechGob).
- Agregar al SOW un riesgo de volatilidad del XLM, cubierto por la contingencia.

### 5. La validación y la diferencia con lo existente cuestan verificarlas

**Qué se ve.**
- Las municipalidades figuran como "contrapartes de validación en terreno" con acceso habilitado por
  la SGTD (`:23`), pero el repositorio no tiene una carta, un correo ni un acta que lo respalde.
- El dato de que Stellar fue la red recomendada en "2 de 23" casos es confidencial (`:77`).
- `docs/diferenciacion.md` no menciona a SozuPay, un receptor chileno que, según el resumen de
  Lumenloop, ya armó cuentas inteligentes con passkeys y delegación de comisiones.

**Por qué pesa.**
- Los receptores comparables muestran algo que el evaluador puede comprobar: usuarios (ArcusX) o una
  organización piloto con nombre (SozuPay).
- Un evaluador del capítulo chileno probablemente conoce SozuPay. Si el documento no lo menciona,
  parece que el equipo no revisó lo que ya existe en su propio capítulo.

**Qué cambiar.**
- Conseguir una confirmación por escrito, aunque sea un correo, del laboratorio de la SGTD o de una
  de las oficinas municipales, y enlazarla en el SOW.
- Publicar la parte no confidencial del análisis "2 de 23" o quitar la cifra.
- Agregar SozuPay a `docs/diferenciacion.md`, con lo que el kit hace distinto: claves por cargo y
  período, un operador con política restringida y rechazos registrados, y una cadena de evidencia
  hasta el acto administrativo que verifica un tercero.
- Comprometer avances semanales públicos dentro del capítulo, como hicieron los receptores chilenos.

## Lo que ya juega a favor

- Diez transacciones en testnet con evidencia reproducible, integración continua y pruebas que
  corren sin red.
- Un "fuera de alcance" explícito, una definición de terminado y un plan B ya escrito: con eso el
  recorte del punto 2 es fácil de hacer.
- Un problema concreto y documentado con fuentes oficiales de dos municipalidades reales.
