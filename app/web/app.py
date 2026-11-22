from flask import Flask, render_template, redirect, url_for, abort, request, flash
from app.models.regla import ReglaProcesal
from app.services.alert_service import obtener_dashboard_plazos
from app.services.action_rules import sugerir_accion
from app.services.action_executor import generar_documento_desde_plazo
from app.models.plazo import Plazo
from app.models.expediente import Expediente
from app.models.documento import Documento
from app.models.actuacion import Actuacion
from app.models.evento import EventoSistema
from app.db.db import SessionLocal
from datetime import datetime, date
from sqlalchemy.orm import joinedload
from app.models.regla import ReglaProcesal
from app.services.regla_service import aplicar_reglas
from app.services.prioridad_service import calcular_prioridad
from app.services.event_service import registrar_evento
from app.services.timeline_service import obtener_timeline_expediente
from app.services.workflow_visual_service import generar_mermaid_expediente
from app.services.inspector_service import obtener_detalle_evento

app = Flask(__name__)
app.secret_key = "clave-super-secreta"


@app.route("/")
def dashboard():
    data = obtener_dashboard_plazos()
    db = SessionLocal()

    PRIORIDAD_ORDEN = {
        "critico": 0,
        "urgente": 1,
        "medio": 2,
        "bajo": 3,
        "ok": 4
    }

    def enrich(plazos):
        resultado = []

        for p in plazos:
            sugerencia = sugerir_accion(p)
            prioridad = calcular_prioridad(p.expediente)

            resultado.append({
                "id": p.id,
                "expediente_id": p.expediente.id,
                "caratula": p.expediente.caratula,
                "tipo": p.tipo,
                "vence": p.fecha_vencimiento,
                "accion": sugerencia["accion"] if sugerencia else "",
                "prioridad": prioridad
            })
            resultado.sort(
             key=lambda x: (
                    PRIORIDAD_ORDEN.get(
                            x["prioridad"]["nivel"],
                             99
                     ),
                     x["vence"]
            )
        )
        return resultado

    expedientes = db.query(Expediente).all()

    return render_template(
        "dashboard.html",
        vencidos=enrich(data["vencidos"]),
        proximos=enrich(data["proximos"]),
        futuros=enrich(data["futuros"]),
        expedientes=expedientes
    )

@app.route("/expediente/nuevo", methods=["GET", "POST"])
def nuevo_expediente():
    db = SessionLocal()

    if request.method == "POST":
        caratula = request.form["caratula"]
        jurisdiccion = request.form["jurisdiccion"]
        tipo = request.form["tipo"]

        exp = Expediente(
            caratula=caratula,
            jurisdiccion=jurisdiccion,
            tipo_proceso=tipo
        )

        db.add(exp)
        db.commit()

        return redirect(url_for("dashboard"))

    return render_template("nuevo_expediente.html")

@app.route("/generar/<int:id>")
def generar_documento(id):

    db = SessionLocal()

    plazo = db.get(Plazo, id)

    generar_documento_desde_plazo(plazo.id)

    db.refresh(plazo)

    expediente = db.query(Expediente).options(
        joinedload(Expediente.documentos)
    ).get(plazo.expediente_id)

    response = render_template(
        "components/documentos_list.html",
        exp=expediente
    )

    db.close()

    return response

@app.route("/expediente/<int:id>")
def ver_expediente(id):
    db = SessionLocal()

    expediente = db.query(Expediente).options(
        joinedload(Expediente.partes),
        joinedload(Expediente.plazos),
        joinedload(Expediente.documentos),
        joinedload(Expediente.actuaciones),
        joinedload(Expediente.historial_estados)
    ).get(id)

    if not expediente:
        db.close()
        return "Expediente no encontrado", 404

    expediente.documentos.sort(key=lambda d: d.id, reverse=True)

    docs_unicos = {}
    for d in expediente.documentos:
        docs_unicos[d.tipo.upper()] = d

    expediente.documentos = list(docs_unicos.values())

    eventos = []

    for a in expediente.actuaciones:
        eventos.append({
            "fecha": a.fecha,
            "tipo": "ACTUACION",
            "titulo": a.tipo,
            "detalle": a.descripcion
        })

    for p in expediente.plazos:
        eventos.append({
            "fecha": p.fecha_inicio,
            "tipo": "PLAZO",
            "titulo": p.tipo,
            "detalle": f"Vence: {p.fecha_vencimiento}"
        })

    for d in expediente.documentos:
        eventos.append({
            "fecha": getattr(d, "created_at", None),
            "tipo": "DOCUMENTO",
            "titulo": d.tipo,
            "detalle": "Documento generado"
        })
    
    for h in expediente.historial_estados:
        eventos.append({
            "tipo": "ESTADO",
            "fecha": h.fecha,
            "titulo": f"{h.estado_anterior or 'INICIO'} → {h.estado_nuevo}",
            "detalle": "Cambio de estado procesal"
        })

    hoy = date.today()

    def clasificar_evento(e):
        if not e["fecha"]:
            return "historico"

        f = e["fecha"]
        if hasattr(f, "date"):
            f = f.date()

        if f == hoy:
            return "hoy"
        elif (hoy - f).days <= 2:
            return "reciente"
        else:
            return "historico"

    def prioridad_evento(e):
        if e["tipo"] == "PLAZO":
            return "alta"
        elif e["tipo"] == "DOCUMENTO":
            return "media"
        return "baja"

    def accion_evento(e):
        if e["tipo"] == "PLAZO" and "Traslado" in e["titulo"]:
            return "Preparar contestación"
        return None
    
    for e in eventos:
        e["categoria"] = clasificar_evento(e)
        e["prioridad"] = prioridad_evento(e)
        e["accion"] = accion_evento(e)

    def normalizar_fecha(f):
        if f is None:
            return datetime.min
        if isinstance(f, datetime):
            return f
        return datetime.combine(f, datetime.min.time())

    eventos.sort(
        key=lambda e: normalizar_fecha(e["fecha"]),
        reverse=True
    )

    eventos_agrupados = {
        "hoy": [],
        "reciente": [],
        "historico": []
    }

    for e in eventos:
        eventos_agrupados[e["categoria"]].append(e)

    db.close()

    return render_template(
        "expediente.html",
        exp=expediente,
        eventos=eventos,
        eventos_agrupados=eventos_agrupados
    )

@app.route("/documento/<int:id>")
def ver_documento(id):
    db = SessionLocal()

    doc = db.query(Documento).options(
        joinedload(Documento.expediente)
    ).get(id)

    db.close()

    return render_template("documento.html", doc=doc)

@app.route("/plazo/<int:id>/cumplir")
def cumplir_plazo(id):

    db = SessionLocal()

    plazo = db.get(Plazo, id)

    plazo.cumplido = True

    db.commit()

    db.refresh(plazo)

    response = render_template(
        "components/plazo_item.html",
        pl=plazo
    )

    db.close()

    return response

@app.route("/reglas/nueva")
def nueva_regla():
    return render_template("nueva_regla.html")

@app.route("/reglas/crear", methods=["POST"])
def crear_regla():
    db = SessionLocal()

    regla = ReglaProcesal(
        evento=request.form["evento"].lower(),
        estado_destino=request.form["estado"],
        generar_documento=bool(request.form.get("generar_documento")),
        template=request.form.get("template"),
        crear_plazo=bool(request.form.get("crear_plazo")),
        dias_plazo=int(request.form.get("dias_plazo") or 0)
    )

    db.add(regla)
    db.commit()
    db.close()

    return redirect("/reglas")

@app.route(
    "/expediente/<int:id>/actuacion/nueva",
    methods=["GET", "POST"]
)
def nueva_actuacion(id):

    db = SessionLocal()

    try:
        expediente = db.get(Expediente, id)

        if expediente is None:
            abort(404)

        # Mostrar formulario
        if request.method == "GET":
            return render_template(
                "nueva_actuacion.html",
                exp=expediente
            )

        # Recibir datos del formulario
        tipo = request.form.get("tipo", "").strip()
        descripcion = request.form.get("descripcion", "").strip()

        if not tipo or not descripcion:
            flash("Debe completar el tipo y la descripción.")
            return redirect(
                url_for("nueva_actuacion", id=id)
            )

        # Crear actuación
        actuacion = Actuacion(
            tipo=tipo,
            descripcion=descripcion,
            fecha=date.today(),
            expediente_id=id
        )

        db.add(actuacion)
        db.flush()

        # Registrar evento asociado
        registrar_evento(
            db,
            tipo="ACTUACION",
            descripcion=f"Actuación '{tipo}' registrada",
            expediente_id=expediente.id,
            actuacion_id=actuacion.id
        )

        # Aplicar reglas procesales
        aplicar_reglas(expediente, actuacion, db)

        # Confirmar toda la operación
        db.commit()

        flash("Actuación creada correctamente.")

        return redirect(
            url_for("ver_expediente", id=id)
        )

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()

@app.route("/reglas")
def listar_reglas():

    db = SessionLocal()

    reglas = db.query(ReglaProcesal).all()

    db.close()

    return render_template(
        "reglas.html",
        reglas=reglas
    )

@app.route("/reglas/<int:id>/toggle")
def toggle_regla(id):

    db = SessionLocal()

    regla = db.get(ReglaProcesal, id)

    regla.activa = not regla.activa

    db.commit()

    db.close()

    return redirect("/reglas")

@app.route("/reglas/<int:id>/editar")
def editar_regla(id):

    db = SessionLocal()

    regla = db.get(ReglaProcesal, id)

    db.close()

    return render_template(
        "editar_regla.html",
        regla=regla
    )

@app.route("/reglas/<int:id>/update", methods=["POST"])
def update_regla(id):

    db = SessionLocal()

    regla = db.get(ReglaProcesal, id)

    regla.evento = request.form["evento"]

    regla.estado_destino = request.form["estado_destino"]

    regla.template = request.form["template"]

    regra_dias = request.form["dias_plazo"]

    if regra_dias:
        regla.dias_plazo = int(regra_dias)

    db.commit()

    db.close()

    return redirect("/reglas")

@app.route("/expedientes")
def listar_expedientes():

    db = SessionLocal()

    expedientes = db.query(Expediente).all()

    db.close()

    return render_template(
        "expedientes.html",
        expedientes=expedientes
    )

@app.route("/expediente/<int:id>/timeline")
def timeline_partial(id):

    db = SessionLocal()

    try:
        exp = db.get(Expediente, id)

        if exp is None:
            abort(404)

        eventos = obtener_timeline_expediente(
            db,
            exp.id
        )

        return render_template(
            "components/timeline.html",
            eventos=eventos
        )

    finally:
        db.close()

@app.route("/expediente/<int:expediente_id>/evento/<int:evento_id>")
def ver_detalle_evento(expediente_id, evento_id):

    db = SessionLocal()

    try:
        detalle = obtener_detalle_evento(
            db,
            expediente_id,
            evento_id
        )

        if detalle is None:
            abort(404)

        return render_template(
            "evento_detalle.html",
            detalle=detalle
        )

    finally:
        db.close()


@app.route("/eventos")
def ver_eventos():

    db = SessionLocal()

    eventos = db.query(EventoSistema)\
        .order_by(EventoSistema.fecha.desc())\
        .all()

    db.close()

    return render_template(
        "eventos.html",
        eventos=eventos
    )

@app.route("/expediente/<int:id>/workflow")
def workflow_expediente(id):

    db = SessionLocal()

    try:
        exp = db.get(Expediente, id)

        if exp is None:
            abort(404)

        graph = generar_mermaid_expediente(
            db,
            exp.id
        )

        return render_template(
            "components/workflow_graph.html",
            graph=graph
        )

    finally:
        db.close()

if __name__ == "__main__":
    app.run(debug=True)