from app.db.db import SessionLocal
from app.models.plazo import Plazo
from app.models.documento import Documento
from app.services.action_rules import sugerir_accion
from app.services.template_engine import render_template


def generar_documento_desde_plazo(plazo_id):
    db = SessionLocal()

    # 1. traer plazo + expediente + partes
    plazo = db.query(Plazo).get(plazo_id)
    exp = plazo.expediente

    # 🔴 VALIDACIÓN: evitar duplicados
    doc_existente = db.query(Documento).filter_by(
        expediente_id=exp.id,
        tipo=plazo.tipo
    ).first()

    if doc_existente:
        db.close()
        return "Documento ya generado"

    # 2. obtener sugerencia
    sugerencia = sugerir_accion(plazo)

    if not sugerencia or "documento" not in sugerencia:
        db.close()
        return None

    template_name = sugerencia["documento"]

    # 3. obtener partes
    actor = None
    demandado = None

    for p in exp.partes:
        if p.tipo == "actor":
            actor = p
        elif p.tipo == "demandado":
            demandado = p

    # 4. contexto
    contexto = {
        "expediente": exp,
        "actor": actor,
        "demandado": demandado,
    }

    # 5. generar contenido
    contenido = render_template(template_name, contexto)

    # 6. guardar documento
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