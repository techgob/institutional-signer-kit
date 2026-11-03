# Statement of Work (SOW) — Instawards

## Institutional Signer Kit: firmar sin poseer — Compromiso acotado de 30 días

*Una institución pública firma en Stellar sin tener nunca XLM.*

---

## 1. Problema y objetivo

### El problema

Ninguna municipalidad peruana puede comprar, custodiar ni rendir cuentas de un criptoactivo solo para pagar comisiones de red. Hacerlo exige un proceso de contratación, una partida presupuestal, reglas de custodia de claves y rendición ante la Contraloría, y choca con el principio de unidad de caja del sistema de tesorería. El costo administrativo de habilitar el pago supera en órdenes de magnitud al pago mismo. Ahí mueren la mayoría de los pilotos de blockchain público, antes de discutir arquitectura.

El efecto se ve en carteras reales. En un taller conjunto con la SGTD, TechGob levantó 23 desafíos públicos de 25 entidades. En un documento de análisis de red para la implementación de prototipos producido por TechGob para la SGTD, este impedimento hizo que se prefirieran redes permisionadas porque no obligan a la entidad a tener un activo. Stellar (recomendada por sus capacidades nativas para 2 de 23 desafíos) no es descartable por razones técnicas y este proyecto habilita el componente necesario para que pueda competir con las otras redes. Además, entrega a la autoridad la prueba que mide el costo por transición y ciclo, junto a la documentación técnica de quién paga, quién firma y qué pasa si el operador desaparece. *(El análisis de portafolio es material de trabajo con la SGTD; puede exponerse al comité bajo acuerdo de confidencialidad.)*

El presupuesto participativo, que las municipalidades están mandatadas a desarrollar, muestra por qué falta esta pieza. Stellar ya puede responder **quién recibió** un pago. Nadie responde **quién decidió, con qué acto y bajo qué regla**. En las dos municipalidades piloto esa evidencia es un PDF escaneado sin integridad alguna (Tocache) y un decreto nativo digital con siete firmas válidas, pero sin sello de tiempo cualificado ni datos de validación de largo plazo (La Punta). A ninguna le falta capacidad de gasto. A las dos les falta una cadena de evidencia que conecte lo que los vecinos acordaron con lo que efectivamente se hizo.

Hoy no existe un componente reutilizable que permita a una entidad pública, a la vez:

- firmar con claves que pertenecen a cargos y períodos, como exige la Ley N.° 29733 de Protección de Datos Personales;
- delegar el pago de comisiones en un operador que **no puede** usar su rol de pagador para otra cosa;
- auditar cada comisión que pagó el operador;
- seguir operando si el operador desaparece o se niega a transmitir;
- lograr que la red rechace un paso administrativo que la norma no permite.

Las cuatro primeras condiciones están construidas y probadas. La quinta es el objeto de este sprint.

### Objetivo

En 30 días TechGob entregará en Stellar Testnet:

1. **Signer Kit v1** completo, empaquetado y documentado, con el relayer de política restringida corrido en testnet en sus cinco casos de rechazo y con `sign-auth-entry` generalizado a cualquier contrato y función;
2. el **registro del ciclo T0–T4** con las guardas G1, G2, G6 y G7, en el que un paso legal omitido falla en la red, más el **certificado de hito** demostrado con un contrato consumidor;
3. las **dos aperturas reales del ciclo en testnet**, una por municipalidad, con las dos variantes de génesis que la norma produce;
4. el **verificador en vivo y la medición de comisiones sobre T0–T4**, reproducibles por un tercero sin intervención de TechGob.

**Criterio de éxito:** dos claves de rol institucionales distintas, cada una con 0 XLM, abren y hacen avanzar hasta T4 dos ciclos legales reales; una transición que omite un paso es rechazada por la red; y un revisor externo reproduce huella, compromiso y comisión de al menos una transición por municipalidad usando solo el repositorio y el recorrido.

---

## 2. Información del proyecto y del equipo

| Campo | Valor |
|---|---|
| Nombre del proyecto | Institutional Signer Kit |
| Postulante | TECH GOB CONSULTORA EN TRANSFORMACIÓN DIGITAL Y TECNOLOGÍAS EMERGENTES SpA (TechGob), Chile |
| Builder / equipo | Nadinne Canto Novoa (@techgob) — dueña de producto (alcance, priorización y aceptación de entregables; máquina de estados derivada del marco normativo; contrato de datos; relación institucional) · Kevin Alexander Soto Burgos (@kasbsquall) — desarrollo (arquitectura técnica, implementación en Soroban, separación firmante-pagador, ingesta y verificador) |
| Contacto principal | Nadinne Canto |
| Capítulo de embajadores | [por confirmar] |
| Chapter Lead | [por confirmar] |
| Repositorio | https://github.com/techgob/institutional-signer-kit (Apache-2.0, con integración continua) |
| Recorrido interactivo | https://signerkit.govtechpe.work |
| Video de demostración | https://youtu.be/Pel8UScd8x4 (1:41) |
| Red | Stellar Testnet (Soroban) |
| Contrapartes de validación en terreno | Municipalidad Provincial de Tocache (San Martín) y Municipalidad Distrital de La Punta (Callao), Perú, con acceso habilitado por la Red Nacional de Laboratorios de Innovación Digital de la Secretaría de Gobierno y Transformación Digital (SGTD-PCM) |
| Fecha de postulación | Noviembre de 2026 |
| Inicio sugerido del sprint | 9 de noviembre de 2026, sujeto a la resolución y a la confirmación del Chapter Lead |
| Duración | 30 días (sprint de 4 semanas) |
| Monto solicitado | USD 5 000 |

---

## 3. Visión general e intención de la instaward

### 3.1 Propósito

Esta instaward pone a trabajar el **Institutional Signer Kit**, un componente abierto y reutilizable que permite a una institución pública autorizar invocaciones en Soroban con **saldo cero en XLM, sin partida presupuestal y sin custodia de activos**.

Soroban firma las entradas de autorización de forma independiente del sobre de la transacción, de modo que quien autoriza y quien paga la comisión pueden ser cuentas distintas. El kit empaqueta esa propiedad en cuatro piezas. **Las cuatro están construidas y con pruebas automatizadas que pasan.** La cuarta, el relayer con política restringida, se construyó con trabajo autofinanciado durante la ventana de postulación y no se carga a esta instaward.

Ese proceso administrativo es el ciclo del presupuesto participativo que la ley peruana hace obligatorio, modelado como máquina de estados a partir de documentos municipales reales de dos municipalidades. El resultado es el registro del ciclo que anuncia el cierre del video: un contrato en el que **una transición que se salta un paso legal es rechazada por la red**, y en el que cada paso cumplido produce un **certificado de hito, una precondición que un desembolso puede exigir**.

Con el kit ya construido, este sprint se concentra en el único bloque sin precedente ejecutado: las guardas del registro, sobre el primer tramo del ciclo (T0 a T4) y con las dos aperturas reales en testnet. Lo que sigue se postula como sprints posteriores, tal como las reglas del programa lo contemplan (sección 7).

### 3.2 Punto de partida: lo que ya es público y verificable

El sprint parte de evidencia que funciona. Todo lo que sigue está en el repositorio, en el recorrido interactivo o en el video, en el commit `e2d374e` o posterior.

**Las cuatro piezas del kit**

| Pieza | Estado hoy | Evidencia |
|---|---|---|
| 1. Firma por rol y ciclo: las claves pertenecen a cargos y períodos, no a personas | **Probada en testnet.** Cuenta clásica de rol con 0 XLM y reserva patrocinada; cuenta de contrato con passkey que rota por ciclo mientras la dirección del rol se mantiene | Corrida HU-01; corrida passkey P-1 a P-4 (`evidence/transacciones.md`) |
| 2. Relayer con política restringida: el pagador solo transmite invocaciones autorizadas, con tope de gasto y límite de frecuencia | **Construido, con nueve pruebas automatizadas que pasan en integración continua** (`signer-kit/test_relayer.py`): rechazo de contrato no permitido, función no permitida, rol fuera de política, límite de frecuencia, comisión estimada excesiva, firma vencida y tope de gasto, más el caso aceptado. **En testnet se corrieron tres de esos casos** (R-1 a R-3): una invocación permitida que el operador pagó, un rechazo por función y un rechazo por tope. **Lo que falta es correr en testnet el rechazo de contrato no permitido y el de límite de frecuencia**, que hoy están probados contra un doble de la red | PR #11; `signer-kit/test_relayer.py`; `evidence/transacciones.md`, sección "Relayer con política restringida"; registros crudos en `evidence/relayer/` |
| 3. Trazabilidad entre comisión y autorización: cada comisión queda enlazada a la entrada firmada que la originó | **Probada**, sin claves, sobre transacciones confirmadas (comprobaciones C1 a C6) | `verifier/conformidad.py`; R-1 dio conforme |
| 4. Autorización portátil: cualquier tercero puede transmitir una entrada publicada; el operador no puede censurar | **Probada en testnet**: la entrada B se publicó como XDR y la transmitió un tercero; el reenvío de la entrada A fue rechazado | tx `fb284c5b…b8dd`; tx `ac8f406c…0542` (`Error(Auth, ExistingValue)`) |

La distinción entre "probado en pruebas automatizadas" y "corrido en testnet" se mantiene en todo este documento, porque es la que un revisor puede comprobar por su cuenta. El relayer no toca la red para rechazar: por diseño, un rechazo se decide antes de estimar la comisión y no genera transacción, de modo que su evidencia es la línea de `evidence/relayer/rechazos.jsonl` y el hecho de que el operador no pagó nada.

**Transacciones registradas en testnet**

Trece en total: creación de la cuenta con reserva patrocinada, HU-01 (entrada A, entrada B y reenvío), traspaso de operador (T-1 y T-2), rotación con passkey (P-1 a P-4) y la corrida del relayer (R-1 a R-3). La invocación pagada por el relayer es `544f62f8…dbb8`, ledger 5 066 171, **13 666 stroops cobrados sobre 23 811 estimados**, con el rol en 0 XLM. El traspaso de operador ya es un cambio de configuración y no una migración: la clave del rol y el contrato no cambian.

**El registro del ciclo, especificado y probado fuera de la cadena**

| Activo | Estado hoy |
|---|---|
| Máquina de estados: 14 transiciones T0–T13 agrupadas en 8 hitos, guardas G1–G12, reglas de sustitución R1–R7 y dos variantes de génesis | Especificada (`docs/maquina-estados.md`); se recorre hito por hito en el recorrido interactivo |
| Guardas | **Especificadas, contrato no desplegado** |
| Contrato de datos con reglas de admisión por campo y validador en dos capas | 7 casos de prueba aprobados en integración continua, incluido el caso de dato personal que debe fallar |
| Contratos Soroban existentes (`ejemplo` y `cuenta-passkey`) | Con pruebas propias, que corren en integración continua desde el PR #11 |
| Ingesta contra un documento real | **Solo T0**: Ordenanza 001-2026-MPT de Tocache, resultado `observado` con 16 inconsistencias (una bloqueante, INC-01: la huella se calculó sobre una copia y no sobre la descarga directa del portal) |
| Verificador local (huella del PDF y compromiso canónico) | Funciona, con pruebas |
| Decisión de imponer las transiciones con contratos Soroban | ADR-001 aceptada |

### 3.3 Declaración de nivel de madurez

Esta sección existe para que el evaluador no tenga que inferirlo. El proyecto contiene dos objetos con madurez distinta, y confundirlos sería leer más de lo que aquí se promete.

La escala es la de niveles de madurez tecnológica de la Comisión Europea, nueve niveles donde el tercero es literalmente "prueba de concepto experimental", el cuarto "validada en laboratorio", el quinto "validada en entorno relevante", el sexto "demostrada en entorno relevante" y el séptimo "demostración de un prototipo de sistema en entorno operacional" (Comisión Europea, 2014).

| Objeto | Al iniciar el sprint | Al cerrar el sprint |
|---|---|---|
| **Signer Kit**, el componente reutilizable | 4: las cuatro piezas construidas con pruebas automatizadas que pasan, tres de ellas corridas en testnet | **5**, con las piezas de firma defendibles en 6: las cinco comprobaciones de política corridas en la red, invocación a un contrato ajeno al de ejemplo, instalable desde un clon limpio por un tercero |
| **Registro del ciclo**, la aplicación | 2: máquina de estados especificada, contrato no desplegado, ingesta validada solo en T0 | **5** para el tramo T0–T4: contrato desplegado, cuatro guardas ejecutadas en la red y dos aperturas reales con documentos legales de dos entidades |

**Por qué esto está por encima de una prueba de concepto.** Una prueba de concepto responde si algo es posible, bajo condiciones que elige quien construye, con datos que puede inventar, sin que nadie más deba poder repetirla, y sin medir su costo. Este sprint se prohíbe las cinco cosas: las condiciones las fija la norma, y las dos variantes de génesis existen porque la ley las produce; los documentos son reales y su huella se verifica contra la descarga directa del portal oficial; que un revisor externo reproduzca huella, compromiso y comisión sin intervención de TechGob es un criterio de aceptación, no una aspiración; el costo se mide por transición, por ciclo y por variante; y los modos de falla están documentados y probados, incluido qué ocurre si el operador desaparece o se niega a transmitir. A eso se suma lo que ninguna prueba de concepto produce: una política de renta de estado a varios años, una decisión de arquitectura con los umbrales que la revertirían (ADR-001), y un informe que permite a una entidad decidir.

**Y por qué no es más que eso.** No es un piloto: ninguna entidad lo opera y ningún procedimiento administrativo depende de él. No es un producto mínimo viable: la oficina de planeamiento y presupuesto no tiene todavía una superficie para usarlo, y eso empieza con la investigación de usuario del sprint 2. No confiere validez jurídica: el registro documenta hechos, no dictamina legalidad ni sustituye el sello de tiempo cualificado que a los documentos de La Punta les falta. El tramo cubierto son cinco de catorce transiciones y cuatro de doce guardas.

**Lo que esta declaración habilita.** Las reglas del programa excluyen financiar "exploración vaga, investigación sin límites definidos o financiamiento de hojas de ruta de largo plazo" y piden un entregable técnico concreto con criterios evaluables al cierre. Declarar el nivel es la forma de mostrar que esto es lo segundo. Y abre la ruta de financiamiento que sigue: el instrumento del Estado peruano para desarrollo tecnológico exige proyectos con "nivel de entrada TRL 4 o 5 y que cuenten con un nivel de salida de TRL 6 o superior" (PROCIENCIA, 2025). Es decir, la secuencia de tres sprints de la sección 7 deja al componente exactamente en la banda que el Estado financia por su cuenta. La instaward no es el final del camino de financiamiento: es el paso que vuelve alcanzable un instrumento público.

**Fuentes de esta sección**

Las citas de ambas fuentes están traducidas del inglés; el texto original se encuentra en los enlaces.

- Comisión Europea. (2014). *Horizon 2020 – Work Programme 2014-2015. General Annexes, Annex G: Technology readiness levels (TRL)* (Decisión C(2014)4995). https://ec.europa.eu/research/participants/data/ref/h2020/wp/2014_2015/annexes/h2020-wp1415-annex-g-trl_en.pdf
- PROCIENCIA. (2025). *Bases del concurso Proyectos de Desarrollo Tecnológico E041-2026-03*. Consejo Nacional de Ciencia, Tecnología e Innovación Tecnológica. https://prociencia.gob.pe/wp-content/uploads/2026/Proyectos%20de%20Desarrollo%20Tecnol%C3%B3gico%202026-03/20251030_Bases-PDT-2026%5BF%5D%5BF%5D.pdf

---

## 4. Alcance del trabajo

El tramo que cubre este sprint:

| T0 | T1 | T2 | T3 | T4 |
|---|---|---|---|---|
| ordenanza aprobada | vigente | convocado | acreditación cerrada | taller realizado |

En el recorrido interactivo son los hitos 1 a 3 (Génesis, Convocatoria, Taller). Los hitos 4 a 8 (T5–T13) siguen especificados y corresponden a los sprints posteriores descritos en la sección 7.

### Entregable 1 — Signer Kit v1 completo

**Construir:**

- `sign-auth-entry` generalizado a cualquier función de contrato. Hoy los scripts invocan `registrar(rol, huella)` y `signer-kit/README.md` declara el límite: "No hay todavía un `sign-auth-entry` genérico"
- Corrida en testnet de los dos casos de rechazo del relayer que faltan: **contrato no permitido** y **límite de frecuencia**. El código y sus pruebas ya existen y pasan; lo que se agrega es la corrida real, con su línea en `evidence/relayer/rechazos.jsonl` y su fila en `evidence/transacciones.md`
- Invocación autorizada por un rol con 0 XLM a un **contrato distinto del de ejemplo**, transmitida y pagada por el relayer, con el verificador de conformidad conforme en C1 a C6
- Traspaso de operador y verificador de conformidad empaquetados como comandos del kit
- Guía de instalación y guía "úsalo con tu propio contrato" (`require_auth()` sobre el rol)

**Criterios de aceptación:**

- Los cinco casos de rechazo del relayer —contrato, función, rol, frecuencia y tope de gasto— quedan corridos en testnet, cada uno con su registro y su fila de evidencia
- Una cuenta de rol con 0 XLM autoriza una invocación a un contrato distinto del de ejemplo; el relayer la transmite y paga; el verificador de conformidad da C1 a C6 conforme
- Una cuenta tercera transmite una entrada publicada
- El kit se instala y corre desde un clon limpio siguiendo solo el README

**Por qué importa:**
Es la pieza reutilizable para cualquier builder de Stellar que trabaje con una entidad pública. Lo que un auditor revisa no es que el relayer funcione, sino que esté demostrado que **no puede** actuar fuera de su política. Las pruebas automatizadas lo demuestran contra un doble de la red; la corrida en testnet lo demuestra contra la red real. El entregable cierra cuando están las dos.

---

### Entregable 2 — Registro del ciclo T0–T4 con guardas y las dos aperturas reales

**Construir:**

- Contrato Soroban del registro con T0 a T4 en orden: **una transición que se salta un paso legal es rechazada por la red**
- Guardas:
  - **G1** ciclo abierto: ninguna transición sin un ciclo abierto previamente
  - **G2** clave única: ubigeo + número de norma + año fiscal; una segunda apertura se rechaza
  - **G6** doble sello de tiempo: la fecha declarada del acto se compara con la marca de tiempo del ledger y el registro se marca como retroactivo cuando corresponde
  - **G7** actos previos a la vigencia: emite alerta y acepta la transición (el registro documenta hechos, no dictamina su legalidad)
- Autorización por rol en cada transición mediante el Signer Kit, con el firmante que `docs/maquina-estados.md` prescribe para cada paso
- Decisión de almacenamiento documentada **antes** de escribir las guardas: qué se guarda de forma persistente y qué solo como huella. La ADR-001 deshabilita la actualización del contrato, de modo que esta decisión no admite corrección después de la primera apertura real
- Cada guarda escrita primero como predicado puro con sus vectores de prueba, igual que los siete casos del contrato de datos, y portada a Rust después
- Las dos variantes de génesis que produce la norma, cada una con su apertura real en testnet: **(A) ordenanza única**, Ordenanza 001-2026-MPT de Tocache; **(B) ordenanza marco más decreto de alcaldía anual**, Decreto de Alcaldía 002-2026-MDLP/AL de La Punta
- Cierre de INC-01: huellas recalculadas sobre la descarga directa del portal oficial, con doble registro por dos roles distintos
- **Certificado de hito**: consulta de solo lectura que devuelve, para un ciclo y una transición, si el paso está cumplido, la huella de su documento, el rol firmante y el ledger. Se demuestra con un contrato consumidor mínimo que se niega a actuar si el hito no existe. No se mueven fondos
- Política de renta de estado: qué se guarda en almacenamiento persistente y qué solo como huella, la estrategia de extensión del tiempo de vida y su costo

**Criterios de aceptación:**

- Las pruebas automatizadas fallan en la red para: paso omitido, ciclo duplicado, transición sin ciclo y rol firmante equivocado
- Cada guarda tiene, además de su prueba de rechazo, una prueba del caso válido que debe pasar: una guarda que rechaza todo no es una guarda
- Ninguna apertura real se registra antes de que la decisión de almacenamiento esté probada en la red contra un ciclo de prueba desechable
- Las dos aperturas reales se confirman en testnet, una por variante de génesis, firmadas por **dos claves de rol distintas con 0 XLM**; la apertura duplicada se rechaza
- El contrato consumidor funciona cuando el hito existe y falla cuando no existe
- `evidence/documentos.md` marca las huellas de ambos documentos como "verificada contra la fuente"
- Ninguna carga anclada contiene datos personales; el caso de prueba de privacidad sigue fallando como está diseñado
- La capacidad de actualizar el contrato queda deshabilitada o condicionada a más de una clave, como exige la ADR-001

**Por qué importa:**
Detectar un paso inválido después no es lo mismo que impedirlo. El certificado de hito es el eslabón que le falta al ecosistema entre un acto administrativo y un desembolso: **acto administrativo verificable → hito certificado → desembolso**. Y las dos variantes de génesis no son un adorno: son la prueba de que el registro modela la norma y no un municipio en particular.

---

### Entregable 3 — Verificador en vivo, medición de comisiones e informe a las autoridades

**Construir:**

- **Informe de costos y del mecanismo para las autoridades competentes**, dirigido a la SGTD y a las dos municipalidades: costo medido por transición, por ciclo y por variante de génesis; quién firma y quién paga en cada paso; qué ocurre si el operador desaparece; y qué tendría que decidir la entidad para operarlo por su cuenta. Es el documento que convierte la evidencia técnica en una decisión administrativa posible

- **Verificador en vivo sobre T0–T4**: el recorrido de signerkit.govtechpe.work pasa de evidencia registrada a lectura en vivo para este tramo. Una persona descarga un documento del portal oficial y la página comprueba (1) su huella SHA-256 y (2) el compromiso canónico contra el ledger. Sigue siendo una página estática, sin backend
- Actualización de la etiqueta de la pieza 2 en el recorrido y de las etiquetas de las guardas entregadas, cada una enlazada a su transacción
- **Medición de comisiones**: comisión real de cada transacción T0–T4, total por ciclo y por variante de génesis, y costo de renta de estado en un horizonte de varios años, publicados en el repositorio
- Pruebas de punta a punta desde un clon limpio, con la integración continua en verde en sus cuatro trabajos
- Video de demostración actualizado, mostrando en testnet el rechazo de un paso omitido
- Nota de preparación para mainnet: ruta de auditoría (módulos de OpenZeppelin Stellar Contracts y postulación al Soroban Security Audit Bank), presupuesto de renta, gobernanza de claves de administración y traspaso del operador al laboratorio de la SGTD
- Guía de entrevista y sesiones agendadas con las oficinas de planeamiento y presupuesto de ambas municipalidades, para que el sprint 2 abra con las entrevistas listas. Las sesiones y el documento de requerimientos son del sprint 2, no de este

**Criterios de aceptación:**

- Un revisor externo reproduce la huella, el compromiso y la comisión de al menos una transición por municipalidad **sin intervención de TechGob**, siguiendo solo el README
- Informe de comisiones publicado con cifras tomadas de los hashes de transacción, no estimadas
- Informe de costos y del mecanismo entregado a la SGTD y a ambas municipalidades, con cada cifra referida a su hash de transacción y sin estimaciones
- Ninguna afirmación del recorrido, del README del kit o de este SOW se contradice con otra al cierre del sprint
- La nota de preparación lista los umbrales de la ADR-001 que revertirían el uso de contratos
- Guía de entrevista cerrada y sesiones del sprint 2 agendadas, o la negativa o falta de respuesta registrada por escrito

**Por qué importa:**
El registro es tan confiable como la capacidad de un ciudadano de comprobarlo por su cuenta, y el argumento de sostenibilidad necesita un costo medido, no una estimación.

---

### Fuera de alcance de este sprint

Lo siguiente está especificado y se postula como sprints posteriores (sección 7), no como promesa de este:

- Transiciones T5 a T8 y las guardas G8 y G10
- Ingesta de los cinco ciclos publicados de La Punta (2023–2027)
- Investigación de usuario con las oficinas de planeamiento y presupuesto, y trabajo de campo
- Verificador ciudadano completo, con la historia del ciclo en lenguaje llano
- Transiciones de nivel proyecto T9 a T13 y la sustitución con las reglas R1 a R7
- Tokenización: token no transferible por proyecto sobre SEP-50
- Perfil del Programa del Vaso de Leche
- Multifirma por rol y ciclo y, por lo tanto, la guarda G9

Excluido de todo el programa en su estado actual:

- Despliegue en mainnet y auditoría externa de seguridad
- Cualquier transferencia de valor, stablecoin o desembolso. El certificado de hito se demuestra con un contrato consumidor que no mueve fondos
- Ceremonia de passkey con un autenticador físico en el navegador
- Integración con SIAF, SEACE o el aplicativo del MEF
- Almacenamiento de documentos en la cadena o en el repositorio; datos personales en cualquier etapa

---

## 4.2 Presupuesto alineado con los entregables

**Monto solicitado: USD 5 000** · Tarifa única de USD 20 por hora para todo el equipo · 215 horas

### Por categoría

| Categoría | Rubro | Horas | Monto | Proporción |
|---|---|---|---|---|
| **Equipo central** | Desarrollo Soroban | 120 | USD 2 400 | 48 % |
| | Producto, revisión de entregables y gestión institucional | 95 | USD 1 900 | 38 % |
| | **Subtotal** | **215** | **USD 4 300** | **86 %** |
| **Tecnología y operaciones** | Infraestructura | — | USD 250 | 5 % |
| | Comisiones de red y renta de estado | — | USD 150 | 3 % |
| | Contingencia | — | USD 300 | 6 % |
| | **Subtotal** | — | **USD 700** | **14 %** |
| **Total** | | **215** | **USD 5 000** | **100 %** |

El acuerdo de aportes y distribución ata las 120 horas de desarrollo Soroban al alcance del plan de trabajo vigente y dispone que, **si durante la ejecución el alcance excediera esas horas, las partes lo acuerdan por escrito antes de ejecutar las horas adicionales**, definiendo en el mismo acto si se pagan, si se reduce el alcance o si se difieren a la etapa siguiente. Este SOW es ese plan de trabajo vigente.

### Las 120 horas de desarrollo Soroban

Distribución por tarea, derivada de los entregables de la sección 4. El total es lo comprometido; el reparto entre tareas es la planificación de la dueña de producto y se ajusta entre tareas durante la ejecución sin alterar el total.

| Tarea | Horas | Entregable |
|---|---|---|
| `sign-auth-entry` generalizado a cualquier función de contrato | 12 | E1 |
| Corrida en testnet del rechazo por contrato no permitido y por límite de frecuencia, con sus registros y filas de evidencia | 5 | E1 |
| Invocación a un contrato distinto del de ejemplo, transmitida y pagada, con el verificador de conformidad conforme en C1 a C6 | 6 | E1 |
| Traspaso de operador y verificador de conformidad empaquetados como comandos del kit | 4 | E1 |
| Guía de instalación y guía "úsalo con tu propio contrato" | 3 | E1 |
| Contrato Soroban del registro con T0 a T4 en orden y autorización por rol en cada transición | 18 | E2 |
| Guardas G1, G2, G6 y G7, cada una con su prueba de rechazo y su prueba del caso válido | 16 | E2 |
| Certificado de hito y contrato consumidor que se niega a actuar si el hito no existe | 10 | E2 |
| Las dos variantes de génesis y las dos aperturas reales en testnet | 10 | E2 |
| Política de renta de estado y estrategia de extensión del tiempo de vida | 6 | E2 |
| Verificador en vivo sobre T0–T4 y actualización de las etiquetas del recorrido | 14 | E3 |
| Medición de comisiones por transición, por ciclo y por variante | 5 | E3 |
| Pruebas de punta a punta desde un clon limpio, con la integración continua en verde | 5 | E3 |
| Video de demostración actualizado con el rechazo de un paso omitido | 3 | E3 |
| Nota de preparación para mainnet | 3 | E3 |
| **Total** | **120** | |

El tramo más cargado es el contrato del registro con sus guardas: 44 de las 120 horas, y es el único bloque sin precedente ejecutado. Si esas horas no alcanzan, el punto de control de la semana 3 decide, y el ajuste se acuerda por escrito antes de ejecutar horas adicionales.

### Las 95 horas de producto, revisión de entregables y gestión institucional

No son horas de coordinación. Son el trabajo que convierte código en un registro que modela la norma, y están desglosadas porque un revisor tiene derecho a saber qué compra:

| Tarea | Horas | Base del cálculo |
|---|---|---|
| Revisión de entregables y visado de pull requests | 40 | 2 horas diarias sobre 20 días hábiles |
| Obtención y verificación de los documentos municipales de ambas municipalidades, incluido el cierre de INC-01 contra la descarga directa del portal | 20 | Dos entidades, dos variantes de génesis, doble registro por roles distintos |
| Informe de costos y del mecanismo para las autoridades competentes: la SGTD y las dos municipalidades | 15 | Redacción, revisión de cifras contra los hashes de transacción y presentación |
| Aceptación de entregables, aprobación por pull request de los cambios a la máquina de estados e informe de cierre al Chapter Lead | 12 | Tres entregables con criterios evaluables, más el cierre del sprint |
| Guía de entrevista y agendamiento de las sesiones del sprint 2 con ambas oficinas de planeamiento y presupuesto | 8 | Preparación, sin ejecutar las sesiones |
| **Total** | **95** | |

**Por qué la revisión pesa 40 horas.** Son 40 horas de revisión contra 120 de desarrollo, una proporción de uno a tres, más alta que la habitual en desarrollo de software. La razón está en la ADR-001: en esta iteración la capacidad de actualizar el contrato queda deshabilitada o condicionada a más de una clave, de modo que una regla mal trasladada desde la norma no se corrige con un parche posterior. Cada transición y cada guarda derivan de un artículo, y quien verifica esa correspondencia es la dueña de producto, no el desarrollador. La revisión no juzga la calidad del código: comprueba que exista una prueba automatizada por cada criterio de aceptación, que los valores de esa prueba coincidan con los de la especificación, y que no entren al repositorio archivos que ningún criterio pidió.

El informe de costos y del mecanismo es un entregable y no un anexo. El argumento del proyecto es que una entidad pública puede usar Stellar sin tener XLM; eso solo se vuelve decisión administrativa cuando la autoridad recibe el costo medido por transición y por ciclo, y la explicación de quién paga, quién firma y qué pasa si el operador desaparece. Sin ese informe el sprint produce evidencia técnica que nadie en el Estado puede usar.

### Por entregable

| Entregable | Desarrollo (h) | Producto, revisión e institucional (h) | Costo del equipo | Costos directos | Total |
|---|---|---|---|---|---|
| E1 — Signer Kit v1 completo | 30 | 15 | USD 900 | — | USD 900 |
| E2 — Registro T0–T4 con guardas y dos aperturas reales | 60 | 42 | USD 2 040 | — | USD 2 040 |
| E3 — Verificador, comisiones e informe a las autoridades | 30 | 38 | USD 1 360 | — | USD 1 360 |
| Transversal | — | — | — | USD 700 | USD 700 |
| **Total** | **120** | **95** | **USD 4 300** | **USD 700** | **USD 5 000** |

**Sobre la partida de comisiones de red y renta de estado (USD 150).** En testnet los XLM se obtienen de friendbot y las comisiones no tienen costo monetario: la comisión medida de una invocación autorizada por el rol es de 13 666 stroops. La partida cubre lo que sí puede costar dinero dentro del sprint: las extensiones de tiempo de vida que exige la política de renta de estado cuando se prueban sobre un horizonte largo, el fondeo de la cuenta del operador si se repite la corrida tras un reinicio de testnet, y una eventual prueba de humo en mainnet si la nota de preparación lo recomienda y la dueña de producto lo aprueba. **Si no se usa, no se gasta y se informa como no ejecutada en el cierre**, con el detalle de comisiones pagadas tomado de `evidence/relayer/comisiones.jsonl`. Ninguna comisión se paga con fondos de una entidad pública: ese es el punto del proyecto.

**Cómo se fijó este alcance.** Por recomendación de quien define en el capítulo de embajadores qué proyectos se postulan a la instaward, el proyecto se evaluó con Stellar Raven, el servidor que da a agentes de inteligencia artificial la documentación de Stellar y el contexto de su ecosistema. Esa revisión quedó en el historial del repositorio con sus fuentes (`docs/revision-postulacion.md`, commit `6bb92c6`), las citas textuales de las reglas del programa están en `docs/instawards-reglas.md`, y concluyó que el plan anterior estaba sobredimensionado para 30 días. El alcance de esta versión responde a esa revisión: tres entregables en lugar de cuatro, ninguno cuyo cierre dependa de la firma de un tercero, y cada elemento retirado reaparece en la sección 7 con el sprint que lo recupera.

**El acuerdo entre las partes.** La relación entre TechGob y el desarrollador está establecida en un acuerdo de aportes y distribución firmado antes de iniciar el trabajo. Declara qué aporta cada parte antes de que exista financiamiento, cómo se distribuye el monto si la instaward se adjudica, la mecánica y el plazo del reparto, la autoría que cada parte declara, la confidencialidad del material de trabajo con la SGTD y qué ocurre si cualquiera de las dos se retira. No forma parte de lo que la postulación requiere, de modo que se conserva fuera del repositorio; está disponible para el Chapter Lead o para SDF si lo solicitan.

**Trabajo previo autofinanciado, que no se carga a esta instaward.** Unas 45 horas de diseño de la máquina de estados y el contrato de datos; las 15 horas del sprint S00 de preparación; y la construcción del relayer con política restringida, sus nueve pruebas automatizadas, la interfaz documentada, la corrida en testnet y las filas de evidencia del PR #11. **Las horas de esta última partida se declaran `SIN DATO`**: lo único observable en el repositorio es la ventana de los commits del PR #11, de 2 horas 18 minutos el 7 de octubre de 2026 para 17 archivos y 1 543 líneas, de las cuales cerca de 900 son documentación y evidencia. Esa ventana es tiempo transcurrido entre commits y no horas trabajadas, así que la cifra la aporta quien hizo el trabajo y no este documento.

---

## 5. Plan de ejecución de 30 días

Calendario de lunes a viernes, Perú. El plan se mantiene como datos validados por esquema en `planning/` y se comprueba en integración continua, igual que el sprint S00.

### Semana 1 — Las dos decisiones de arquitectura

Las dos tareas de las que depende todo lo demás, y las únicas que no se pueden corregir tarde.

- `sign-auth-entry` generalizado a cualquier función de contrato, que es por donde el registro autoriza por rol
- Decisión de almacenamiento del registro, documentada
- Esqueleto vertical de T0 con G1, G2 y la consulta de certificado de hito, desplegado en testnet **contra un ciclo de prueba desechable**, nunca contra un documento municipal real
- Las guardas escritas como predicados puros con sus vectores de prueba

**Resultado esperado**
El modelo de almacenamiento resuelto y ejercido en la red. Como la ADR-001 deshabilita la actualización del contrato, este es el último momento en que el diseño admite cambios.

**Punto de control (fin de la semana 1):** si la decisión de almacenamiento o el esqueleto de T0 no están resueltos y probados en la red, el diseño del contrato se replantea con un mes por delante en lugar de con una semana. Ninguna apertura real se registra antes de superar este punto.

### Semana 2 — El ciclo y sus guardas

- T1 a T4 en orden, con el firmante que la máquina de estados prescribe para cada paso
- **G7 antes de G6.** G7 es la única guarda que acepta la transición y emite alerta, así que exige un canal de observación que no sea un rechazo; si el contrato no lo tiene, es un cambio de diseño y aparece aquí
- G6 al cierre, que solo necesita la marca de tiempo del ledger
- Contrato consumidor que se niega a actuar si el hito no existe

**Resultado esperado**
Un paso omitido, un ciclo duplicado, una transición sin ciclo y un rol equivocado, rechazados por la red, cada guarda con su prueba de rechazo y su prueba del caso válido.

### Semana 3 — Las dos aperturas reales y el cierre del kit

- Variantes de génesis A y B sobre el contrato ya estabilizado
- Apertura del ciclo de Tocache y del de La Punta en testnet, con dos claves de rol distintas en 0 XLM
- Cierre de INC-01 sobre descargas directas del portal
- Política de renta de estado
- Cierre del kit, que no depende del registro: corridas en testnet del rechazo por contrato no permitido y por límite de frecuencia, invocación a un contrato distinto del de ejemplo, empaquetado y guías

**Resultado esperado**
Dos ciclos legales reales abiertos y avanzados hasta T4, cada uno con su variante de génesis; los cinco casos de rechazo del relayer corridos en testnet; el kit instalable desde un clon limpio.

**Punto de control (fin de la semana 3):** si una guarda no resulta implementable como está especificada, el cambio se propone por pull request con su justificación y lo aprueba la dueña de producto. Las reglas que vienen de la norma no se abandonan por conveniencia de implementación. Si la apertura de una de las dos municipalidades se bloquea por falta de documento, se informa como pendiente y no se completa con supuestos: E1 y E3 no se recortan.

### Semana 4 — Verificar, medir e informar

- Verificador en vivo sobre T0–T4 y actualización de las etiquetas del recorrido
- Medición de comisiones por transición, por ciclo y por variante
- Informe de costos y del mecanismo para la SGTD y ambas municipalidades
- Pruebas de punta a punta, documentación y video actualizado
- Nota de preparación para mainnet
- Guía de entrevista y agendamiento de las sesiones del sprint 2

**Resultado esperado**
Un revisor verifica la cadena completa de T0 a T4 en las dos municipalidades solo con el repositorio y el recorrido; informe de comisiones publicado; informe de costos y mecanismo entregado a las autoridades.

---

## 6. Evidencia de cumplimiento

### Entregable 1

- Versión etiquetada del Signer Kit v1 en el repositorio
- Filas R-4 y R-5 de `evidence/transacciones.md`: rechazo por contrato no permitido y por límite de frecuencia, corridos en testnet, con sus líneas en `evidence/relayer/rechazos.jsonl`
- Hash en testnet de la invocación a un contrato distinto del de ejemplo, y de la transmisión por un tercero
- Salida del verificador de conformidad (C1 a C6)

### Entregable 2

- ID del contrato del registro en testnet
- Hashes de las dos aperturas reales y de la apertura duplicada rechazada
- Hash de un paso omitido rechazado
- Informe de pruebas por guarda, con el caso de rechazo y el caso válido, enlazado a la integración continua
- Hashes del contrato consumidor, con el hito presente y ausente
- `evidence/documentos.md` con las dos huellas verificadas contra la fuente
- Documento de política de renta de estado

### Entregable 3

- Verificador en vivo en signerkit.govtechpe.work para T0–T4
- Recorrido documentado de una verificación independiente por municipalidad
- Informe de comisiones por transición, ciclo y variante
- Informe de costos y del mecanismo, con acuse de entrega a la SGTD y a ambas municipalidades
- Video de demostración actualizado
- Nota de preparación para mainnet
- Guía de entrevista y confirmación de las sesiones agendadas para el sprint 2
- Repositorio con la integración continua en verde en sus cuatro trabajos

### Lista de verificación de evidencia

| Entregable | Evidencia presente | Parcial | Ausente |
|---|---|---|---|
| E1 — Signer Kit v1 completo | ☐ | ☐ | ☐ |
| E2 — Registro T0–T4 y dos aperturas reales | ☐ | ☐ | ☐ |
| E3 — Verificador, comisiones e informe a las autoridades | ☐ | ☐ | ☐ |

### Definición de terminado (para todo entregable)

- Reproducible desde un clon limpio siguiendo el README
- Sin claves ni secretos en el código, ni de testnet
- Ninguna salida contiene datos personales
- Cada enlace citado abre y muestra lo que el texto afirma; donde el repositorio no registra un valor, dice `SIN DATO` en lugar de estimarlo
- Lo probado contra un doble de la red se declara como tal y no como corrido en testnet
- Integración continua en verde en el commit de la versión

---

## 7. Alineación con los sprints siguientes

Las reglas del programa contemplan hasta dos desembolsos posteriores, con un tope acumulado de USD 15 000 en XLM, cada uno con su propio sprint, el anterior completado y confirmado por el Chapter Lead. No son automáticos. La secuencia que TechGob propone, con el alcance ya especificado en el repositorio:

| Sprint | Alcance | Qué habilita |
|---|---|---|
| **1 — esta instaward** | Signer Kit v1 completo; registro T0–T4 con G1, G2, G6 y G7; dos aperturas reales; certificado de hito; verificador, comisiones e informe a las autoridades sobre T0–T4 | El kit reutilizable, la prueba de que la red puede rechazar un paso administrativo inválido, y el costo medido en manos de quien decide |
| **2** | T5 a T8 con las guardas G8 y G10; ingesta de los cinco ciclos publicados de La Punta; investigación de usuario en terreno con las oficinas de planeamiento y presupuesto de ambas municipalidades, con las entrevistas ya agendadas en el sprint 1 | El ciclo completo a nivel de ciclo, validado contra una serie histórica real y contra el requerimiento de quienes lo operan |
| **3** | Verificador ciudadano completo; transiciones de nivel proyecto T9 a T13 con la sustitución R1 a R7; perfil del Programa del Vaso de Leche | El registro llega al proyecto ejecutado y se extiende al primer programa de beneficio, con entregas atestiguadas por los comités, sin mover un sol en la cadena y sin tocar el padrón de beneficiarias |

**Por qué los comités del Vaso de Leche.** Los comités del programa son el mejor testigo posible: no necesitan interpretar un expediente para saber si la entrega llegó, y son los únicos con incentivo directo para reportar cuando no llega.

En los tres sprints TechGob paga las comisiones. Después, el rol de operador pasa al Laboratorio de Innovación Digital de la SGTD, y el traspaso ya probado en testnet lo convierte en un cambio de configuración. El camino a mainnet pasa por una auditoría externa y una postulación al SCF Build Award.

---

## 8. Métricas de éxito

| Métrica | Hoy | Meta del sprint |
|---|---|---|
| Piezas del kit construidas y con pruebas automatizadas que pasan | 4 de 4 | 4 de 4 |
| Casos de rechazo del relayer corridos en testnet | 2 de 5 | 5 de 5 |
| Invocación a un contrato distinto del de ejemplo | No | Sí, pagada por el relayer y conforme en C1 a C6 |
| Guardas ejecutadas en testnet | 0 | 4 (G1, G2, G6 y G7) |
| Variantes de génesis con apertura real en testnet | 0 | 2 (ordenanza única y ordenanza marco con decreto anual) |
| Claves de rol institucionales distintas que firman con 0 XLM | 1 | 2, una por municipalidad |
| Transiciones del ciclo registradas | T0 solo en ingesta | T0 a T4 donde exista el documento fuente |
| Transiciones inválidas rechazadas por la red | 0 | 100 % de los casos de prueba |
| Comisión por transición, por ciclo y por variante | Una medición aislada | Medida y publicada |
| Verificaciones independientes de terceros | 0 | Al menos 1 por municipalidad |
| Entidades que reciben el informe de costos y del mecanismo | 0 | 3 (SGTD y las dos municipalidades) |
| Datos personales en cargas ancladas | 0 | 0 |

---

## 9. Riesgos, dependencias y mitigaciones

| Riesgo o dependencia | Probabilidad | Impacto | Mitigación |
|---|---|---|---|
| **Capítulo y Chapter Lead sin confirmar.** Las reglas exigen identificar al Chapter Lead que acompaña la postulación y participación activa en el capítulo | Alta | Bloqueante | Se completan los dos campos pendientes de la sección 2, capítulo y Chapter Lead, antes de enviar. La fecha de inicio del 9 de noviembre queda sujeta a esa confirmación |
| **KYC previo al desembolso.** Las reglas exigen completar el KYC de SDF antes de cualquier desembolso, y pueden pedir repetirlo o pedir el KYB de la organización durante el premio | Media | Alto | El enlace del KYC y la lista de documentos se solicitan al Chapter Lead **antes de enviar la postulación**, y la documentación de la sociedad queda reunida de antemano. SDF no publica esa lista, de modo que se confirma en lugar de suponerse. El plan de trabajo no depende del desembolso para arrancar |
| Documentos municipales retrasados: constancia de publicación de la ordenanza de Tocache, versiones públicas sin columna de documento de identidad | Media | Medio | Solicitudes emitidas al inicio del sprint. Las transiciones faltantes se informan como pendientes y nunca se completan con supuestos |
| Reinicio de testnet que rompe los enlaces al explorador. La documentación oficial indica de 2 a 4 reinicios al año, a las 17:00 UTC, anunciados con al menos dos semanas de anticipación; el próximo programado es el 16 de diciembre de 2026 | Baja dentro del sprint | Bajo | El sprint cierra antes de esa fecha. Cada corrida está automatizada y fechada, y los resúmenes con hashes, ledgers y comisiones quedan versionados en el repositorio, de modo que un enlace caído no borra la evidencia |
| Costo de renta de estado subestimado | Media | Alto | La política de renta es parte de E2 y su costo se mide en E3, con la partida de comisiones como respaldo |
| Una guarda no es implementable tal como está especificada | Baja | Medio | Cambio propuesto por pull request y aprobado por la dueña de producto; las reglas que vienen de la norma no se abandonan por conveniencia |
| Un operador único concentra poder | Baja | Alto | Las entradas se publican y cualquier tercero puede transmitirlas; el traspaso ya está probado; el operador de destino es el laboratorio de la SGTD |
| Datos personales llegan a la cadena | Baja | Alto | Regla de admisión por campo, privacidad por defecto, rechazo estructural, validador en dos capas y un caso de prueba que debe fallar |
| Trabajo adelantado que se declare probado a un estándar distinto del resto | Media | Medio | Ninguna afirmación de este SOW declara "corrido en testnet" lo que solo está probado contra un doble de la red. Cada corrida tiene su hash en `evidence/transacciones.md`, su prueba automatizada y la integración continua en verde |

---

## 10. Protección de datos y seguridad

- Solo se anclan documentos públicos por mandato legal. Nunca datos personales, ni la huella de un identificador personal.
- Las claves pertenecen a roles y ciclos, no a personas.
- El esquema lo hace cumplir: cada campo declara su regla de admisión; un campo sin anotación queda fuera de la cadena; se rechazan los campos no declarados y los nombres de campo que sugieren datos personales. El caso de prueba que intenta anclar un dato personal debe fallar, y falla en integración continua.
- Sin secretos en el repositorio; los scripts leen las claves desde el almacén de la CLI de Stellar.
- Marco: Ley N.° 29733 y Decreto Supremo N.° 016-2024-JUS. El registro no reemplaza la evaluación de protección de datos que corresponde a cada entidad.

---

## Anexo — Coherencia con los artefactos públicos

| Afirmación de este SOW | Repositorio | Video | Recorrido interactivo |
|---|---|---|---|
| Firmar sin tener XLM | README, evidencia de HU-01 | Título y apertura | Piezas 1, 3 y 4 marcadas como probadas |
| Las cuatro piezas están construidas y con pruebas que pasan | `signer-kit/relayer.py`, `signer-kit/test_relayer.py`, integración continua | — | Pieza 2 marcada como construida |
| Del relayer faltan dos casos de rechazo por correr en testnet | `evidence/transacciones.md`, R-1 a R-3; `signer-kit/README.md` | — | Pieza 2, nota de alcance |
| Alcance T0–T4 con cuatro guardas | README, "Alcance de esta postulación a instaward" | Sección 05, rotulada en inglés: la etapa siguiente es el registro del ciclo, en desarrollo | Hitos 1 a 3 |
| Un paso legal omitido es rechazado por la red | `docs/maquina-estados.md`, ADR-001 | Rotulado en inglés: un paso legal omitido es rechazado por la red | Descripción de las guardas |
| Certificado de hito | `docs/statement-of-work.md` | Rotulado en inglés: certificado de hito, una precondición que un desembolso puede exigir | — |
| Dos variantes de génesis | `docs/maquina-estados.md`, sección de génesis | — | Hito 1 |
| Diseñado sobre documentos municipales reales del Perú | `evidence/documentos.md`, contrato de datos | "Está diseñado sobre documentos municipales reales del Perú" | 16 inconsistencias de la ordenanza de Tocache |
