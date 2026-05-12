from datetime import date

from app.db.db import SessionLocal
from app.models.actuacion import Actuacion
from app.models.expediente import Expediente

from app.services.regla_service import aplicar_reglas


def procesar_actuacion(expediente_id, tipo, descripcion):
    db = SessionLocal()

    exp = db.get(Expediente, expediente_id)

    act = Actuacion(
        tipo=tipo,
        fecha=date.today(),
        descripcion=descripcion,
        expediente_id=expediente_id
    )

    db.add(act)

    aplicar_reglas(exp, act, db)

    db.commit()
    db.close()

    return True