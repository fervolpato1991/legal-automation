from app.db.db import SessionLocal
from app.models.plazo import Plazo
from app.models.documento import Documento
from app.services.action_rules import sugerir_accion
from app.services.template_engine import render_template


def generar_documento_desde_plazo(plazo_id):
    db = SessionLocal()

    plazo = db.query(Plazo).get(plazo_id)
    exp = plazo.expediente

    doc_existente = db.query(Documento).filter_by(
        expediente_id=exp.id,
        tipo=plazo.tipo
    ).first()

    if doc_existente:
        db.close()
        return "Documento ya generado"

    sugerencia = sugerir_accion(plazo)

    if not sugerencia or "documento" not in sugerencia:
        db.close()
        return None

    template_name = sugerencia["documento"]

    actor = None
    demandado = None

    for p in exp.partes:
        if p.tipo == "actor":
            actor = p
        elif p.tipo == "demandado":
            demandado = p

    contexto = {
        "expediente": exp,
        "actor": actor,
        "demandado": demandado,
    }

    contenido = render_template(template_name, contexto)

    doc = Documento(
        expediente_id=exp.id,
        tipo=plazo.tipo,
        contenido=contenido
    )

    db.add(doc)
    
    plazo.cumplido = True

    db.commit()
    db.close()

    return contenido