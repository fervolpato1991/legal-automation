from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.db import Base

class HistorialEstado(Base):

    __tablename__ = "historial_estados"

    id = Column(Integer, primary_key=True)

    expediente_id = Column(
        Integer,
        ForeignKey("expedientes.id")
    )

    actuacion_id = Column(
        Integer,
        ForeignKey("actuaciones.id"),
        nullable=True
    )

    estado_anterior = Column(String)

    estado_nuevo = Column(String)

    fecha = Column(
        DateTime,
        default=datetime.utcnow
    )

    expediente = relationship("Expediente", back_populates="historial_estados")

    actuacion = relationship("Actuacion")