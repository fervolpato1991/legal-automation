from datetime import date, timedelta

from app.models.regla import ReglaProcesal
from app.models.plazo import Plazo
from app.models.documento import Documento

from app.services.workflow_service import cambiar_estado
from app.services.template_engine import render_template


def evaluar_condicion(regla, expediente, db):
    if not regla.condicion:
        return True

    if regla.condicion == "no_existe_plazo":
        existe = db.query(Plazo).filter_by(
            expediente_id=expediente.id,
            tipo=regla.evento,
            cumplido=False
        ).first()
        return not existe

    return True


def aplicar_reglas(expediente, actuacion, db):

    reglas = db.query(ReglaProcesal).filter_by(
        evento=actuacion.tipo.lower()
    ).all()

    for regla in reglas:

        if not regla.activa:
            continue

        if not evaluar_condicion(regla, expediente, db):
            continue

        # ⚠️ evitar duplicación lógica
        if regla.unica:
            existente = db.query(Documento).filter_by(
                expediente_id=expediente.id,
                tipo=regla.evento
            ).first()

            if existente:
                print(f"⚠️ Regla '{regla.evento}' ya aplicada")
                continue

        # 🔁 estado
        if regla.estado_destino:
            cambiar_estado(expediente, regla.estado_destino, db)

        # ⏳ plazo
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
                    fecha_vencimiento=date.today() + timedelta(days=regla.dias_plazo or 0),
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
                contenido = render_template(
                    regla.template,
                    {
                        "expediente": expediente,
                        "actuacion": actuacion
                    }
                )

                doc = Documento(
                    tipo=regla.evento,
                    contenido=contenido,
                    expediente_id=expediente.id
                )

                db.add(doc)