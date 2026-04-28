from datetime import date, timedelta

from app.models.documento import Documento
from app.models.plazo import Plazo
from app.services.template_service import render_template
from app.services.workflow_service import cambiar_estado


def regla_traslado(expediente, actuacion, db):
    if "traslado" not in actuacion.tipo.lower():
        return

    cambiar_estado(expediente, "TRASLADO_NOTIFICADO", db)

    fecha_vencimiento = date.today() + timedelta(days=5)
    
    with db.no_autoflush:
        plazo_existente = db.query(Plazo).filter_by(
            expediente_id=expediente.id,
            tipo="Traslado",
            fecha_vencimiento=fecha_vencimiento
            ).first()
        
    if not plazo_existente:
        nuevo_plazo = Plazo(
            tipo="Traslado",
            fecha_inicio=date.today(),
            fecha_vencimiento=fecha_vencimiento,
            cumplido=False,
            expediente_id=expediente.id
        )
        
        db.add(nuevo_plazo)

    if plazo_existente:
        print("⚠️ Plazo ya existente, no se crea duplicado")
        return

    existente = db.query(Documento).filter_by(
        expediente_id=expediente.id,
        tipo="traslado"
    ).first()

    if existente:
        return

    contenido = render_template("amparo_contestacion.txt", expediente)

    doc = Documento(
        tipo="traslado",
        contenido=contenido,
        expediente_id=expediente.id
    )

    db.add(doc)

    print("⚙️ Documento de traslado generado automáticamente")


def regla_contestacion(expediente, actuacion, db):
    if "contestacion" not in actuacion.tipo.lower():
        return

    cambiar_estado(expediente, "CONTESTACION_PRESENTADA", db)

    plazo = db.query(Plazo).filter_by(
        expediente_id=expediente.id,
        tipo="Traslado",
        cumplido=False
    ).first()

    if plazo:
        plazo.cumplido = True


def ejecutar_reglas(expediente, actuacion, db):
    reglas = [
        regla_traslado,
        regla_contestacion,
    ]

    for regla in reglas:
        regla(expediente, actuacion, db)