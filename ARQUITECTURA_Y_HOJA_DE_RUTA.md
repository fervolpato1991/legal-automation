# Sistema Jurídico --- Arquitectura, Estado y Hoja de Ruta

**Versión documental:** consolidación posterior a la inspección del
28/10/2026\
**Repositorio conocido:**
`https://github.com/fervolpato1991/legal-automation.git`\
**Estado:** documento de arquitectura y plan; no certifica que todas las
funcionalidades descritas estén probadas.

## 1. Propósito del proyecto

El proyecto busca construir un sistema de gestión y automatización de
procesos jurídicos.

El objetivo no es solamente almacenar expedientes, actuaciones y
documentos, sino representar un proceso jurídico de forma estructurada
para que el sistema pueda:

-   saber en qué etapa se encuentra cada expediente;
-   registrar qué ocurrió y cuándo;
-   detectar qué debería ocurrir a continuación;
-   detectar qué está pendiente;
-   generar plazos y documentos a partir de reglas verificables;
-   mantener trazabilidad de las decisiones automáticas;
-   mostrar visualmente el flujo procesal;
-   reducir la necesidad de recordar manualmente qué hacer en cientos de
    expedientes;
-   posteriormente detectar nuevos despachos/proveídos y convertirlos en
    acciones o tareas;
-   evolucionar hacia automatización de procesos;
-   eventualmente generalizar el motor para otros dominios;
-   dejar abierta una vía futura de monetización.

### 1.1 Prioridad inicial del dominio

La primera especialización será en **juicios de apremio en la Provincia
de Buenos Aires**, aprovechando el acceso disponible al portal SNyPE
para estudiar procesos, etapas, despachos/proveídos, modelos de
escritos, plazos y patrones repetitivos.

La estrategia es construir primero un motor sólido sobre un dominio
jurídico bien delimitado y luego generalizarlo.

El material real que se use para estudiar patrones deberá manejarse con
minimización de datos y respetando las condiciones de acceso y uso de
las fuentes. Los datos de prueba del repositorio deben ser ficticios o
anonimizados.

### 1.2 Condición arquitectónica: Asistente Procesal

El objetivo de largo plazo no es únicamente gestionar expedientes ni
mantener un catálogo de modelos de escritos. El sistema debe evolucionar
hacia un **Asistente Procesal** capaz de analizar el contexto de un
expediente, identificar acciones procesales pendientes o posibles,
explicar por qué las propone, ayudar al usuario a destrabar situaciones
en las que no conoce el siguiente paso y, cuando una acción requiera un
escrito, seleccionar un modelo compatible según sus metadatos y el
contexto procesal.

Los modelos de escritos serán un componente del conocimiento procesal,
no el centro del sistema.

El sistema deberá distinguir entre:

-   acciones procesales;
-   modelos de escritos;
-   documentos concretos;
-   reglas procesales;
-   antecedentes de uso;
-   conocimiento suficientemente respaldado;
-   situaciones para las cuales no existe todavía conocimiento
    suficiente.

Cuando no exista un modelo adecuado, el sistema deberá informar esa
ausencia, permitir que el usuario incorpore un nuevo modelo y,
eventualmente, utilizar escritos anteriores de situaciones similares
como referencia para asistir en la elaboración de uno nuevo.

La arquitectura deberá permitir incorporar progresivamente búsqueda
contextual, similitud entre antecedentes, asistencia mediante lenguaje
natural, IA generativa, recuperación de conocimiento relevante y
razonamiento asistido sobre el contexto procesal.

El funcionamiento fundamental no deberá depender inicialmente de una IA.
La IA deberá apoyarse sobre el modelo procesal estructurado, las reglas,
los datos y los antecedentes registrados.

### 1.3 Acción antes que escrito

El asistente no debe limitarse a responder "qué escrito usar". Debe
razonar primero sobre:

``` text
¿Qué está ocurriendo?
        ↓
¿En qué etapa está el expediente?
        ↓
¿Qué acción procesal corresponde o podría corresponder?
        ↓
¿Por qué?
        ↓
¿La acción requiere un escrito?
        ↓
¿Qué modelo es compatible?
        ↓
¿Existen antecedentes útiles?
```

Por lo tanto, `AccionProcesal` debe poder existir independientemente de
`ModeloEscrito`.

Ejemplos conceptuales:

``` text
NOTIFICAR_RESOLUCION
REITERAR_OFICIO
ACREDITAR_NOTIFICACION
CONTESTAR_TRASLADO
SOLICITAR_INTIMACION
CONTROLAR_VENCIMIENTO
```

El mismo tipo de acción puede resolverse mediante un escrito, una
actuación interna, una tarea de seguimiento, una notificación, una
revisión manual u otro mecanismo.

### 1.4 Ingesta de información judicial externa

El sistema deberá poder incorporar información proveniente de diferentes
fuentes judiciales, incluyendo SNyPE/NYPE, MEV, sistemas del PJN y otros
portales relevantes.

Mecanismos posibles:

-   carga manual;
-   copia o importación de información;
-   archivos y documentos;
-   integraciones automatizadas, cuando resulte técnica y jurídicamente
    viable.

Las integraciones estarán desacopladas del núcleo procesal mediante
adaptadores o servicios específicos por fuente. El motor procesal no
deberá depender de la estructura particular de un portal.

``` text
FUENTE JUDICIAL
     ↓
ADAPTADOR / CONECTOR
     ↓
ENTRADA JUDICIAL
     ↓
NORMALIZACIÓN
     ↓
VALIDACIÓN
     ↓
IDENTIFICACIÓN DEL EXPEDIENTE
     ↓
ACTUACIÓN / HECHO PROCESAL
     ↓
EVENTO
     ↓
MOTOR PROCESAL
```

### 1.5 Ingesta segura y validada

La información externa no deberá convertirse automáticamente en una
actuación ni desencadenar acciones procesales sin normalización,
validación y, cuando corresponda, confirmación del usuario.

Se deberá conservar, cuando esté disponible:

-   origen y fuente judicial;
-   fecha de incorporación;
-   fecha de origen;
-   referencia externa;
-   contenido original o representación suficiente para auditoría;
-   expediente identificado y grado de certeza de la correspondencia;
-   actuación generada;
-   eventos y reglas derivados;
-   validaciones y confirmaciones realizadas.

``` text
INFORMACIÓN EXTERNA
        ↓
ENTRADA JUDICIAL
        ↓
NORMALIZACIÓN
        ↓
VALIDACIÓN / CONFIRMACIÓN
        ↓
ACTUACIÓN
        ↓
EVENTO
        ↓
REGLA
        ↓
ACCIÓN / TAREA / PLAZO / DOCUMENTO
```

## 2. Arquitectura conceptual del núcleo

El núcleo se está construyendo alrededor de esta cadena:

``` text
EVENTO
   ↓
ACTUACIÓN / HECHO PROCESAL
   ↓
REGLA PROCESAL
   ↓
CAMBIO DE ESTADO
   ↓
CONSECUENCIAS
   ├── PLAZO
   ├── DOCUMENTO
   ├── TAREA / ACCIÓN PENDIENTE
   └── EVENTO DE SISTEMA
   ↓
TIMELINE / WORKFLOW
   ↓
DETECCIÓN DE PENDIENTES
   ↓
ASISTENCIA Y AUTOMATIZACIÓN CONTROLADA
```

El expediente no debe ser solo una colección de datos, sino una
representación observable y eventualmente ejecutable de un proceso.

**Distinción esencial:** el orden temporal no equivale a causalidad. Una
relación causal debe derivarse de referencias explícitas ---por ejemplo,
una actuación que dispara una regla y esta que crea un plazo--- y no
inferirse simplemente porque dos eventos aparecen uno después del otro.

## 3. Capas arquitectónicas objetivo

La arquitectura debe crecer por capas, manteniendo el núcleo procesal
determinista y auditable.

### Capa 1 --- Fuentes y captura

Responsabilidades: - recibir carga manual, documentos, datos importados
y, a futuro, conectores; - conservar metadatos de origen; - separar la
recepción de información de su aceptación como hecho procesal; -
detectar duplicados de entradas cuando sea posible.

### Capa 2 --- Ingesta, normalización y validación

Responsabilidades: - representar una `EntradaJudicial` antes de crear
una actuación; - extraer texto y metadatos sin perder la referencia al
original; - normalizar fechas, identificadores, tipos de despacho y
expediente candidato; - validar campos obligatorios y
correspondencias; - registrar incertidumbre y solicitar confirmación
cuando haga falta.

La extracción mediante IA, si se incorpora, propondrá datos
estructurados; no será por sí sola autoridad para modificar el
expediente.

### Capa 3 --- Núcleo procesal verificable

Responsabilidades: - expediente y contexto procesal; -
actuaciones/hechos; - catálogo de etapas y estados; - reglas versionadas
y explícitas; - evaluación de condiciones; - transiciones de estado; -
plazos, documentos y tareas; - historial y eventos auditables.

Esta capa es la fuente de verdad operativa. Debe poder funcionar sin un
LLM.

### Capa 4 --- Inteligencia operativa

Responsabilidades: - pendientes por expediente; - plazos próximos a
vencer; - expedientes sin movimiento; - detección de workflow
incompleto; - tareas derivadas; - prioridades y alertas; - vistas de
timeline y workflow; - explicación de la regla y los datos que
originaron cada resultado.

Las recomendaciones deben incluir motivo, evidencia disponible,
incertidumbre y acciones necesarias para confirmarlas.

### Capa 5 --- Asistente Procesal e IA

Responsabilidades futuras: - interpretar preguntas en lenguaje
natural; - recuperar el contexto del expediente; - generar candidatos de
acciones; - recuperar reglas, modelos y antecedentes relevantes; -
resumir despachos; - explicar opciones y faltantes; - asistir en la
redacción de borradores.

La IA no debe inventar normas, hechos, plazos, relaciones causales ni
autoridad. Si la evidencia es insuficiente, debe indicarlo. Sus salidas
deben poder rastrearse hasta reglas, fuentes, actuaciones o antecedentes
identificables.

### Capa 6 --- Ejecución controlada

Responsabilidades: - presentar acciones sugeridas; - permitir revisión y
aprobación humana; - generar borradores sin presentarlos
automáticamente; - registrar quién confirmó una acción y cuándo; -
separar operaciones reversibles de acciones externas o de consecuencias
jurídicas; - disponer de idempotencia, manejo de errores y registro de
auditoría.

No se debe presentar ni enviar un escrito, modificar información
judicial externa ni ejecutar una acción de consecuencias relevantes sin
autorización explícita y controles apropiados.

## 4. Stack tecnológico

### Backend

-   Python
-   Flask
-   SQLAlchemy
-   SQLite en la etapa actual
-   Jinja2

### Frontend

-   HTML
-   Bootstrap
-   HTMX
-   Mermaid
-   JavaScript progresivo
-   CSS separado

### Filosofía frontend

No se busca migrar prematuramente a React ni convertir la aplicación en
una SPA.

``` text
Flask + Jinja
      +
HTMX
      +
JavaScript progresivo
      +
Mermaid
```

La prioridad es aprender JavaScript mientras se agrega interactividad
real sin reescribir la aplicación. La tecnología podrá revisarse si
aparecen requisitos concretos que la arquitectura actual no pueda
satisfacer.

## 5. Estructura conocida del proyecto

Estructura conocida hasta la inspección:

``` text
Proyecto-Juridico/
├── reset_db.py
├── migrations/
│   ├── env.py
│   └── versions/
├── app/
│   ├── crud/
│   ├── db/
│   ├── models/
│   ├── services/
│   ├── web/
│   │   └── templates/
│   └── static/
│       ├── js/
│       │   └── workflow.js
│       └── css/
│           └── styles.css
├── alembic.ini
└── README.md
```

Esta estructura es orientativa, no un inventario exhaustivo. La
inspección identificó además `app/web/templates/components/`,
`timeline_service.py`, `workflow_visual_service.py` y `diff_app.txt`.
Debe revisarse el árbol real antes de declarar definitivo el inventario.

**Advertencia:** `reset_db.py` ejecuta `drop_all()` y `create_all()`.
Elimina las tablas y las recrea. No debe ejecutarse como paso ordinario
de recuperación ni sobre una base cuyos datos se quieran conservar.

## 6. Modelos actuales y evolución prevista

### 6.1 Modelos existentes

#### `Expediente`

Campos conocidos: `id`, `caratula`, `numero`, `jurisdiccion`, `juzgado`,
`tipo_proceso`, `estado_id`.

Relaciones conocidas: estado, partes, actuaciones, plazos, documentos e
historial de estados.

#### `Actuacion`

Campos conocidos: `id`, `tipo`, `fecha`, `descripcion`, `expediente_id`.
Representa una actuación procesal registrada.

#### `Documento`

Campos conocidos: `id`, `tipo`, `contenido`, `created_at`,
`expediente_id`, con referencias adicionales a actuación y regla.
Representa documentos almacenados o generados.

#### `Plazo`

Campos conocidos: `id`, `tipo`, `fecha_inicio`, `fecha_vencimiento`,
`cumplido`, `expediente_id`, con referencias adicionales a actuación y
regla. Existe una restricción de unicidad para cierta combinación de
expediente, tipo y fecha de vencimiento.

#### `ReglaProcesal`

Campos conocidos: `id`, `evento`, `estado_destino`, `generar_documento`,
`template`, `crear_plazo`, `dias_plazo`, `condicion`, `activa`, `unica`.

#### `EstadoProcesal`

Representa un estado procesal. En el código revisado, el cambio de
estado busca un registro por nombre.

#### `HistorialEstado`

Registra transiciones, con estado anterior/nuevo, fecha, expediente y
referencias opcionales a actuación/regla.

#### `EventoSistema`

Registra sucesos del sistema, con tipo, descripción, fecha, expediente y
referencias opcionales a actuación/regla, además de un campo `datos`.

#### `Parte`

Representa partes relacionadas con un expediente.

### 6.2 Entidades conceptuales futuras

No deben agregarse todas de una vez. Deben incorporarse cuando exista un
caso de uso concreto y un diseño revisado.

#### `AccionProcesal`

Representa una acción posible o requerida, independientemente de si
necesita escrito. Debería permitir identificar tipo, dominio, etapa,
condiciones previas, estado de resolución, urgencia, origen, evidencia y
explicación.

#### `ModeloEscrito`

Representa una plantilla reutilizable con metadatos como tipo de acción,
etapa, tipo de proceso, evento desencadenante, condiciones,
fuero/jurisdicción y variables requeridas.

#### `EntradaJudicial`

Representa información recibida de una fuente antes de confirmarse como
actuación. Debe conservar origen, fechas, referencia externa, contenido
original o representación auditable, estado de validación y
correspondencia candidata con expediente.

#### `TareaProcesal`

Representa una tarea de seguimiento o acción pendiente que no
necesariamente requiere un escrito. Debe poder vincularse a su origen y
a la regla o recomendación que la produjo.

#### Versionado y evidencia

Las reglas, modelos y fuentes de conocimiento deben poder versionarse o
conservar suficiente información para reconstruir por qué una
recomendación se generó en un momento determinado.

No conviene diseñar una gran estructura de entidades futuras sin validar
primero los flujos actuales. El objetivo es evolucionar de manera
incremental.

## 7. Servicios conocidos y contratos a fortalecer

### `workflow_service.py`

Responsabilidad actual: buscar estado destino, registrar historial y
actualizar el estado del expediente.

**Riesgo observado:** si no encuentra el estado destino, retorna sin
realizar el cambio; el llamador no recibe un resultado estructurado que
confirme éxito o fallo.

**Evolución requerida:** devolver un resultado explícito, no crear
historial de una transición fallida y permitir que la transacción se
confirme o revierta coherentemente.

### `regla_service.py`

Responsabilidades actuales: buscar reglas asociadas a una actuación,
evaluar condiciones, evitar ciertas duplicaciones, cambiar estados,
crear plazos, generar documentos y registrar eventos.

**Riesgos observados:** - condiciones desconocidas aceptadas por
defecto; - control `unica` centrado en documentos, no en todas las
consecuencias; - cálculo simple de días corridos; - evento de cambio de
estado que puede registrarse aunque no ocurra el cambio; - trazabilidad
insuficiente de los objetos creados.

**Evolución requerida:** condiciones explícitas, fallo seguro,
resultados estructurados, idempotencia, relaciones causales verificables
y transacciones coherentes.

### `event_service.py`

Agrega eventos a la sesión, pero no hace `commit`. El control
transaccional queda en el llamador. Esto debe mantenerse explícito en
los contratos de servicio.

### `timeline_service.py`

La versión observada consulta eventos de sistema. Debe decidirse si el
timeline representa solo eventos o una línea temporal unificada de
actuaciones, documentos, plazos y otros elementos. En ambos casos se
debe preservar el origen y evitar omisiones silenciosas.

### `workflow_visual_service.py`

Genera Mermaid a partir de eventos ordenados cronológicamente. Debe
corregir el escape de texto y evitar representar la mera sucesión
temporal como causalidad demostrada.

## 8. Flujo objetivo para registrar una actuación

El flujo debe ser transaccional, trazable y seguro ante errores:

``` text
Solicitud de usuario
        ↓
Validar expediente y datos
        ↓
Crear actuación/hecho
        ↓
Identificar reglas aplicables
        ↓
Evaluar condiciones explícitas
        ↓
Proponer/ejecutar consecuencias permitidas
        ↓
Validar cada resultado
        ↓
Registrar eventos y relaciones causales
        ↓
Confirmar transacción
        ↓
Actualizar timeline / workflow / pendientes
```

Una regla no debe considerarse ejecutada solo porque se intentó
ejecutar. Cada consecuencia debe registrar su resultado real. Ante un
error, no se deben dejar estados parciales o eventos que describan
resultados inexistentes.

## 9. Timeline, workflow e Inspector Procesal

### 9.1 Timeline

Debe mostrar la evolución temporal del expediente. Hay que resolver si
se construye desde eventos del sistema o si integra actuaciones,
documentos, plazos y tareas. Una vista unificada deberá indicar el tipo
y origen de cada elemento.

La ruta conocida es `/expediente/<id>/timeline`. Se ha modificado para
utilizar el servicio de eventos, por lo que debe probarse si desaparecen
elementos sin evento asociado.

### 9.2 Workflow visual

Mermaid permite representar un grafo procesal. Debe diferenciar: -
secuencia temporal; - relación de origen y consecuencia; - transiciones
de estado; - tareas pendientes; - relaciones no confirmadas.

Solo se mostrarán flechas causales cuando exista una referencia
explícita que las respalde.

### 9.3 Interacción Timeline ↔ Workflow

Archivo JavaScript conocido: `app/static/js/workflow.js`.

Objetivo: - al seleccionar un evento del timeline, resaltar el nodo
correspondiente; - al seleccionar un nodo, resaltar y desplazar la vista
hacia el elemento del timeline; - limpiar resaltados anteriores; -
conservar la interacción después de swaps HTMX; - manejar nodos o
eventos sin correspondencia.

Esta funcionalidad está pendiente de validación integral.

### 9.4 Inspector Procesal

Una vez validado el núcleo visual, el inspector permitirá explorar un
evento y sus relaciones:

``` text
EVENTO
- tipo, fecha, descripción y origen

ACTUACIÓN / HECHO
- tipo, descripción y expediente

REGLA
- regla aplicada, versión y condición evaluada

ESTADO
- estado anterior, estado nuevo y resultado

CONSECUENCIAS
- plazo, documento, tarea u otra acción

TRAZABILIDAD
- fuente, relaciones y evidencia disponible
```

El inspector debe exponer lo que se conoce y señalar explícitamente lo
que no se conoce. No debe fabricar relaciones causales a partir de la
proximidad temporal.

## 10. Estado técnico observado al 28/10/2026

El detalle de los hallazgos se conserva en `ESTADO_ACTUAL.md` y la
secuencia de revisión en `BITACORA_INSPECCION.md`.

Resumen: - Python 3.12.0 funciona en `venv_inspeccion`. - Los entornos
virtuales anteriores apuntan a una instalación de Python 3.10 que ya no
existe. - No se encontró manifiesto de dependencias en la raíz. - Hay
cambios locales y archivos no rastreados que deben preservarse. - La
base SQLite de prueba existe; los datos son ficticios. - No existe
`alembic_version`. - `migrations/env.py` parece tener una importación
incompatible con la estructura conocida. - Hay dos rutas para crear
actuaciones en la misma URL. - Las condiciones desconocidas de reglas se
aceptan por defecto. - La transición de estado no comunica éxito/fallo
al servicio que registra eventos. - El timeline nuevo puede omitir
objetos sin evento. - El workflow Mermaid puede sugerir causalidad por
simple orden temporal. - No se ha validado el funcionamiento integral en
navegador.

## 11. Hoja de ruta consolidada

Las marcas históricas de "implementado" deben entenderse como
afirmaciones del documento previo, no como garantía de funcionamiento.
Las etapas se consideran terminadas solo después de pruebas
reproducibles.

### Fase 1 --- Núcleo del sistema

**Estado documental anterior:** modelos y CRUD básico declarados
implementados.\
**Situación actual:** el código y los modelos existen, pero faltan
pruebas integrales.

-   [x] Modelos principales presentes en el código
-   [x] Operaciones básicas para expedientes y actuaciones presentes
-   [x] Modelos para estados, plazos, documentos, reglas, historial y
    eventos presentes
-   [ ] Validar contratos, transacciones y relaciones entre servicios
-   [ ] Pruebas automatizadas mínimas

### Fase 2 --- Observabilidad procesal

-   \[\~\] Timeline modificado para usar eventos
-   \[\~\] Workflow Mermaid presente en cambios locales
-   [ ] Definir semántica unificada del timeline
-   [ ] Validar renderizado y refresco HTMX
-   [ ] Validar interacción bidireccional Timeline ↔ Workflow
-   [ ] Corregir el escape de Mermaid
-   [ ] Separar cronología de causalidad
-   [ ] Construir Inspector Procesal después de estabilizar lo anterior

### Fase 3 --- Modelado jurídico de apremios

-   [ ] Catálogo de etapas
-   [ ] Catálogo de actuaciones frecuentes
-   [ ] Estados procesales específicos
-   [ ] Reglas por etapa
-   [ ] Cómputo de plazos respaldado y configurable
-   [ ] Modelos de escritos con metadatos
-   [ ] Tipos de despachos/proveídos
-   [ ] Consecuencias habituales
-   [ ] Condiciones procesales explícitas
-   [ ] Caminos alternativos del proceso

Usar material práctico para el modelado con minimización de datos y
respetando las condiciones de las fuentes. No convertir ejemplos
ficticios en reglas jurídicas reales sin validación.

### Fase 4 --- Automatización operativa

-   [ ] Pendientes por expediente
-   [ ] Acciones sugeridas y próximos pasos
-   [ ] Plazos próximos a vencer
-   [ ] Detección de expedientes sin movimiento
-   [ ] Detección de workflows incompletos
-   [ ] Alertas y tareas derivadas
-   [ ] Priorización explicable
-   [ ] Relación explícita entre origen, regla y consecuencia

### Fase 5 --- Ingesta de información externa

-   [ ] Modelo de entrada judicial
-   [ ] Importación manual y desde archivos
-   [ ] Normalización y validación
-   [ ] Identificación de expediente con manejo de incertidumbre
-   [ ] Confirmación humana cuando corresponda
-   [ ] Adaptadores desacoplados para fuentes
-   [ ] Evaluar conectores automatizados solo tras estudiar viabilidad
    técnica, jurídica y condiciones de uso

### Fase 6 --- Asistente Procesal

-   [ ] Consultas en lenguaje natural sobre expedientes y pendientes
-   [ ] Candidatos de acciones procesales
-   [ ] Explicación de recomendaciones
-   [ ] Recuperación contextual de reglas, modelos y antecedentes
-   [ ] Compatibilidad contextual de modelos de escritos
-   [ ] Detección de información faltante
-   [ ] Indicación expresa de evidencia insuficiente
-   [ ] Revisión humana de borradores y acciones relevantes

Niveles de respaldo propuestos:

``` text
ALTO
Regla configurada + contexto compatible + evidencia identificable

MEDIO
Antecedentes similares + contexto suficiente, con incertidumbre explicada

INSUFICIENTE
No existe regla, modelo o evidencia suficiente
```

No debe inventarse una solución procesal cuando el respaldo es
insuficiente.

### Fase 7 --- Generalización del motor

-   [ ] Separar progresivamente motor de workflow y dominio jurídico
-   [ ] Mantener apremios como primer dominio
-   [ ] Definir contratos genéricos solo a partir de necesidades
    demostradas
-   [ ] Evitar abstracciones prematuras

Modelo conceptual:

``` text
                MOTOR
                  │
        ┌─────────┴─────────┐
        │                   │
     Jurídico          Otros dominios
        │
     Apremios
```

El motor podrá representar eventos, reglas, estados, consecuencias,
tareas, plazos, documentos e historial, independientemente del dominio.

### Fase 8 --- Monetización

Evaluar después de validar utilidad y adopción: - SaaS para estudios; -
licencias; - automatización para áreas jurídicas; - módulos
especializados; - servicios de automatización; - funcionalidades
premium.

La monetización no debe dirigir prematuramente la arquitectura.

## 12. Principios de desarrollo

### Principio 1 --- No automatizar a ciegas

Toda automatización debe tener evento de origen, regla identificable,
resultado real y trazabilidad.

### Principio 2 --- Explicar por qué ocurrió algo

Ejemplo: "Se creó el plazo X porque ocurrió la actuación Y y se ejecutó
la regla Z", con referencias verificables a esos objetos.

### Principio 3 --- Primero apremios, después generalización

Construir un dominio bien delimitado antes de intentar representar todo
el derecho.

### Principio 4 --- Observabilidad antes que IA

``` text
registrar
→ modelar
→ relacionar
→ visualizar
→ detectar
→ sugerir
→ automatizar con control
```

### Principio 5 --- JavaScript progresivo

Mejorar la interfaz actual sin migrar de arquitectura solo para
incorporar otro framework.

### Principio 6 --- Fallo seguro

Una condición desconocida, un estado destino inexistente o una entrada
externa ambigua no deben habilitar una acción automáticamente. El
sistema debe detenerse, registrar el motivo y solicitar revisión.

### Principio 7 --- Separación entre sugerir y ejecutar

El sistema puede proponer una acción, pero las operaciones de
consecuencias relevantes requieren controles y autorización humana.

## 13. Checklist de continuidad después de una pausa

Antes de iniciar una etapa nueva:

1.  Preservar el estado de Git y revisar los cambios locales.
2.  Iniciar la aplicación en un entorno reproducible.
3.  Abrir un expediente ficticio.
4.  Verificar timeline.
5.  Verificar workflow Mermaid.
6.  Crear una actuación de prueba.
7.  Comprobar reglas aplicables.
8.  Comprobar el resultado del cambio de estado.
9.  Comprobar plazo y documento.
10. Comprobar eventos y relaciones causales.
11. Probar Timeline ↔ Workflow.
12. Revisar la consola del navegador.
13. Confirmar que no hay errores ni consecuencias duplicadas.
14. Recién entonces continuar con funcionalidades nuevas.

No ejecutar `reset_db.py` como parte de este checklist.

## 14. Punto de continuidad inmediato

Orden recomendado para retomar el trabajo:

1.  Preservar todos los cambios locales.
2.  Revisar `diff_app.txt` y los diffs.
3.  Revisar `.gitignore` y el árbol real.
4.  Inventariar dependencias e imports.
5.  Resolver la configuración de Alembic sin ejecutar migraciones.
6.  Revisar el mapa de rutas y consolidar la creación de actuaciones.
7.  Hacer explícitos los resultados de cambios de estado y la evaluación
    segura de reglas.
8.  Definir timeline y causalidad.
9.  Recuperar la ejecución de la aplicación.
10. Validar la interfaz y las pruebas.
11. Construir el Inspector Procesal.
12. Empezar el modelado específico de apremios.
13. Incorporar pendientes y automatización operativa.

## 15. Mantenimiento de la documentación

Cada cambio importante debe reflejarse en: - este documento, para
arquitectura y hoja de ruta; - `ESTADO_ACTUAL.md`, para estado
verificado; - `BITACORA_INSPECCION.md`, para evidencia y decisiones
cronológicas.

Usar las marcas: - `[ ]` pendiente; - `[x]` implementado y probado; -
`[~]` en desarrollo o pendiente de validación.

No marcar una función como completada solo porque se escribió el código.
Registrar la prueba que respalda el estado.

El objetivo es retomar el proyecto después de una pausa sin reconstruir
mentalmente todo el contexto y sin perder la trazabilidad de las
decisiones.

---

# Evolución tecnológica y arquitectura futura

Referencia: EVOLUCION_TECNOLOGICA_Y_ARQUITECTURA_FUTURA

## 1. Criterio rector

La evolución del Sistema Jurídico debe priorizar la confiabilidad del núcleo procesal antes que la incorporación de herramientas tecnológicas adicionales.

El objetivo es evolucionar desde una aplicación de registro y gestión de expedientes hacia un Asistente Procesal capaz de identificar acontecimientos, evaluar reglas, determinar consecuencias, detectar pendientes y asistir al profesional en la toma de decisiones.

La arquitectura debe conservar trazabilidad, explicabilidad, integridad de los datos y supervisión humana.

No se incorporarán tecnologías por novedad o prestigio. Cada incorporación deberá resolver una necesidad concreta y justificable.

## 2. Principios arquitectónicos

- Mantener inicialmente la arquitectura modular basada en Flask, SQLAlchemy, SQLite, Jinja2, Bootstrap, HTMX y JavaScript.
- Evitar migraciones tecnológicas o arquitecturas distribuidas que no estén justificadas por necesidades reales.
- Separar el motor determinístico de reglas procesales de los componentes de inteligencia artificial.
- Registrar la procedencia de los datos y las consecuencias derivadas de cada acontecimiento.
- Diferenciar hechos confirmados, inferencias, propuestas automáticas y decisiones aprobadas por un profesional.
- Preservar el historial de modificaciones y permitir auditar las decisiones procesales.
- Incorporar nuevas tecnologías progresivamente, mediante cambios pequeños, verificables y documentados.

## 3. Trazabilidad de decisiones procesales

Se considera una capacidad transversal prioritaria.

El sistema debería poder explicar, para cada consecuencia procesal:

1. Qué acontecimiento detectó.
2. De qué documento, actuación o fuente obtuvo la información.
3. Qué regla procesal evaluó.
4. Qué condiciones consideró cumplidas y por qué.
5. Qué consecuencia produjo.
6. Qué plazos, documentos o tareas se generaron.
7. Qué elementos quedaron pendientes.
8. Si la consecuencia fue automática, propuesta por inteligencia artificial o confirmada por un profesional.

La cronología debe distinguir entre secuencia temporal y relación causal. La mera proximidad cronológica entre eventos no demuestra que uno haya causado al otro.

## 4. Tecnologías previstas

### 4.1. Confiabilidad y calidad del núcleo

**pytest — prioridad inmediata durante la etapa de correcciones**

Incorporar pruebas automatizadas para verificar servicios, reglas, estados, plazos, documentos y transacciones.

Las pruebas deben cubrir tanto resultados exitosos como errores, condiciones no satisfechas y situaciones en las que el sistema no debe producir consecuencias.

**Pydantic — incorporación gradual**

Evaluar su utilización para validar y estructurar datos de entrada y salida de servicios, eventos, actuaciones, reglas e integraciones externas.

No debe duplicar innecesariamente las validaciones ya resueltas por los modelos y la base de datos.

### 4.2. Reproducibilidad e infraestructura

**Docker — después de estabilizar la aplicación**

Evaluar la containerización para reproducir el entorno de ejecución en diferentes computadoras y reducir problemas de instalación y configuración.

**GitHub Actions — después de incorporar pruebas**

Configurar integración continua para ejecutar pruebas automatizadas y verificaciones de calidad ante cambios en el repositorio.

**PostgreSQL — cuando el modelo de datos y la concurrencia lo justifiquen**

Evaluar la migración desde SQLite cuando existan necesidades de múltiples usuarios, concurrencia, mayor volumen de información o capacidades avanzadas de consulta.

La migración deberá contar con un procedimiento de respaldo, conversión, validación y reversión.

### 4.3. Procesamiento documental

**Tesseract OCR**

Evaluar su uso para extraer texto de documentos escaneados e imágenes.

**Docling**

Evaluar su uso para procesar PDF y documentos con estructuras complejas, tablas y secciones.

Ambas tecnologías podrían integrarse a un flujo de recepción documental que extraiga información, identifique datos relevantes y proponga acontecimientos procesales.

La extracción automática deberá incluir mecanismos de validación y confirmación humana, especialmente para fechas, números de expediente, nombres y plazos.

### 4.4. Inteligencia artificial y asistencia procesal

**OpenAI API**

Evaluar su incorporación para interpretar documentos, clasificar acontecimientos, extraer información, resumir resoluciones y proponer actuaciones.

La inteligencia artificial no deberá sustituir al motor determinístico de reglas ni producir por sí sola decisiones procesales definitivas.

**LangGraph**

Evaluar su utilización en una etapa avanzada para construir flujos de asistencia con pasos, estados, condiciones, herramientas y puntos de aprobación humana.

Su incorporación dependerá de que los servicios procesales y las reglas determinísticas estén previamente estabilizados.

### 4.5. Búsqueda documental inteligente

**pgvector**

Evaluar su incorporación junto con PostgreSQL para almacenar representaciones vectoriales y realizar búsquedas semánticas sobre documentos, resoluciones, antecedentes y actuaciones.

Su utilidad dependerá de la existencia de una biblioteca documental suficientemente organizada y de mecanismos para identificar las fuentes de cada resultado.

### 4.6. Inteligencia de negocios

**Microsoft Power BI**

Considerar su incorporación como módulo complementario de análisis y estadísticas, no como parte del núcleo procesal.

Posibles indicadores:

- Expedientes por jurisdicción, tipo de proceso y estado.
- Plazos pendientes, vencidos y cumplidos.
- Expedientes sin movimientos relevantes durante períodos determinados.
- Tiempo promedio entre acontecimientos procesales.
- Volumen de trabajo por período.
- Documentos y actuaciones generados.
- Frecuencia de activación de reglas.
- Identificación de cuellos de botella.

Su incorporación deberá esperar a que los datos sean consistentes, confiables y suficientemente estructurados. Los indicadores deberán distinguir datos confirmados de datos inferidos.

## 5. Orden de incorporación recomendado

1. pytest: pruebas del núcleo procesal durante las correcciones.
2. Docker: reproducibilidad del entorno una vez estabilizada la instalación.
3. GitHub Actions: automatización de pruebas y controles de calidad.
4. Pydantic: validación estructurada en los puntos de integración que lo requieran.
5. PostgreSQL: cuando la evolución del sistema justifique una base de datos más robusta.
6. Tesseract OCR y Docling: automatización de recepción y procesamiento documental.
7. OpenAI API: interpretación y asistencia documental, con supervisión profesional.
8. pgvector: búsqueda semántica sobre una biblioteca documental organizada.
9. LangGraph: flujos avanzados de asistencia una vez consolidado el motor procesal.
10. Power BI: análisis de gestión y estadísticas cuando existan datos confiables.

Este orden es orientativo. Cada incorporación deberá revisarse según el estado real del proyecto y sus necesidades.

## 6. Seguridad, auditoría y protección de información

La evolución deberá contemplar progresivamente:

- Gestión segura de credenciales y secretos.
- Autenticación y autorización por usuario y función.
- Registro auditable de operaciones y modificaciones.
- Copias de seguridad automáticas y pruebas de restauración.
- Protección de documentos y datos personales.
- Control de acceso a integraciones externas.
- Registro de errores y monitoreo de operaciones.
- Separación entre ambientes de desarrollo, prueba y producción.

## 7. Criterio de incorporación

Antes de incorporar una tecnología se deberá documentar:

- Necesidad concreta que resuelve.
- Beneficio esperado.
- Costos de implementación y mantenimiento.
- Dependencias que introduce.
- Impacto sobre la arquitectura existente.
- Riesgos de seguridad y protección de datos.
- Pruebas necesarias para validar su funcionamiento.
- Alternativas más sencillas disponibles.

La incorporación deberá ser gradual y reversible siempre que resulte técnicamente posible.

## 8. Decisión de alcance actual

Estas tecnologías y capacidades forman parte de la visión futura del proyecto. Su documentación no significa que estén implementadas ni que deban incorporarse inmediatamente.

La prioridad inmediata continúa siendo recuperar un entorno reproducible, estabilizar los servicios existentes, corregir las inconsistencias detectadas y verificar los flujos principales.

El principio rector es construir primero un sistema capaz de determinar con precisión qué ocurrió y qué consecuencias produjo; posteriormente, dotarlo de capacidades para interpretar, anticipar y asistir.
