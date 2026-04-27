from flask import Flask, render_template, redirect, url_for
from app.services.alert_service import obtener_dashboard_plazos
from app.services.action_rules import sugerir_accion
from app.services.action_executor import generar_documento_desde_plazo
from app.models.plazo import Plazo
from app.models.expediente import Expediente
from app.models.documento import Documento
from app.models.actuacion import Actuacion
from flask import flash, request
from app.db.db import SessionLocal
from sqlalchemy.orm import joinedload
from datetime import datetime, date

app = Flask(__name__)
app.secret_key = "clave-super-secreta"


@app.route("/")
def dashboard():
    data = obtener_dashboard_plazos()
    db = SessionLocal()

    def enrich(plazos):
        resultado = []
        for p in plazos:
            sugerencia = sugerir_accion(p)
            resultado.append({
                "id": p.id,
                "expediente_id": p.expediente.id,
                "caratula": p.expediente.caratula,
                "tipo": p.tipo,
                "vence": p.fecha_vencimiento,
                "accion": sugerencia["accion"] if sugerencia else "",
            })
        return resultado

    expedientes = db.query(Expediente).all()

    return render_template(
        "dashboard.html",
        vencidos=enrich(data["vencidos"]),
        proximos=enrich(data["proximos"]),
        futuros=enrich(data["futuros"]),
        expedientes=expedientes
    )


@app.route("/generar/<int:plazo_id>")
def generar(plazo_id):
    generar_documento_desde_plazo(plazo_id)
    flash("Documento generado correctamente")
    return redirect(url_for("dashboard"))

@app.route("/expediente/<int:id>")
def ver_expediente(id):
    db = SessionLocal()

    expediente = db.query(Expediente).options(
        joinedload(Expediente.partes),
        joinedload(Expediente.plazos),
        joinedload(Expediente.documentos),
        joinedload(Expediente.actuaciones)
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

    db.close()

    return render_template("expediente.html", exp=expediente, eventos=eventos)


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

    plazo = db.query(Plazo).options(
        joinedload(Plazo.expediente)
    ).get(id)

    if plazo:
        plazo.cumplido = True
        db.commit()

        expediente_id = plazo.expediente_id

    db.close()

    return redirect(f"/expediente/{expediente_id}")

@app.route("/expediente/<int:id>/actuacion/nueva")
def nueva_actuacion(id):
    return render_template("nueva_actuacion.html", expediente_id=id)


@app.route("/expediente/<int:id>/actuacion/nueva", methods=["POST"])
def crear_actuacion(id):
    db = SessionLocal()

    tipo = request.form["tipo"]
    descripcion = request.form["descripcion"]

    actuacion = Actuacion(
        tipo=tipo,
        fecha=date.today(),
        descripcion=descripcion,
        expediente_id=id
    )

    db.add(actuacion)
    db.commit()
    db.close()

    return redirect(f"/expediente/{id}")

if __name__ == "__main__":
    app.run(debug=True)