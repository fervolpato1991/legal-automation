# Sistema Jurídico --- Estado actual verificado

**Fecha de corte:** 28/10/2026\
**Repositorio:**
`https://github.com/fervolpato1991/legal-automation.git`\
**Directorio local inspeccionado:** `E:\Proyecto-Juridico`\
**Rama conocida:** `main`

## 1. Propósito de este documento

Este documento registra el estado observado durante la recuperación del
proyecto después del formateo de la PC. Distingue entre:

-   **Verificado:** observado directamente en archivos, comandos o
    estructura de la base.
-   **Pendiente de prueba:** el código existe, pero no se ejecutó una
    prueba funcional integral.
-   **Riesgo identificado:** comportamiento que podría ser incorrecto y
    requiere revisión.
-   **Planificado:** objetivo de arquitectura aún no implementado o no
    verificado.

Los expedientes y actuaciones de la base actual son datos ficticios de
prueba. Su contenido no constituye el objetivo de esta auditoría.

## 2. Estado general

El proyecto local contiene una aplicación Flask con modelos SQLAlchemy,
servicios procesales, templates Jinja, y cambios locales para un
timeline basado en eventos y una visualización Mermaid. La base SQLite
existe y contiene registros de prueba.

**No se verificó todavía el funcionamiento integral de la aplicación.**
No debe interpretarse que las funciones listadas en la documentación
histórica funcionan correctamente solo porque exista código asociado.

No se modificó código funcional ni se ejecutaron migraciones durante
esta inspección.

## 3. Entorno de desarrollo

-   Python 3.12.0 está instalado y funciona.
-   Se creó `venv_inspeccion` para inspeccionar el proyecto sin depender
    del entorno anterior.
-   Los entornos `venv` anteriores, tanto en la carpeta del proyecto
    como en el respaldo, apuntan a
    `C:\Program Files\Python310\python.exe`, que ya no existe tras el
    formateo.
-   No se debe eliminar todavía el entorno anterior: primero debe
    confirmarse qué dependencias necesita la aplicación y si hay
    archivos útiles.
-   No se encontró `requirements.txt`, `pyproject.toml` ni `Pipfile` en
    la raíz durante la búsqueda realizada.
-   El `README.md` es breve y no sustituye un manifiesto de
    dependencias.

**Próximo paso de entorno:** identificar imports/dependencias reales y
preparar un manifiesto reproducible después de revisar los archivos
pertinentes. No instalar paquetes a ciegas ni ejecutar la aplicación
hasta disponer de una lista mínima de dependencias.

## 4. Estado de Git y archivos locales

El estado observado fue:

``` text
 M app/web/app.py
 M app/web/templates/base.html
 M app/web/templates/components/timeline.html
 M app/web/templates/expediente.html
?? ARQUITECTURA_Y_HOJA_DE_RUTA.md
?? app/services/timeline_service.py
?? app/services/workflow_visual_service.py
?? app/static/
?? app/web/templates/components/workflow_graph.html
?? diff_app.txt
?? venv_inspeccion/
```

`git diff --stat` informó cambios en cuatro archivos versionados:

``` text
app/web/app.py                             | 69 +++++++++++++++---------------
app/web/templates/base.html                | 24 +++++++++++
app/web/templates/components/timeline.html | 27 +++++++++---
app/web/templates/expediente.html          | 15 +++++++
4 files changed, 94 insertions(+), 41 deletions(-)
```

`git diff --check` no mostró salida.

### Reglas de preservación

-   No ejecutar `git reset`, `git checkout` para descartar cambios,
    `git clean`, `git pull`, `git restore`, ni otras operaciones que
    puedan sobrescribir o eliminar trabajo local sin una decisión
    explícita e informada.
-   No agregar, confirmar ni publicar cambios con `git add`, `commit` o
    `push` sin autorización expresa.
-   No borrar `diff_app.txt`: debe inspeccionarse antes de decidir si es
    un archivo temporal o contiene trabajo útil.
-   `venv_inspeccion/` aparece como no rastreado porque está dentro del
    repositorio. Más adelante se deberá decidir cómo evitar que el
    entorno virtual se incluya accidentalmente en Git, preferentemente
    mediante una regla apropiada de `.gitignore`, previa revisión del
    archivo.
-   `ARQUITECTURA_Y_HOJA_DE_RUTA.md` aparece como archivo no rastreado
    en la copia local. La versión revisada debe compararse y guardarse
    de forma consciente, sin asumir que ya está versionada en Git.

También existe una carpeta de respaldo
`E:\Proyecto-Juridico - Respaldo`. No se ha demostrado que todos sus
archivos sean idénticos a los del directorio de trabajo.

## 5. Base SQLite

**Archivo:** `E:\Proyecto-Juridico\legal_system.db`\
**Tamaño observado:** 53.248 bytes\
**Fecha observada:** 11/09/2026 17:36

La base fue examinada en modo de solo lectura. Tablas y cantidades
observadas:

  Tabla                    Registros
  ---------------------- -----------
  `expedientes`                    3
  `actuaciones`                    6
  `eventos_sistema`               13
  `documentos`                     3
  `plazos`                         3
  `reglas_procesales`              2
  `estados_procesales`             0
  `historial_estados`              0
  `partes`                         0

Los datos son ficticios y no requieren una auditoría jurídica de su
contenido.

### Integridad observada

-   `PRAGMA foreign_key_check` no informó infracciones.
-   No se encontraron referencias a expedientes inexistentes en las
    tablas examinadas.
-   No existe la tabla `alembic_version`.

La ausencia de `alembic_version` no demuestra por sí sola que la base
esté dañada, pero impide asumir que Alembic conoce su estado. No
ejecutar migraciones hasta aclarar la configuración y el estado de
esquema.

## 6. Modelos y arquitectura conocidos

Se identificaron los modelos principales siguientes:

-   `Expediente`
-   `Actuacion`
-   `Documento`
-   `Plazo`
-   `ReglaProcesal`
-   `EstadoProcesal`
-   `HistorialEstado`
-   `EventoSistema`
-   `Parte`

Los modelos están repartidos en `app/models/`; `app/models/__init__.py`
importa los modelos conocidos. La clase `Base` está definida en
`app/db/db.py`.

El modelo actual es una base inicial. Aún no representa de manera
completa conceptos como `AccionProcesal`, entrada judicial externa,
origen/evidencia, versiones de reglas, metadatos procesales de modelos
de escritos, confirmación humana o niveles de respaldo.

## 7. Hallazgos de código

### 7.1 `app/services/event_service.py`

`registrar_evento(...)` crea y agrega un `EventoSistema` a la sesión,
pero no hace `commit`. Esto permite que la transacción sea controlada
por el llamador; el llamador debe asegurar que evento y consecuencia se
confirmen o reviertan juntos.

### 7.2 `app/services/regla_service.py`

Hallazgos observados en el código:

-   Busca reglas mediante `evento=actuacion.tipo.lower()`.
-   Omite reglas inactivas.
-   `evaluar_condicion()` acepta condiciones vacías.
-   La condición conocida `no_existe_plazo` comprueba la existencia de
    un plazo pendiente del mismo tipo.
-   Una condición desconocida devuelve `True`, lo que puede habilitar
    una regla sin que el sistema entienda su condición. **Riesgo
    prioritario:** las condiciones desconocidas deberían fallar de forma
    segura y dejar un diagnóstico.
-   El control `unica` comprueba la existencia de un documento asociado
    al expediente y al tipo de evento. No parece ser una garantía
    general de idempotencia para todas las consecuencias.
-   El servicio puede intentar cambiar estado, crear plazo y generar
    documento.
-   La creación de plazos usa `date.today()` y días corridos
    (`timedelta`); no modela por ahora calendarios judiciales, días
    hábiles, ferias ni reglas de cómputo.
-   El evento `CAMBIO_ESTADO` se registra después de llamar a
    `cambiar_estado()`, pero esa función no comunica de manera explícita
    si el cambio se efectuó. Puede registrarse un evento aunque no haya
    ocurrido la transición.
-   Los eventos de plazo/documento no incluyen actualmente, según el
    código revisado, el identificador del plazo o documento creado
    dentro del campo `datos`; la trazabilidad podría ser más precisa.
-   Se observó texto con caracteres de codificación incorrecta en
    algunos mensajes de consola.

Estos hallazgos son candidatos a corrección, no autorización para
cambiar el código automáticamente.

### 7.3 `app/services/workflow_service.py`

`cambiar_estado()` busca el estado de destino por nombre. Si no existe,
imprime un mensaje y retorna sin cambiar el estado. Si existe, crea un
`HistorialEstado` y actualiza el estado del expediente.

La función no devuelve un resultado estructurado que permita al servicio
de reglas saber con certeza si la transición se efectuó. Esto debe
resolverse antes de confiar en la trazabilidad automática.

### 7.4 Rutas Flask

En `app/web/app.py` se observaron dos funciones asociadas a la ruta
`/expediente/<int:id>/actuacion/nueva`:

-   una función `crear_actuacion` con método POST;
-   una función `nueva_actuacion` con métodos GET y POST.

Ambas implementan creación de actuaciones con diferencias: la primera
registra el evento `ACTUACION`, mientras que la segunda, en el código
revisado, no lo registra. Se debe inspeccionar el mapa real de rutas de
Flask y probar los métodos GET/POST antes de decidir una corrección.

También se observó una `secret_key` hardcodeada
(`"clave-super-secreta"`). Para un uso real debe sustituirse por
configuración segura fuera del código, con un valor secreto por entorno.
No es una prioridad para una prueba local aislada, pero sí un requisito
antes de desplegar.

La nueva ruta de workflow debe comprobar la existencia del expediente y
devolver 404 si no existe, en lugar de arriesgar un error por acceder a
un objeto inexistente.

### 7.5 Timeline

El servicio nuevo `app/services/timeline_service.py` consulta
`EventoSistema` y devuelve una lista de eventos ordenados por fecha
descendente.

La versión anterior de la ruta de timeline construía elementos desde
actuaciones, documentos y plazos. La ruta actualizada utiliza
`obtener_timeline_expediente()`, por lo que puede dejar fuera documentos
o plazos que no tengan su correspondiente evento.

Debe decidirse explícitamente si el timeline será: 1. una vista
exclusivamente de eventos del sistema, o 2. una línea temporal unificada
que incluya hechos y objetos procesales, conservando el origen y la
relación de cada elemento.

La segunda opción probablemente se ajuste mejor a la visión del
producto, pero requiere un modelo de representación común y pruebas.

### 7.6 Workflow Mermaid

`app/services/workflow_visual_service.py` consulta los eventos de un
expediente en orden cronológico y dibuja una cadena entre eventos
consecutivos.

Riesgos observados: - conectar eventos cronológicamente no demuestra
causalidad; - el escape de texto solo reemplaza comillas dobles, por lo
que ciertos caracteres pueden romper el diagrama; - `classDef` se agrega
dentro del bucle; - existe una variable de iteración que no se utiliza.

El diagrama debe distinguir secuencia temporal de relaciones causales
verificadas. Una flecha causal solo debe mostrarse cuando existe una
relación explícita en los datos.

### 7.7 Inicialización y migraciones

`app/main.py` importa modelos y ejecuta
`Base.metadata.create_all(bind=engine)`. `create_all()` crea tablas
ausentes, pero no modifica automáticamente columnas de tablas
existentes. Se debe verificar que todos los modelos que deben
registrarse estén importados antes de invocarlo.

`migrations/env.py` contiene `from models import Base`, mientras que la
estructura revisada ubica `Base` en `app.db.db`. No se encontró un
`models.py` en la inspección realizada. Por ello, la importación de
Alembic parece inconsistente y debe verificarse/corregirse antes de usar
migraciones.

La migración llamada `ea0593be0233_initial.py` solo agrega la columna
`domicilio` a `partes`; no constituye una migración inicial completa del
esquema.

**No ejecutar `alembic upgrade`, `alembic downgrade` ni `reset_db.py`
durante esta etapa.**

## 8. Funcionalidades visuales pendientes de validación

Se añadieron o modificaron archivos relacionados con:

-   timeline basado en eventos;
-   workflow Mermaid;
-   CSS propio;
-   JavaScript para interacción Timeline ↔ Workflow;
-   reinicialización de Mermaid tras swaps de HTMX.

No se ha completado una prueba integral de navegador. Pendiente
comprobar:

-   inicio de la aplicación;
-   apertura de un expediente ficticio;
-   renderizado del timeline;
-   renderizado del workflow;
-   sincronización de selección entre timeline y diagrama;
-   funcionamiento después de un swap HTMX;
-   consola del navegador;
-   comportamiento cuando no hay eventos o no existe el expediente.

## 9. Riesgos prioritarios

1.  Condiciones desconocidas de reglas aceptadas por defecto.
2.  Registro de cambio de estado sin confirmar que el cambio ocurrió.
3.  Duplicidad de rutas de creación de actuaciones.
4.  Posible pérdida de elementos del timeline al basarlo solo en
    eventos.
5.  Diagrama que puede sugerir causalidad sin evidencia.
6.  Configuración de Alembic aparentemente inconsistente.
7.  Falta de manifiesto reproducible de dependencias.
8.  `secret_key` hardcodeada.
9.  Ausencia de pruebas automatizadas identificadas en la inspección
    actual.
10. Falta de un mecanismo explícito y uniforme de rollback/cierre de
    sesión en algunos flujos revisados.

## 10. Próximo paso concreto

No desarrollar todavía el Inspector Procesal ni nuevas automatizaciones.

Orden recomendado:

1.  Preservar el estado local y revisar `diff_app.txt` y el diff de cada
    archivo.
2.  Inventariar imports y dependencias para recuperar un entorno
    reproducible.
3.  Confirmar la estructura de modelos, imports y configuración de base.
4.  Corregir o aclarar la configuración de Alembic sin ejecutar
    migraciones contra la base existente.
5.  Resolver la duplicidad de rutas de creación de actuaciones.
6.  Definir la semántica del timeline y separar cronología de
    causalidad.
7.  Hacer que el resultado de `cambiar_estado()` sea verificable y que
    los eventos reflejen hechos ocurridos.
8.  Cambiar la evaluación de condiciones desconocidas para que no
    habilite reglas por defecto.
9.  Ejecutar pruebas pequeñas y aisladas.
10. Probar la interfaz completa en el navegador.
11. Recién después avanzar al Inspector Procesal.

## 11. Límite de esta inspección

Este documento refleja archivos, salidas de consola y estructura
examinados durante la sesión. No certifica que la aplicación arranque ni
que todos los servicios funcionen. Cada punto pendiente debe verificarse
antes de marcarlo como completado.

## Punto de control documental — inspección inicial (28/10/2026)

### Estado de la inspección

Avance estimado: aproximadamente 75 %. Es una estimación de trabajo,
no una medición automática. La inspección inicial aún no está cerrada.

### Evidencia revisada en esta conversación

- Se examinó `diff_app.txt`, con cambios en `app/web/app.py`.
- Se inspeccionaron las rutas de creación de actuaciones, timeline y
  workflow.
- Se leyó `app/services/event_service.py`.
- Se leyó `app/services/regla_service.py`.
- Se inspeccionó `app/services/workflow_service.py`, pero la salida
  copiada en la conversación quedó interrumpida en una instrucción
  `print("â`. No se debe concluir que el archivo esté truncado sin
  comprobar su contenido completo.
- Se leyeron `app/services/timeline_service.py`,
  `app/services/workflow_visual_service.py` y las plantillas de
  timeline y workflow.
- Se inspeccionó el estado de Git y el inventario de archivos de la
  raíz.

### Hallazgos confirmados o riesgos concretos

1. Dos funciones están asociadas a
   `/expediente/<int:id>/actuacion/nueva`; ambas aceptan POST y difieren
   en el registro de eventos.
2. Las rutas de timeline y workflow no comprueban explícitamente si el
   expediente existe.
3. La timeline nueva consulta solo `eventos_sistema`, a diferencia de
   la versión anterior, que reunía actuaciones, documentos y plazos.
4. El diagrama Mermaid conecta eventos por orden cronológico, lo que
   no demuestra causalidad procesal.
5. El escape de etiquetas Mermaid es insuficiente para caracteres
   especiales; `classDef` se repite dentro del bucle.
6. `evaluar_condicion()` acepta condiciones desconocidas al devolver
   `True`; debe revisarse para que falle de forma segura.
7. `cambiar_estado()` no comunica un resultado explícito al llamador.
   El servicio de reglas registra `CAMBIO_ESTADO` sin verificar que la
   transición se haya realizado.
8. La condición `unica` no constituye una garantía general de
   idempotencia.
9. Los plazos usan días corridos y no contemplan todavía reglas de
   cómputo judicial.
10. Se observaron textos con codificación incorrecta y una comilla
    adicional en `data-event-id` de la plantilla de timeline.
11. Las rutas de timeline y workflow necesitan manejo de expedientes
    inexistentes.
12. No se verificó todavía la ejecución integral de la aplicación.

### Restricciones vigentes

- No ejecutar `reset_db.py`.
- No ejecutar migraciones Alembic hasta aclarar su configuración.
- No descartar cambios locales ni ejecutar operaciones destructivas
  de Git.
- No hacer `git add`, `commit` o `push` sin autorización expresa.
- No instalar dependencias a ciegas.
- No considerar funcional una característica hasta probarla.

### Próxima acción

Completar la inspección de `workflow_service.py`, revisar el inventario
y `.gitignore`, identificar dependencias y verificar imports y rutas.
Después cerrar el diagnóstico y comenzar las correcciones prioritarias
con pruebas controladas.

La reconstrucción del `README.md` queda pendiente hasta confirmar el
procedimiento de ejecución y distinguir las funciones implementadas de
las planificadas.

## Cierre del diagnóstico inicial — 28/10/2026

Referencia: CIERRE_DIAGNOSTICO_INICIAL_20261028

### Entorno y dependencias

- El entorno `venv_inspeccion` funciona con Python 3.12.0, pero solo tiene pip instalado.
- El entorno virtual anterior conserva metadatos de paquetes que permiten recuperar versiones de referencia.
- Versiones registradas: Flask 3.1.3; SQLAlchemy 2.0.49; Jinja2 3.1.6; Alembic 1.18.4; Werkzeug 3.1.8; blinker 1.9.0; click 8.3.3; colorama 0.4.6; greenlet 3.4.0; itsdangerous 2.2.0; Mako 1.3.11; MarkupSafe 3.0.3; setuptools 57.4.0; tomli 2.4.1; typing_extensions 4.15.0; pip 21.2.3.
- Estas versiones proceden de metadatos locales: todavía no existe un manifiesto de dependencias fiable ni se verificó la ejecución con ellas.
- No se encontró un manifiesto de dependencias útil en la búsqueda realizada.

### Hallazgos funcionales prioritarios

1. `cambiar_estado()` retorna sin resultado explícito cuando no encuentra el estado solicitado. `regla_service.py` registra igualmente un evento `CAMBIO_ESTADO`, lo que puede producir un registro engañoso.
2. La base inspeccionada tiene tres eventos `CAMBIO_ESTADO`, pero cero registros en `historial_estados` y cero filas en `estados_procesales`.
3. Existen dos rutas que aceptan POST para `/expediente/<id>/actuacion/nueva`, con comportamientos diferentes.
4. La cronología nueva se basa en eventos, a diferencia de la vista anterior que reunía actuaciones, documentos y plazos. Hay que verificar y decidir el modelo antes de dar por válida la vista.
5. El generador Mermaid representa los eventos en orden cronológico, pero esa secuencia no demuestra causalidad procesal.
6. Se identificaron problemas de codificación de caracteres y una comilla duplicada en el atributo `data-event-id` de la plantilla de cronología.
7. `app/web/app.py` contiene una clave secreta escrita directamente en el código.
8. `app/templates` contiene plantillas de documentos `.txt`, mientras que `app/web/templates` contiene las plantillas HTML de la interfaz. No se deben fusionar sin revisar sus consumidores.
9. El archivo `.gitignore` excluye `venv/`, pero no `venv_inspeccion/`.
10. La base de datos fue inspeccionada en modo de lectura. No se ejecutaron `reset_db.py` ni migraciones.

### Estado de verificación

- No se ha demostrado que la aplicación funcione de extremo a extremo después del formateo.
- No se instalaron dependencias en `venv_inspeccion`.
- No se realizaron correcciones de código como parte de esta inspección.
- Los cambios locales y los documentos sin seguimiento deben conservarse.
- No se realizó ningún commit ni push.

### Próxima acción

Preparar una recuperación controlada del proyecto y reconstruir el entorno de ejecución a partir de las dependencias identificadas, después de comprobar las importaciones, la configuración y la compatibilidad. Luego corregir los problemas prioritarios y probar los flujos principales antes de actualizar el README.

---

## Estado actualizado del proyecto - 09/11/2026

### Recuperación del entorno

- Proyecto recuperado desde el repositorio GitHub.
- Entorno virtual funcional: `venv_inspeccion`.
- Python: 3.12.0.
- Dependencias instaladas y verificadas:
  - Flask 3.1.3
  - SQLAlchemy 2.0.49
  - Alembic 1.18.4
  - Jinja2 3.1.6
- Se creó `requirements.txt` con las versiones directas anteriores.
- Las importaciones de las dependencias principales finalizaron correctamente.

### Integridad y protección de datos

- La base `legal_system.db` se conservó.
- Se verificó que su SHA256 antes y después de la importación controlada de la aplicación coincide.
- Las pruebas HTTP de lectura también finalizaron sin modificar la base.
- Se creó una copia integral externa del proyecto, incluyendo `.git` y documentación.
- La copia y el original tienen hashes SHA256 coincidentes para la base de datos.
- No se ejecutaron `reset_db.py` ni migraciones.
- `venv/`, `venv_inspeccion/` y `legal_system.db` están excluidos mediante `.gitignore`.

### Correcciones y componentes incorporados

- Se eliminó la ruta POST duplicada de creación de actuaciones.
- La ruta única de creación de actuaciones admite GET y POST.
- Se incorporaron validaciones de campos obligatorios, registro del evento asociado y manejo transaccional.
- Se incorporó `timeline_service.py` para consultar los eventos del expediente.
- Se incorporó `workflow_visual_service.py` para generar una representación Mermaid cronológica.
- Se incorporó la ruta de visualización del workflow.
- Se corrigió el atributo `data-event-id` de la plantilla de timeline.
- Se corrigió el manejo de expedientes inexistentes y el cierre de sesiones en las rutas de timeline y workflow.

### Validaciones realizadas

- Importación controlada de `app.web.app`: correcta.
- Compilación de la aplicación con `compileall`: correcta.
- Rutas GET de consulta y formularios probadas mediante Flask test_client: todas respondieron 200 OK.
- Hash de la base antes y después de las pruebas HTTP: idéntico.
- `git diff --check`: sin errores; solo se informó una advertencia de conversión LF/CRLF en `.gitignore`.

### Limitaciones de las pruebas

- No se probaron todavía los POST de creación de actuaciones y reglas en ejecución.
- No se validó de extremo a extremo la aplicación de reglas procesales.
- La representación Mermaid muestra una secuencia cronológica; todavía no representa causalidad procesal.
- La aplicación no está certificada funcionalmente en todos sus flujos.

### Estado de Git y próximo desarrollo

- Rama actual: `main`.
- Remoto: `origin`.
- Los cambios locales están preservados.
- No se ejecutó `git add`, `git commit` ni `git push`.
- El respaldo externo integral está verificado.
- La revisión técnica inicial se considera cerrada.

Próximo componente funcional: `app/services/inspector_service.py`, comenzando por `obtener_detalle_evento(db, expediente_id, evento_id)`.

El desarrollo continuará con cambios acotados y pruebas específicas, sin reabrir inspecciones generales salvo que aparezca un defecto que afecte al componente en desarrollo.

## ACTUALIZACIÓN 10/11/2026 — INSPECTOR PROCESAL IMPLEMENTADO

### 1. Funcionalidad desarrollada

Se implementó el servicio `app/services/inspector_service.py`, con la función:

`obtener_detalle_evento(db, expediente_id, evento_id)`

La función recupera el detalle de un evento del sistema y sus relaciones con:
- Expediente.
- Actuación.
- Regla procesal.

Se incorporó la ruta:

`/expediente/<int:expediente_id>/evento/<int:evento_id>`

También se creó la plantilla:

`app/web/templates/evento_detalle.html`

La ficha del Inspector muestra los datos del evento, el expediente relacionado y, cuando existen, la actuación y la regla procesal asociadas.

### 2. Integración con la timeline

Se incorporó el acceso «Ver detalle» desde `app/web/templates/components/timeline.html`.

Durante la prueba visual se detectó un error HTTP 500 en `ver_expediente()`, causado porque la timeline del expediente combina actuaciones, plazos, documentos e historial de estados con eventos del sistema.

Los registros de esa timeline mixta no comparten necesariamente los campos `id` y `expediente_id`.

Se corrigió la plantilla para mostrar el enlace al Inspector únicamente cuando ambos identificadores están disponibles:

`{% if e.id is defined and e.expediente_id is defined %}`

La corrección preserva los registros de la timeline general y permite acceder al detalle de los eventos del sistema.

### 3. Pruebas realizadas

- Compilación de `inspector_service.py`: correcta.
- Compilación general de `app`: correcta.
- Recuperación de un evento existente y sus relaciones: correcta.
- Evento inexistente: devuelve `None`.
- Evento perteneciente a otro expediente: devuelve `None`.
- GET `/expediente/1/evento/1`: HTTP 200.
- GET `/expediente/1/evento/5`: HTTP 404.
- GET de un evento inexistente: HTTP 404.
- GET `/expediente/1/timeline`: HTTP 200.
- Hash SHA256 de la base de datos antes y después de las pruebas: idéntico.
- Prueba visual en navegador: realizada satisfactoriamente.
- Corrección del error 500 en la ficha del expediente: verificada.

Las pruebas de lectura se realizaron sin escrituras en la base de datos.

### 4. Estado resultante

El Inspector Procesal se considera implementado e integrado en la aplicación.

El usuario comprobó visualmente la ficha del evento y confirmó que la aplicación funciona correctamente después de la corrección de la timeline.

### 5. Pendientes

- Revisar los errores 404 de los recursos estáticos `styles.css` y `workflow.js` observados en los registros del servidor, si persisten.
- Actualizar la documentación técnica cuando se incorporen nuevas funcionalidades.
- Retomar el cierre de Git y preparar el commit, sin ejecutarlo hasta contar con autorización expresa.

### 6. Próximo paso

Retomar la revisión del estado de Git, clasificar los cambios incorporados y preparar el commit de esta etapa. No ejecutar `git add`, `git commit` ni `git push` sin autorización expresa.
