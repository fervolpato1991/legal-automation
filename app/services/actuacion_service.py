from datetime import date

from app.db.db import SessionLocal
from app.models.actuacion import Actuacion
from app.models.expediente import Expediente

from app.services.rules_engine import ejecutar_reglas


def procesar_actuacion(expediente_id, tipo, descripcion, contexto_extra=None):
    db = SessionLocal()

    exp = db.get(Expediente, expediente_id)

    if not exp:
        db.close()
        return False

    act = Actuacion(
        tipo=tipo,
        fecha=date.today(),
        descripcion=descripcion,
        expediente_id=expediente_id
    )

    db.add(act)

    ejecutar_reglas(exp, act, db)

    db.commit()
    db.close()

    return True