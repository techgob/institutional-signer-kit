# Statement of Work (SOW) — Instawards

## Institutional Signer Kit: firmar sin poseer — Compromiso acotado de 30 días

*Una institución pública firma en Stellar sin tener nunca XLM.*

---

## 1. Información del proyecto y del equipo

| Campo | Valor |
|---|---|
| Nombre del proyecto | Institutional Signer Kit |
| Postulante | TECH GOB CONSULTORA EN TRANSFORMACIÓN DIGITAL Y TECNOLOGÍAS EMERGENTES SpA (TechGob), Chile |
| Builder / equipo | Nadinne Canto Novoa — dueña de producto (alcance, priorización y aceptación de entregables; máquina de estados derivada del marco normativo; contrato de datos; relación institucional) · Kevin Alexander Soto Burgos (@kasbsquall) — desarrollo (arquitectura técnica, implementación en Soroban, separación firmante-pagador, ingesta y verificador) |
| Contacto principal | [por confirmar] |
| Capítulo de embajadores | [por confirmar] |
| Chapter Lead | [por confirmar] |
| Repositorio | https://github.com/techgob/institutional-signer-kit (Apache-2.0, con integración continua) |
| Recorrido interactivo | https://signerkit.govtechpe.work |
| Video de demostración | https://youtu.be/Pel8UScd8x4 (1:41) |
| Red | Stellar Testnet (Soroban) |
| Contrapartes de validación en terreno | Municipalidad Provincial de Tocache (San Martín) y Municipalidad Distrital de La Punta (Callao), Perú, con acceso habilitado por la Red Nacional de Laboratorios de Innovación Digital de la Secretaría de Gobierno y Transformación Digital (SGTD-PCM) |
| Fecha de postulación | Octubre de 2026 |
| Inicio sugerido del sprint | 2 de noviembre de 2026 (sprint S02 del plan publicado, sujeto a la resolución) |
| Duración | 30 días (sprint de 4 semanas) |
| Monto solicitado | USD 5 000 |

---

## 2. Visión general e intención de la instaward

### 2.1 Propósito

Esta instaward completa el **Institutional Signer Kit**, un componente abierto y reutilizable que permite a una institución pública autorizar invocaciones en Soroban con **saldo cero en XLM, sin partida presupuestal y sin custodia de activos**.

Soroban firma las entradas de autorización de forma independiente del sobre de la transacción, de modo que quien autoriza y quien paga la comisión pueden ser cuentas distintas. El kit empaqueta esa propiedad en cuatro piezas. Tres ya están probadas en testnet; este sprint construye la cuarta y pone el kit completo a trabajar sobre un proceso administrativo real.

Ese proceso es el ciclo del presupuesto participativo que la ley peruana hace obligatorio, modelado como máquina de estados a partir de documentos municipales reales de dos municipalidades. El resultado es el registro del ciclo que anuncia el cierre del video: un contrato en el que **una transición que se salta un paso legal es rechazada por la red**, y en el que cada paso cumplido produce un **certificado de hito, una precondición que un desembolso puede exigir**.

### 2.2 Punto de partida: lo que ya es público y verificable

El sprint parte de evidencia que funciona. Todo lo que sigue está en el repositorio, en el recorrido interactivo o en el video.

**Las cuatro piezas del kit**

| Pieza | Estado hoy | Evidencia |
|---|---|---|
| 1. Firma por rol y ciclo: las claves pertenecen a cargos y períodos, no a personas | **Probada en testnet.** Cuenta clásica de rol con 0 XLM y reserva patrocinada; cuenta de contrato con passkey que rota por ciclo mientras la dirección del rol se mantiene | Corrida HU-01; corrida passkey P-1 a P-4 (`evidence/transacciones.md`) |
| 2. Relayer con política restringida: el pagador solo transmite invocaciones autorizadas, con tope de gasto y límite de frecuencia | **No implementado.** Lo financia esta instaward | `signer-kit/README.md`; recorrido, pieza 2 |
| 3. Trazabilidad entre comisión y autorización: cada comisión queda enlazada a la entrada firmada que la originó | **Probada**, sin claves, sobre transacciones confirmadas (comprobaciones C3, C4 y C5) | `verifier/conformidad.py` |
| 4. Autorización portátil: cualquier tercero puede transmitir una entrada publicada; el operador no puede censurar | **Probada en testnet**: la entrada B se publicó como XDR y la transmitió un tercero; el reenvío de la entrada A fue rechazado | tx `fb284c5b…b8dd`; tx `ac8f406c…0542` (`Error(Auth, ExistingValue)`) |

**Diez transacciones registradas en testnet** respaldan estas afirmaciones: creación de la cuenta con reserva patrocinada, HU-01 (A, B y reenvío), traspaso de operador (T-1, T-2) y rotación con passkey (P-1 a P-4). El traspaso de operador ya es un cambio de configuración y no una migración: la clave del rol y el contrato no cambian.

**El registro del ciclo, especificado y probado fuera de la cadena**

| Activo | Estado hoy |
|---|---|
| Máquina de estados: 14 transiciones T0–T13 agrupadas en 8 hitos, guardas G1–G12, reglas de sustitución R1–R7 y dos variantes de génesis | Especificada (`docs/maquina-estados.md`); se recorre hito por hito en el recorrido interactivo |
| Guardas | **Especificadas, contrato no desplegado** (etiqueta del recorrido) |
| Contrato de datos con reglas de admisión por campo y validador en dos capas | 7 casos de prueba aprobados en integración continua |
| Ingesta contra un documento real | **Solo T0**: Ordenanza 001-2026-MPT de Tocache, resultado `observado` con 16 inconsistencias (una bloqueante, INC-01: la huella se calculó sobre una copia y no sobre la descarga directa del portal) |
| Verificador local (huella del PDF y compromiso canónico) | Funciona, con pruebas |
| Decisión de imponer las transiciones con contratos Soroban | ADR-001 aceptada |

Comisión medida para una invocación autorizada por el rol en el contrato de ejemplo: **13 677 stroops**, pagados por el operador; el rol termina con 0 XLM. El costo del contrato real del ciclo se mide en este sprint.

---

## 3. Problema y objetivo

### El problema

Ninguna municipalidad peruana puede comprar, custodiar ni rendir cuentas de un criptoactivo solo para pagar comisiones de red. Hacerlo exige un proceso de contratación, una partida presupuestal, reglas de custodia de claves y rendición ante la Contraloría, y choca con el principio de unidad de caja del sistema de tesorería. El costo administrativo de habilitar el pago supera en órdenes de magnitud al pago mismo. Ahí mueren la mayoría de los pilotos de blockchain público, antes de discutir arquitectura.

El efecto se ve en carteras reales. En un taller conjunto con la SGTD, TechGob levantó 23 desafíos públicos de 25 entidades. Stellar fue la red recomendada en **2 de 23** casos. No se descartó por razones técnicas para notarización o credenciales; se prefirieron redes permisionadas porque no obligan a la entidad a tener un activo. *(El análisis de portafolio es material de trabajo con la SGTD; puede exponerse al comité bajo acuerdo de confidencialidad.)*

El presupuesto participativo muestra por qué falta esta pieza. Stellar ya puede responder **quién recibió** un pago. Nadie responde **quién decidió, con qué acto y bajo qué regla**. En las dos municipalidades piloto esa evidencia es un PDF escaneado sin integridad alguna (Tocache) y un decreto nativo digital con siete firmas válidas, pero sin sello de tiempo cualificado ni datos de validación de largo plazo (La Punta). A ninguna le falta capacidad de gasto. A las dos les falta una cadena de evidencia que conecte lo que los vecinos acordaron con lo que efectivamente se hizo.

Hoy no existe un componente reutilizable que permita a una entidad pública, a la vez:

- firmar con claves que pertenecen a cargos y períodos, como exige la Ley N.° 29733 de Protección de Datos Personales;
- delegar el pago de comisiones en un operador que **no puede** usar su rol de pagador para otra cosa;
- auditar cada comisión que pagó el operador;
- seguir operando si el operador desaparece o se niega a transmitir;
- lograr que la red rechace un paso administrativo que la norma no permite.

### Objetivo

En 30 días TechGob entregará en Stellar Testnet:

1. **Signer Kit v1**, empaquetado y documentado, con el relayer de política restringida (pieza 2);
2. el **registro del ciclo T0–T8** con sus guardas, en el que un paso legal omitido falla en la red y cada paso cumplido puede consultarse como certificado de hito;
3. la **ingesta v2** con los dos perfiles de documento (escaneado y nativo digital), con documentos reales de ambas municipalidades;
4. un **verificador ciudadano** que reproduce cada huella desde la fuente oficial y el ledger sin ayuda de TechGob;
5. la **investigación de usuario** con ambas municipalidades y el **costo medido de comisiones** por transición.

**Criterio de éxito:** dos claves de rol institucionales distintas, cada una con 0 XLM, firman transiciones válidas de un ciclo legal real; una transición inválida es rechazada por la red; y un revisor externo puede comprobarlo todo solo con el repositorio y el recorrido interactivo.

---

## 4. Alcance del trabajo

El ciclo usa las mismas transiciones que el video (allí con etiquetas en inglés) y que el recorrido:

| T0 | T1 | T2 | T3 | T4 | T5 | T6 | T7 | T8 |
|---|---|---|---|---|---|---|---|---|
| ordenanza aprobada | vigente | convocado | acreditación cerrada | taller realizado | priorizado | acta formalizada | comité instalado | remitido al MEF |

En el recorrido interactivo estas nueve transiciones son los hitos 1 a 6 (Génesis, Convocatoria, Taller, Priorización, Acta y comité, Remisión). Los hitos 7 y 8 (T9–T13, nivel proyecto) siguen especificados y corresponden a la siguiente iteración.

### Entregable 1 (semana 1) — Signer Kit v1

**Construir:**

- `sign-auth-entry` generalizado a cualquier función de contrato (hoy está fijo en `registrar(rol, huella)`)
- **Relayer con política restringida** (pieza 2): lista de contratos y funciones permitidos, tope de gasto por rol, límite de frecuencia y registro de solicitudes rechazadas
- Registro del operador con cada comisión pagada y la entrada de autorización que la originó, legible por el verificador de conformidad (pieza 3)
- Publicación de cada entrada firmada como XDR antes de transmitirla (pieza 4)
- Soporte para los dos tipos de rol ya probados: cuenta clásica con reserva patrocinada y cuenta de contrato con passkey
- Traspaso de operador y verificador de conformidad (C1–C6) empaquetados como comandos del kit
- Guía de instalación y guía "úsalo con tu propio contrato" (`require_auth()` sobre el rol)

**Criterios de aceptación:**

- Una cuenta de rol con 0 XLM autoriza una invocación a un contrato distinto del de ejemplo; el relayer la transmite y paga; el verificador de conformidad da C1–C6 conforme
- El relayer rechaza, dejando registrado el motivo, un contrato no permitido, una función no permitida y una invocación que supera el tope de gasto (tres pruebas automatizadas)
- Una cuenta tercera transmite una entrada publicada

**Por qué importa:**
Es la pieza reutilizable para cualquier builder de Stellar que trabaje con una entidad pública. Con la pieza 2, el operador paga pero no puede usar ese rol para otra cosa, que es lo que hace aceptable el arreglo ante un auditor.

---

### Entregable 2 (semana 2) — Registro del ciclo T0–T8 con guardas

**Construir:**

- Contrato Soroban del registro del ciclo con T0–T8 en orden: **una transición que se salta un paso legal es rechazada por la red**
- Guardas para estas transiciones:
  - **G1** ciclo abierto: ninguna transición sin un ciclo abierto previamente
  - **G2** clave única: ubigeo + número de norma + año fiscal; una segunda apertura se rechaza
  - **G6** doble sello de tiempo: la fecha declarada del acto se compara con la marca de tiempo del ledger y el registro se marca como retroactivo cuando corresponde
  - **G7** actos previos a la vigencia: emite alerta y acepta la transición (el registro documenta hechos, no dictamina su legalidad)
  - **G8** claves incompatibles: una misma clave no puede representar al comité de vigilancia y al consejo de coordinación local
  - **G10** puntaje verificable (T5): el contrato recalcula la suma del vector de criterios y rechaza valores fuera de la escala
- Autorización por rol en cada transición mediante el Signer Kit (el firmante que `docs/maquina-estados.md` prescribe para cada paso)
- Las dos variantes de génesis: (A) ordenanza única, Tocache; (B) ordenanza marco más decreto de alcaldía anual, La Punta
- **Certificado de hito**: una consulta de solo lectura que devuelve, para un ciclo y una transición, si el paso está cumplido, la huella de su documento, el rol firmante y el ledger. Se demuestra con un contrato consumidor mínimo que se niega a actuar si el hito no existe. No se mueven fondos.
- Política de renta de estado: qué se guarda en almacenamiento persistente y qué solo como huella, la estrategia de extensión del tiempo de vida y su costo

**Criterios de aceptación:**

- Las pruebas automatizadas fallan en la red para: paso omitido, ciclo duplicado, transición sin ciclo, rol firmante equivocado, misma clave para comité y consejo, y puntaje fuera de escala
- La apertura del ciclo 2027 de Tocache se confirma en testnet y la apertura duplicada se rechaza; ambas quedan como filas 3 y 4 de `evidence/transacciones.md` (ya reservadas)
- El contrato consumidor funciona cuando el hito existe y falla cuando no existe
- La capacidad de actualizar el contrato queda deshabilitada o condicionada a más de una clave en esta iteración, como exige la ADR-001

**Por qué importa:**
Detectar un paso inválido después no es lo mismo que impedirlo. El certificado de hito es el eslabón que le falta al ecosistema entre un acto administrativo y un desembolso: **acto administrativo verificable → hito certificado → desembolso**.

---

### Entregable 3 (semana 3) — Ingesta v2 e investigación de usuario

**Construir:**

- Validador de ingesta v2 con los dos perfiles de documento ya definidos en el contrato de datos:

| | Tocache | La Punta |
|---|---|---|
| Origen del documento | Escaneado de un impreso | Nativo digital |
| Autoría | Firma manuscrita y sellos de visto bueno | Siete certificados digitales FAU |
| Integridad hoy | Ninguna | Criptográfica (SHA-256), sin sello de tiempo cualificado |
| Validación en la ingesta | Doble revisión humana por dos roles | Verificación automática de firma más revisión simple |

- Cierre de INC-01: huellas recalculadas sobre la descarga directa del portal oficial, con doble registro por dos roles distintos
- Ingesta y anclaje, mediante el registro, de los documentos T0–T8 disponibles para **Tocache 2027** y para los **cinco ciclos publicados de La Punta (2023–2027)**
- Solo versiones públicas: cuando una plantilla incluye columna de documento de identidad (INC-10), se ancla únicamente la versión sin esa columna
- **Investigación de usuario** con la oficina de planeamiento y presupuesto (OPP) de cada municipalidad: guía de entrevista, sesiones en terreno en Tocache y La Punta, y documento de requerimientos

**Criterios de aceptación:**

- Los cinco ciclos publicados de La Punta se ingestan sin excepciones manuales; cualquier rechazo se explica por una regla del validador
- Las transiciones de ambas municipalidades las firman **dos claves de rol distintas con 0 XLM**
- `evidence/documentos.md` marca ambas huellas como "verificada contra la fuente"
- El caso de prueba de privacidad (`caso_01_dato_personal_en_proyecto`) sigue fallando como está diseñado; ninguna carga anclada contiene datos personales
- Documento de requerimientos cerrado y firmado, o confirmado por escrito, por cada OPP

**Por qué importa:**
La firma digital prueba quién firmó. El anclaje prueba cuándo existió el documento y que la serie está completa. En Tocache el registro aporta la integridad que hoy no existe; en La Punta, la permanencia que una firma sin sello de tiempo cualificado no garantiza cuando los certificados expiren.

---

### Entregable 4 (semana 4) — Verificador ciudadano, medición de comisiones y preparación del piloto

**Construir:**

- **Verificador ciudadano**: el recorrido de signerkit.govtechpe.work pasa de evidencia registrada a lectura en vivo. Una persona descarga un documento del portal oficial y la página comprueba (1) su huella SHA-256 y (2) el compromiso canónico contra el ledger, y muestra la historia del ciclo en lenguaje llano. Sigue siendo una página estática, sin backend
- **Medición de comisiones**: comisión real de cada transacción T0–T8, total por ciclo y costo de renta de estado en un horizonte de varios años, publicados en el repositorio
- Pruebas de punta a punta desde un clon limpio, con la integración continua en verde (contrato de datos, verificador, conformidad, plan de sprint y pruebas del contrato)
- Video de demostración actualizado, mostrando en testnet el rechazo de un paso omitido
- Nota de preparación para mainnet: ruta de auditoría (módulos de OpenZeppelin Stellar Contracts y postulación al Soroban Security Audit Bank), presupuesto de renta, gobernanza de claves de administración y traspaso del operador al laboratorio de la SGTD
- Informe de investigación de usuario

**Criterios de aceptación:**

- Un revisor externo reproduce la huella y el compromiso de al menos una transición por municipalidad **sin intervención de TechGob**, siguiendo solo el README
- En el recorrido, las etiquetas de las guardas del entregable 2 cambian de "especificadas, contrato no desplegado" a "ejecutadas en testnet", cada una enlazada a su transacción
- Informe de comisiones publicado con cifras tomadas de los hashes de transacción
- La nota de preparación lista los umbrales de la ADR-001 que revertirían el uso de contratos

**Por qué importa:**
El registro es tan confiable como la capacidad de un ciudadano de comprobarlo por su cuenta, y el argumento de sostenibilidad necesita un costo medido, no una estimación.

---

### Fuera de alcance

En línea con el README del repositorio ("Fuera de alcance por ahora"), quedan excluidos:

- Despliegue en mainnet
- Auditoría externa de seguridad
- Tokenización (token no transferible por proyecto sobre SEP-50)
- Transiciones de nivel proyecto T9–T13, incluida la sustitución de proyectos (hitos 7 y 8 del recorrido)
- Multifirma por rol y ciclo y, por lo tanto, la guarda G9 (quórum del comité); en esta iteración T7 registra el acta de elección y las claves de rol del comité
- Perfil del Programa del Vaso de Leche
- Cualquier transferencia de valor, stablecoin o desembolso (el certificado de hito se demuestra con un contrato consumidor que no mueve fondos)
- Ceremonia de passkey con un autenticador físico en el navegador (la rotación ya está probada con claves P-256 generadas en software)
- Integración con SIAF, SEACE o el aplicativo del MEF
- Almacenamiento de documentos en la cadena o en el repositorio; datos personales en cualquier etapa

---

## 4.2 Presupuesto alineado con los entregables

**Monto solicitado: USD 5 000** · Tarifa única de USD 20 por hora para todo el equipo · 190 horas

### Por categoría

| Categoría | Rubro | Horas | Monto | Proporción |
|---|---|---|---|---|
| **Equipo central y operación** | Desarrollo Soroban | 120 | USD 2 400 | 48 % |
| | Gestión institucional e investigación de usuario | 70 | USD 1 400 | 28 % |
| | **Subtotal** | **190** | **USD 3 800** | **76 %** |
| **Tecnología y operaciones** | Trabajo de campo en Tocache y La Punta | — | USD 600 | 12 % |
| | Infraestructura | — | USD 250 | 5 % |
| | Contingencia | — | USD 350 | 7 % |
| | **Subtotal** | — | **USD 1 200** | **24 %** |
| **Total** | | **190** | **USD 5 000** | **100 %** |

### Por entregable

| Entregable | Desarrollo (h) | Producto e institucional (h) | Costo del equipo | Costos directos | Total |
|---|---|---|---|---|---|
| E1 — Signer Kit v1 | 35 | 5 | USD 800 | — | USD 800 |
| E2 — Registro del ciclo T0–T8 | 40 | 10 | USD 1 000 | — | USD 1 000 |
| E3 — Ingesta v2 e investigación de usuario | 25 | 35 | USD 1 200 | USD 600 trabajo de campo | USD 1 800 |
| E4 — Verificador, comisiones y preparación | 20 | 20 | USD 800 | — | USD 800 |
| Transversal | — | — | — | USD 600 infraestructura y contingencia | USD 600 |
| **Total** | **120** | **70** | **USD 3 800** | **USD 1 200** | **USD 5 000** |

Las comisiones de testnet las paga el operador y no son una partida. El trabajo previo autofinanciado (unas 45 horas de diseño y la prueba de concepto en testnet) no se carga a esta instaward.

---

## 5. Plan de ejecución de 30 días

Calendario de lunes a viernes, Perú. El plan se mantiene como datos validados por esquema en `planning/` y se comprueba en integración continua, igual que el sprint S00.

### Semana 1

- `sign-auth-entry` genérico
- Relayer con lista permitida, tope de gasto, límite de frecuencia y registro de rechazos
- Registro de comisiones enlazado a las entradas de autorización
- Empaquetado del kit y guías
- Investigación de usuario: guía de entrevista y sesiones agendadas con ambas OPP

**Resultado esperado**
Una cuenta de rol con 0 XLM autoriza una invocación a un contrato distinto del de ejemplo; el relayer rechaza tres violaciones de política, en testnet y en pruebas.

### Semana 2

- Contrato del registro T0–T8
- Guardas G1, G2, G6, G7, G8 y G10
- Variantes de génesis A y B
- Consulta del certificado de hito y contrato consumidor
- Política de renta de estado

**Resultado esperado**
Ciclo 2027 de Tocache abierto en testnet; un paso omitido y un ciclo duplicado rechazados por la red.

**Punto de control (fin de la semana 2):** si las pruebas de guardas no pasan, el plan B conserva T0–T4 con G1, G2, G6 y G7 y el certificado de hito, y traslada T5–T8 con G8 y G10 a la siguiente iteración. E1 y E4 no se recortan.

### Semana 3

- Ingesta v2 con ambos perfiles
- INC-01 cerrada sobre descargas directas del portal
- Tocache 2027 y La Punta 2023–2027 anclados
- Sesiones en terreno en Tocache y La Punta

**Resultado esperado**
Documentos reales de ambas municipalidades anclados como transiciones firmadas por dos claves de rol distintas con 0 XLM.

### Semana 4

- Verificador ciudadano en vivo sobre el recorrido
- Medición de comisiones por transición y por ciclo
- Pruebas de punta a punta, documentación y video actualizado
- Nota de preparación; requerimientos firmados por ambas OPP

**Resultado esperado**
Un revisor verifica la cadena completa solo con el repositorio y el recorrido; informe de comisiones publicado.

---

## 6. Evidencia de cumplimiento

### Entregable 1

**Evidencia**

- Versión etiquetada del Signer Kit v1 en el repositorio
- Hashes en testnet: invocación autorizada por el rol a un contrato distinto del de ejemplo; transmisión por un tercero
- Informe de pruebas de los tres rechazos del relayer
- Salida del verificador de conformidad (C1–C6)

### Entregable 2

**Evidencia**

- ID del contrato del registro en testnet
- Hashes de las filas 3 y 4 de `evidence/transacciones.md` (apertura del ciclo y duplicado rechazado)
- Hash de un paso omitido rechazado
- Informe de pruebas por guarda (enlace a la integración continua)
- Hashes del contrato consumidor (hito presente y ausente)
- Documento de política de renta de estado

### Entregable 3

**Evidencia**

- Validador de ingesta v2 con sus casos de prueba
- `evidence/documentos.md` actualizado con huellas verificadas
- Hashes de las transiciones ancladas de ambas municipalidades
- Documento de requerimientos firmado o confirmado por cada OPP

### Entregable 4

**Evidencia**

- Verificador en vivo en signerkit.govtechpe.work
- Recorrido documentado de una verificación independiente
- Informe de comisiones
- Video de demostración actualizado
- Nota de preparación para mainnet
- Repositorio con la integración continua en verde

### Lista de verificación de evidencia

| Entregable | Evidencia presente | Parcial | Ausente |
|---|---|---|---|
| E1 — Signer Kit v1 | ☐ | ☐ | ☐ |
| E2 — Registro del ciclo T0–T8 | ☐ | ☐ | ☐ |
| E3 — Ingesta v2 e investigación de usuario | ☐ | ☐ | ☐ |
| E4 — Verificador ciudadano, comisiones y preparación | ☐ | ☐ | ☐ |

### Definición de terminado (para todo entregable)

- Reproducible desde un clon limpio siguiendo el README
- Sin claves ni secretos en el código
- Ninguna salida contiene datos personales
- Cada enlace citado abre y muestra lo que el texto afirma; donde el repositorio no registra un valor, dice `SIN DATO` en lugar de estimarlo
- Integración continua en verde en el commit de la versión

---

## 7. Alineación con el siguiente paso

Al terminar esta instaward, el registro cubrirá el nivel ciclo del proceso y el kit estará completo. La siguiente iteración (USD 8 000, 6 semanas), ya descrita en el repositorio, agrega:

- las transiciones de nivel proyecto T9–T13 (hitos 7 y 8 del recorrido), incluida la sustitución con las reglas R1–R7;
- la tokenización: un token no transferible por proyecto priorizado sobre SEP-50;
- la multifirma por rol y ciclo para el comité de vigilancia (G9);
- el primer perfil de beneficio, el Programa del Vaso de Leche, con entregas mensuales atestiguadas por los comités, sin mover un sol en la cadena y sin tocar el padrón de beneficiarias.

En las etapas 1 y 2 TechGob paga las comisiones. Después, el rol de operador pasa al Laboratorio de Innovación Digital de la SGTD, y el traspaso ya probado en testnet lo convierte en un cambio de configuración. El camino a mainnet pasa por una auditoría externa (Soroban Security Audit Bank) y una postulación al SCF Build Award.

---

## 8. Métricas de éxito

| Métrica | Meta del sprint |
|---|---|
| Claves de rol institucionales distintas que firman con 0 XLM | 2 (una por municipalidad) |
| Piezas del kit probadas en testnet | 4 de 4 (hoy 3 de 4) |
| Transiciones del ciclo registradas | T0–T8 donde exista el documento fuente |
| Transiciones inválidas rechazadas por la red | 100 % de los casos de prueba |
| Guardas ejecutadas en testnet | 6 (G1, G2, G6, G7, G8 y G10); hoy 0 |
| Comisión por transición y por ciclo | Medida y publicada |
| Verificaciones independientes de terceros | Al menos 1 por municipalidad |
| Datos personales en cargas ancladas | 0 |

---

## 9. Riesgos y mitigaciones

| Riesgo | Probabilidad | Impacto | Mitigación |
|---|---|---|---|
| Retraso en documentos municipales (constancia de publicación de la ordenanza de Tocache; versiones públicas de actas y cuadros de puntaje sin columna de DNI) | Media | Medio | Solicitudes emitidas al inicio del sprint (DEP-02, DEP-03); las transiciones faltantes se informan como pendientes y nunca se completan con supuestos |
| Retraso en la firma de requerimientos por las OPP | Media | Bajo | Se acepta como equivalente una confirmación por correo o un acta de reunión |
| Reinicio trimestral de testnet que rompe los enlaces al explorador | Media | Bajo | Cada corrida está automatizada y fechada; el recorrido guarda sus datos en dos arreglos que se actualizan tras repetir la corrida |
| Costo de renta de estado subestimado | Media | Alto | La política de renta es parte de E2 y su costo se mide en E4 |
| Una guarda no es implementable tal como está especificada | Baja | Medio | Cambio propuesto por pull request y aprobado por la dueña de producto; las reglas que vienen de la norma no se abandonan por conveniencia |
| Un operador único concentra poder | Baja | Alto | Las entradas se publican y cualquier tercero puede transmitirlas; el traspaso ya está probado; el operador de destino es el laboratorio de la SGTD |
| Datos personales llegan a la cadena | Baja | Alto | Regla de admisión por campo, privacidad por defecto, rechazo estructural, validador en dos capas y un caso de prueba que debe fallar |

---

## 10. Protección de datos y seguridad

- Solo se anclan documentos públicos por mandato legal. Nunca datos personales, ni la huella de un identificador personal.
- Las claves pertenecen a roles y ciclos, no a personas.
- El esquema lo hace cumplir: cada campo declara su regla de admisión; un campo sin anotación queda fuera de la cadena; se rechazan los campos no declarados y los nombres de campo que sugieren datos personales.
- Sin secretos en el repositorio; los scripts leen las claves desde el almacén de la CLI de Stellar.
- Marco: Ley N.° 29733 y Decreto Supremo N.° 016-2024-JUS. El registro no reemplaza la evaluación de protección de datos que corresponde a cada entidad.

---

## Anexo — Coherencia con los artefactos públicos

| Afirmación de este SOW | Repositorio | Video | Recorrido interactivo |
|---|---|---|---|
| Firmar sin tener XLM | README, evidencia de HU-01 | Título y apertura | Piezas 1, 3 y 4 marcadas como probadas |
| El relayer restringido está por construir | `signer-kit/README.md` | — | Pieza 2: "No implementado · lo financia esta iteración" |
| Alcance T0–T8 con guardas | README, "Alcance de esta postulación a instaward" | "05 · next · the cycle registry, in development", T0–T8 | Hitos 1–6; guardas "especificadas · contrato no desplegado" |
| Un paso legal omitido es rechazado por la red | `docs/maquina-estados.md`, ADR-001 | "skips a legal step → rejected by the network" | Descripción de las guardas |
| Certificado de hito | `docs/statement-of-work.md`, sección 4 | "milestone certificate — a precondition a disbursement can require" | — |
| Diseñado sobre documentos municipales reales del Perú | `evidence/documentos.md`, contrato de datos | "Está diseñado sobre documentos municipales reales del Perú" | 16 inconsistencias de la ordenanza de Tocache |
| Fuera de alcance | README, "Fuera de alcance por ahora" | — | Hitos 7–8 mostrados como especificados |
