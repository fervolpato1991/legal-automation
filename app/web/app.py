from flask import Flask, render_template, redirect, url_for
from app.services.alert_service import obtener_dashboard_plazos
from app.services.action_rules import sugerir_accion
from app.services.action_executor import generar_documento_desde_plazo
from app.models.plazo import Plazo
from app.models.expediente import Expediente
from app.models.documento import Documento
from flask import flash, abort
from app.db.db import SessionLocal
from sqlalchemy.orm import joinedload

app = Flask(__name__)
app.secret_key = "clave-super-secreta"


@app.route("/")
def dashboard():
    data = obtener_dashboard_plazos()

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

    return render_template(
        "dashboard.html",
        vencidos=enrich(data["vencidos"]),
        proximos=enrich(data["proximos"]),
        futuros=enrich(data["futuros"])
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
        joinedload(Expediente.documentos)
    ).get(id)

    expediente.documentos.sort(key=lambda d: d.id, reverse=True)

    docs_unicos = {}
    for d in expediente.documentos:
        docs_unicos[d.tipo.upper()] = d

    expediente.documentos = list(docs_unicos.values())

    db.close()

    return render_template("expediente.html", exp=expediente)

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

    plazo = db.query(Plazo).get(id)

    if plazo:
        plazo.cumplido = True
        db.commit()

        expediente_id = plazo.expediente_id

    db.close()

    return redirect(f"/expediente/{expediente_id}")

if __name__ == "__main__":
    app.run(debug=True)