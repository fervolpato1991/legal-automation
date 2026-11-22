# Sistema Jurídico --- Bitácora de inspección y recuperación

**Fecha de corte:** 28/10/2026\
**Proyecto:** `E:\Proyecto-Juridico`\
**Repositorio remoto conocido:**
`https://github.com/fervolpato1991/legal-automation.git`

## 1. Objetivo

Recuperar el contexto del proyecto después del formateo de la PC,
preservar los cambios locales y establecer una base verificable para
continuar el desarrollo del Asistente Procesal.

La inspección se limitó a lecturas de archivos, estado de Git, uso del
intérprete de Python y consultas de solo lectura a SQLite. No se
realizaron cambios funcionales ni operaciones de Git para alterar el
historial.

Los expedientes y actuaciones de la base son ficticios. Su contenido no
es un objetivo de auditoría jurídica.

## 2. Registro cronológico

### 2.1 Entorno de Python

**Observado** - Python 3.12.0 funciona en el entorno de inspección. -
`venv_inspeccion` está en `E:\Proyecto-Juridico\venv_inspeccion`. - El
entorno anterior apunta a `C:\Program Files\Python310\python.exe`, que
ya no existe después del formateo.

**Decisión** - Mantener los entornos anteriores por ahora. - No instalar
dependencias a ciegas. - Identificar imports y dependencias reales antes
de reconstruir el entorno de ejecución. - El entorno `venv_inspeccion`
aparece como no rastreado dentro del repositorio; revisar más adelante
la estrategia de `.gitignore`.

### 2.2 Estado local de Git

Estado observado:

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

El diff de los cuatro archivos versionados mostró 94 inserciones y 41
eliminaciones. `git diff --check` no informó errores de whitespace.

**Decisiones de preservación** - No descartar cambios. - No ejecutar
`git reset`, `git clean`, `git restore`, `pull`, `checkout` destructivo
ni operaciones equivalentes. - No ejecutar `git add`, `commit` o `push`
sin autorización. - Inspeccionar `diff_app.txt` antes de decidir su
destino. - La documentación de arquitectura local aparece sin
seguimiento; revisar antes de sustituirla.

### 2.3 Inspección de SQLite

La base `E:\Proyecto-Juridico\legal_system.db` existe y fue abierta en
modo de solo lectura.

Tablas y registros:

  Tabla                    Cantidad
  ---------------------- ----------
  `expedientes`                   3
  `actuaciones`                   6
  `eventos_sistema`              13
  `documentos`                    3
  `plazos`                        3
  `reglas_procesales`             2
  `estados_procesales`            0
  `historial_estados`             0
  `partes`                        0

Se observaron cuatro tipos de eventos: `ACTUACION` (4), `CAMBIO_ESTADO`
(3), `DOCUMENTO_GENERADO` (3) y `PLAZO_CREADO` (3). Las actuaciones de
prueba incluyen variaciones de mayúsculas y escritura.

La regla activa examinada se asocia a `traslado`, configura estado de
destino `TRASLADO`, generación de documento y plazo de 15 días. Otra
regla está inactiva y tiene valores de prueba `se` y `fs`.

**Integridad** - No se detectaron referencias a expedientes inexistentes
en las tablas consultadas. - `PRAGMA foreign_key_check` no devolvió
infracciones. - No existe la tabla `alembic_version`.

**Interpretación** Los datos son ficticios y solo sirven como entorno de
prueba. La ausencia de estados e historial en la base actual no se debe
convertir por sí sola en una conclusión sobre la calidad de los datos de
producción; sí indica que las transiciones de estado deben probarse en
un entorno controlado.

**Decisión** No ejecutar migraciones ni `reset_db.py`. No alterar esta
base como parte de la inspección.

### 2.4 Configuración de migraciones

`migrations/env.py` importa `Base` desde `models`, mientras que la
estructura revisada ubica la clase en `app.db.db`. No se identificó un
`models.py` en la búsqueda previa. La migración
`ea0593be0233_initial.py` agrega solamente la columna `domicilio` a
`partes`.

**Hallazgo** La configuración de Alembic parece inconsistente y la
migración llamada "initial" no describe todo el esquema.

**Decisión** Verificar los imports y la estrategia de migraciones antes
de usar Alembic. No ejecutar `upgrade` ni `downgrade` hasta que se
comprenda la relación entre modelos, esquema y base existente.

### 2.5 Servicio de reglas

Hallazgos en `app/services/regla_service.py`:

-   Las reglas se buscan con el tipo de actuación en minúsculas.
-   Se omiten reglas inactivas.
-   La condición conocida `no_existe_plazo` comprueba plazos no
    cumplidos.
-   Las condiciones desconocidas devuelven `True`.
-   `unica` comprueba la existencia de un documento del mismo tipo, por
    lo que no asegura idempotencia general.
-   Los plazos se calculan con fecha actual y días corridos.
-   El evento de cambio de estado se registra sin una confirmación
    explícita del resultado de `cambiar_estado()`.
-   Los eventos no parecen almacenar referencias directas al objeto de
    plazo/documento creado.
-   Hay mensajes de consola con problemas de codificación.

**Decisión** Priorizar una evaluación segura de condiciones, resultado
explícito de transiciones, trazabilidad de consecuencias e idempotencia.
No implementar reglas jurídicas nuevas durante la recuperación.

### 2.6 Servicio de cambio de estado

`workflow_service.py` busca el estado de destino por nombre. Si no
existe, imprime un mensaje y retorna; si existe, registra historial y
actualiza el estado actual.

**Hallazgo** El llamador no puede distinguir mediante el valor de
retorno si el cambio se efectuó.

**Decisión** Diseñar un resultado explícito para éxito/fallo y asegurar
que el evento refleje el resultado real, antes de ampliar las
automatizaciones.

### 2.7 Rutas Flask

Se observaron dos funciones para `/expediente/<int:id>/actuacion/nueva`,
una POST y otra GET/POST. Hay diferencias en el registro del evento
`ACTUACION`.

También se observó una clave secreta hardcodeada. La nueva ruta de
workflow requiere una comprobación explícita de expediente inexistente.

**Decisión** Inspeccionar el mapa de rutas y probar GET/POST; luego
consolidar en una sola ruta coherente. Externalizar la clave secreta
antes de cualquier despliegue.

### 2.8 Timeline y workflow visual

El servicio nuevo de timeline consulta únicamente `EventoSistema`,
mientras que la versión anterior de la ruta reunía actuaciones,
documentos y plazos. Esto puede excluir elementos sin evento asociado.

El workflow Mermaid une eventos consecutivos por orden temporal. La
secuencia temporal no demuestra causalidad. El escape de caracteres es
limitado y `classDef` se agrega dentro del bucle.

**Decisión** Definir un modelo de timeline que distinga tipos de
elementos y su origen; no presentar flechas cronológicas como relaciones
causales si no están registradas explícitamente. Validar los swaps de
HTMX y la interacción bidireccional.

## 3. Inventario de decisiones vigentes

1.  Preservar todos los cambios locales.
2.  No ejecutar `reset_db.py`.
3.  No ejecutar migraciones mientras Alembic y el esquema no estén
    aclarados.
4.  No crear automatizaciones jurídicas nuevas antes de validar el
    núcleo existente.
5.  Mantener Flask/Jinja/SQLAlchemy/SQLite como stack actual; no migrar
    a SPA.
6.  Priorizar observabilidad, trazabilidad y reglas deterministas antes
    de incorporar IA.
7.  Tratar el contenido actual de la base como datos ficticios.
8.  Distinguir cronología de causalidad.
9.  Separar la acción procesal del modelo de escrito.
10. Mantener confirmación humana en decisiones o acciones de
    consecuencias relevantes.

## 4. Pendientes de inspección y prueba

-   Revisar `diff_app.txt`.
-   Inspeccionar el árbol real y `.gitignore`.
-   Inventariar dependencias e imports.
-   Verificar imports de `app.main`, `app.models` y Alembic.
-   Obtener el mapa real de rutas Flask.
-   Revisar las dos implementaciones de creación de actuación.
-   Confirmar el contrato de `cambiar_estado()`.
-   Diseñar evaluación segura de condiciones.
-   Decidir semántica del timeline.
-   Corregir la representación de causalidad en Mermaid.
-   Recuperar el entorno de ejecución de forma reproducible.
-   Probar interfaz, HTMX, Mermaid y consola del navegador.
-   Añadir pruebas automatizadas mínimas para reglas, estados, plazos,
    documentos y eventos.

## 5. Próxima sesión: secuencia recomendada

1.  Confirmar que los tres documentos se guardaron en el directorio
    correcto.
2.  Revisar el inventario del repositorio y `.gitignore` sin modificar
    nada.
3.  Examinar `diff_app.txt` y los diffs pendientes.
4.  Identificar dependencias necesarias para ejecutar la aplicación.
5.  Resolver la configuración de imports y migraciones sin ejecutar
    migraciones.
6.  Corregir, con cambios pequeños y pruebas, los defectos del flujo de
    creación de actuaciones y trazabilidad.
7.  Validar timeline/workflow en navegador.
8.  Solo después retomar el Inspector Procesal.

## 6. Criterio para actualizar esta bitácora

Cada paso futuro debe registrar: - fecha; - archivo o componente
afectado; - evidencia o prueba ejecutada; - resultado observado; -
decisión adoptada; - riesgos restantes.

No marcar una tarea como completada solo porque se escribió el código;
exigir una prueba o evidencia reproducible.

## 2.9 Punto de control documental — 28/10/2026

Se consolidan aquí los resultados de las últimas tandas de inspección
para que el trabajo pueda retomarse desde otro chat sin depender de la
memoria conversacional.

### Archivos y componentes inspeccionados

- `diff_app.txt`
- `app/web/app.py`: creación de actuaciones, timeline, eventos y
  workflow.
- `app/services/event_service.py`
- `app/services/regla_service.py`
- `app/services/workflow_service.py` (la salida compartida quedó
  interrumpida; falta verificar el contenido íntegro).
- `app/services/timeline_service.py`
- `app/services/workflow_visual_service.py`
- `app/web/templates/components/timeline.html`
- `app/web/templates/components/workflow_graph.html`
- Inventario de archivos raíz y `git status --short`.

### Hallazgos nuevos

1. La ruta `/expediente/<int:id>/actuacion/nueva` tiene dos funciones
   asociadas: `crear_actuacion` (POST) y `nueva_actuacion` (GET/POST).
   Sus flujos no son equivalentes y una registra el evento `ACTUACION`
   mientras la otra no lo hace en el código inspeccionado.
2. La nueva timeline depende exclusivamente de `EventoSistema`; puede
   omitir actuaciones, documentos y plazos sin evento asociado.
3. El endpoint de timeline y el de workflow acceden a `exp.id` sin
   verificar antes que la consulta haya encontrado el expediente.
4. El workflow Mermaid une todos los eventos consecutivos por tiempo.
   Esa relación no debe presentarse como causalidad procesal demostrada.
5. El servicio Mermaid escapa únicamente comillas dobles y agrega
   `classDef` en cada iteración.
6. `timeline.html` contiene una comilla adicional en el atributo
   `data-event-id`.
7. Se detectaron textos mal codificados en mensajes y etiquetas.
8. Las condiciones desconocidas de reglas se consideran verdaderas.
9. `cambiar_estado()` no devuelve una señal explícita de éxito o fallo;
   por eso `regla_service.py` puede registrar un cambio no realizado.
10. El `Get-Content` compartido para `workflow_service.py` terminó en
    una línea incompleta. Debe verificarse si el archivo está íntegro
    y si la interrupción fue de la salida copiada.

### Decisiones

- Separar timeline cronológica, workflow con relaciones explícitas e
  inspector procesal con explicación de reglas y consecuencias.
- No inferir causalidad solo por el orden temporal.
- Corregir primero integridad del flujo, resultados de reglas y
  transiciones, y después validar la representación visual.
- Mantener intactos código, base de datos e historial de Git durante
  la inspección.
- Actualizar el README solo después de comprobar cómo instalar y
  ejecutar la aplicación.

### Próximos pasos

1. Confirmar la integridad de `workflow_service.py`.
2. Inspeccionar `.gitignore`, el árbol y las diferencias locales
   restantes sin alterarlas.
3. Identificar las dependencias y comprobar los imports.
4. Cerrar el diagnóstico inicial.
5. Preparar un punto de recuperación controlado.
6. Corregir de forma incremental los defectos prioritarios y probarlos.
7. Documentar el procedimiento verificado en `README.md`.


## 2.10 Cierre del diagnóstico inicial — 28/10/2026

Referencia: CIERRE_DIAGNOSTICO_INICIAL_20261028

### Última comprobación del entorno

Se inspeccionaron los metadatos de paquetes conservados en `venv\Lib\site-packages`. Se recuperaron las versiones registradas de Flask, SQLAlchemy, Jinja2, Alembic y sus dependencias. El entorno `venv_inspeccion` solo contiene pip; todavía no se instaló la aplicación en él.

No se encontró un manifiesto de dependencias útil en la búsqueda realizada. El único `setup.py` encontrado estaba dentro de datos de prueba de un paquete instalado en el entorno anterior.

### Comprobaciones adicionales

- `workflow_service.py` tiene 33 líneas y no estaba truncado. `cambiar_estado()` no devuelve un resultado explícito y retorna sin modificar el expediente cuando no encuentra el estado.
- `.gitignore` excluye `venv/`, pero no `venv_inspeccion/`.
- `app/templates` contiene cuatro plantillas de documentos `.txt`.
- `app/web/templates` contiene las plantillas HTML de la interfaz y sus componentes.
- Se inventariaron las importaciones Python para identificar las dependencias externas y los servicios internos.
- El primer intento de inventariar importaciones mediante una línea Python falló por sintaxis en el comando; el intento posterior con un bloque multilínea produjo el inventario esperado.

### Conclusión de la inspección

La inspección inicial se considera suficientemente completa para pasar a una fase controlada de reconstrucción y correcciones. No equivale a certificar que la aplicación funciona. Los problemas prioritarios son el registro de cambios de estado, las rutas POST duplicadas, la coherencia de la cronología, la configuración del entorno y la verificación funcional.

No se ejecutaron migraciones, `reset_db.py` ni operaciones destructivas de Git. No se modificó la base de datos durante esta etapa.

### Próximos pasos

1. Conservar los documentos y cambios locales existentes.
2. Verificar la configuración y compatibilidad de las dependencias antes de instalarlas.
3. Reconstruir el entorno de ejecución.
4. Corregir los problemas funcionales prioritarios en cambios pequeños y verificables.
5. Probar los flujos principales y registrar los resultados.
6. Actualizar el README cuando la instalación y ejecución hayan sido comprobadas.

---

## 2.11 Recuperación, correcciones y cierre de revisión - 09/11/2026

### Recuperación del entorno

Se reconstruyó el entorno virtual `venv_inspeccion` utilizando Python 3.12.0.

Se instalaron y verificaron Flask 3.1.3, SQLAlchemy 2.0.49, Alembic 1.18.4 y Jinja2 3.1.6. Las importaciones principales finalizaron correctamente.

Se creó `requirements.txt` con las versiones directas de las dependencias.

### Respaldo e integridad

Se realizó una copia integral externa del proyecto en:

`E:\Proyecto-Juridico-Respaldos\Restauracion\Proyecto-Juridico-20261103-192021`

La copia incluye el repositorio Git, la base de datos, el código y la documentación. Se excluyeron los entornos virtuales y las credenciales locales.

La verificación SHA256 de `legal_system.db` confirmó que el original y la copia coinciden.

La importación controlada de `app.web.app` no modificó la base. Las pruebas HTTP de lectura tampoco alteraron su hash.

### Correcciones realizadas

1. Se eliminó la ruta POST duplicada `/expediente/<id>/actuacion/nueva`.
2. Se consolidó la creación de actuaciones en una ruta GET/POST.
3. Se incorporó validación de campos obligatorios.
4. Se agregó el registro del evento ACTUACION dentro de la transacción.
5. Se incorporó manejo de rollback y cierre de sesión.
6. Se agregó `timeline_service.py`.
7. Se agregó `workflow_visual_service.py`.
8. Se incorporó la ruta `/expediente/<id>/workflow`.
9. Se corrigió el atributo HTML `data-event-id`.
10. Se corrigió el manejo de expedientes inexistentes y el cierre de sesiones en las rutas de timeline y workflow.

### Pruebas

- Importación controlada de la aplicación: correcta.
- Compilación de Python: correcta.
- Rutas GET de consulta y formularios verificadas mediante `test_client`: respuestas 200 OK.
- Hash de la base antes y después de las pruebas: idéntico.
- `git diff --check`: sin errores; advertencia LF/CRLF en `.gitignore`.

No se probaron los POST ni la ejecución integral de las reglas procesales. Por lo tanto, estas comprobaciones no constituyen una certificación funcional completa.

### Cierre de esta etapa

Se considera cerrada la inspección general y la revisión inicial de los cambios.

No se ejecutaron operaciones destructivas de Git, migraciones ni reinicialización de la base.

Los archivos históricos `.respaldo-*` se conservan fuera del repositorio. `diff_app.txt` corresponde a un diff antiguo y no se incorpora al código fuente.

El commit queda pendiente de autorización expresa.

### Próximo paso

Comenzar el desarrollo de `app/services/inspector_service.py`, con la función:

`obtener_detalle_evento(db, expediente_id, evento_id)`

La implementación deberá recuperar y presentar el detalle de un evento perteneciente al expediente indicado, verificando la relación entre ambos identificadores.


## 2.12. IMPLEMENTACIÓN Y VALIDACIÓN DEL INSPECTOR PROCESAL — 10/11/2026

### Objetivo

Implementar una primera versión del Inspector Procesal que permita consultar el detalle de un evento del sistema y sus relaciones con las entidades del expediente.

### Archivos incorporados o modificados

**Nuevos:**
- `app/services/inspector_service.py`
- `app/web/templates/evento_detalle.html`

**Modificados:**
- `app/web/app.py`
- `app/web/templates/components/timeline.html`

### Implementación

Se desarrolló `obtener_detalle_evento(db, expediente_id, evento_id)` utilizando SQLAlchemy y `joinedload` para recuperar las relaciones del evento con expediente, actuación y regla procesal.

Se agregó la ruta:

`/expediente/<int:expediente_id>/evento/<int:evento_id>`

Se creó una ficha de detalle con información del evento y sus entidades relacionadas.

Se incorporó el enlace «Ver detalle» en la timeline.

### Incidencia detectada y resolución

Durante la prueba en navegador, la ruta `/expediente/1` devolvió HTTP 500.

Causa: `timeline.html` intentaba generar enlaces al Inspector para todos los elementos de una timeline mixta. Los registros de actuaciones, plazos, documentos e historial de estados no disponen necesariamente de `id` y `expediente_id`.

Resolución: se condicionó la generación del enlace a la existencia de ambos campos mediante:

`{% if e.id is defined and e.expediente_id is defined %}`

No fue necesario modificar el servicio Inspector ni alterar la estructura de la base de datos.

### Validaciones

- Compilación individual y general: correcta.
- Consulta de evento existente: correcta.
- Consulta de evento inexistente: correctamente rechazada.
- Verificación de pertenencia del evento al expediente: correcta.
- Rutas HTTP del Inspector: respuestas esperadas 200 y 404.
- Timeline parcial: HTTP 200.
- Hash SHA256 de la base de datos: sin variaciones.
- Inspección visual en navegador: satisfactoria.

### Resultado

Se considera completada la primera implementación del Inspector Procesal.

La funcionalidad permite navegar desde un evento de la timeline hasta su ficha detallada, preservando el funcionamiento de la timeline mixta del expediente.

### Observaciones pendientes

Se habían observado respuestas HTTP 404 para los recursos estáticos `styles.css` y `workflow.js`. Se deja constancia para su eventual comprobación, sin ampliar el alcance de esta etapa.

### Próxima actividad

Retomar el cierre de Git: verificar los cambios, clasificar los archivos que corresponden al commit y preparar su contenido. No ejecutar operaciones de incorporación o confirmación sin autorización expresa.
