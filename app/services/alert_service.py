from datetime import date, timedelta
from app.db.db import SessionLocal
from app.models.plazo import Plazo
from sqlalchemy.orm import joinedload


def obtener_dashboard_plazos():
    db = SessionLocal()

    hoy = date.today()
    limite = hoy + timedelta(days=3)

    vencidos = db.query(Plazo).options(
        joinedload(Plazo.expediente)
    ).filter(
        Plazo.fecha_vencimiento < hoy,
        Plazo.cumplido == False
    ).order_by(Plazo.fecha_vencimiento.asc()).all()

    proximos = db.query(Plazo).options(
        joinedload(Plazo.expediente)
    ).filter(
        Plazo.fecha_vencimiento >= hoy,
        Plazo.fecha_vencimiento <= limite,
        Plazo.cumplido == False
    ).order_by(Plazo.fecha_vencimiento.asc()).all()

    futuros = db.query(Plazo).options(
        joinedload(Plazo.expediente)
    ).filter(
        Plazo.fecha_vencimiento > limite,
        Plazo.cumplido == False
    ).order_by(Plazo.fecha_vencimiento.asc()).all()

    db.close()

    return {
        "vencidos": vencidos,
        "proximos": proximos,
        "futuros": futuros
    }