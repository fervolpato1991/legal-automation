from datetime import date, timedelta

from app.models import ReglaProcesal, Plazo, Documento
from app.services.workflow_service import cambiar_estado
from app.services.template_engine import render_template


def aplicar_reglas(expediente, actuacion, db):
    
    reglas = db.query(ReglaProcesal).filter_by(
        evento=actuacion.tipo.lower()
    ).all()

    for regla in reglas:

        if regla.estado_destino:
            cambiar_estado(expediente, regla.estado_destino, db)

        if regla.crear_plazo:

            existente = db.query(Plazo).filter_by(
                expediente_id=expediente.id,
                tipo=regla.evento,
                cumplido=False
            ).first()

            if not existente:
                nuevo_plazo = Plazo(
                    tipo=regla.evento,
                    fecha_inicio=date.today(),
                    fecha_vencimiento=date.today() + timedelta(days=regla.dias_plazo),
                    cumplido=False,
                    expediente_id=expediente.id
                )
                db.add(nuevo_plazo)

        if regla.generar_documento:

            existente_doc = db.query(Documento).filter_by(
                expediente_id=expediente.id,
                tipo=regla.evento
            ).first()

            if not existente_doc:
                contenido = render_template(regla.template, expediente)

                doc = Documento(
                    tipo=regla.evento,
                    contenido=contenido,
                    expediente_id=expediente.id
                )

                db.add(doc)