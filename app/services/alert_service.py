from datetime import date, timedelta
from app.db.db import SessionLocal
from app.models.plazo import Plazo


def obtener_plazos_proximos(dias=3):
    db = SessionLocal()

    hoy = date.today()
    limite = hoy + timedelta(days=dias)

    plazos = db.query(Plazo).filter(
        Plazo.cumplido == False,
        Plazo.fecha_vencimiento <= limite
    ).order_by(Plazo.fecha_vencimiento.asc()).all()

    return plazos