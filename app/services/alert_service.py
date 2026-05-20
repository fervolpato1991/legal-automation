from datetime import date, timedelta

from sqlalchemy.orm import joinedload

from app.db.db import SessionLocal
from app.models.plazo import Plazo
from app.models.expediente import Expediente


def obtener_dashboard_plazos():

    db = SessionLocal()

    try:

        hoy = date.today()

        limite = hoy + timedelta(days=3)

        base_query = db.query(Plazo).options(

            joinedload(Plazo.expediente)
                .joinedload(Expediente.plazos),

            joinedload(Plazo.expediente)
                .joinedload(Expediente.documentos),

            joinedload(Plazo.expediente)
                .joinedload(Expediente.estado)

        ).filter(
            Plazo.cumplido == False
        )

        vencidos = base_query.filter(
            Plazo.fecha_vencimiento < hoy
        ).order_by(
            Plazo.fecha_vencimiento.asc()
        ).all()

        proximos = base_query.filter(
            Plazo.fecha_vencimiento >= hoy,
            Plazo.fecha_vencimiento <= limite
        ).order_by(
            Plazo.fecha_vencimiento.asc()
        ).all()

        futuros = base_query.filter(
            Plazo.fecha_vencimiento > limite
        ).order_by(
            Plazo.fecha_vencimiento.asc()
        ).all()

        return {
            "vencidos": vencidos,
            "proximos": proximos,
            "futuros": futuros
        }

    finally:

        db.close()