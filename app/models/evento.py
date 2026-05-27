from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Text
)

from sqlalchemy.orm import relationship

from sqlalchemy.sql import func

from app.db.db import Base


class EventoSistema(Base):

    __tablename__ = "eventos_sistema"

    id = Column(Integer, primary_key=True)

    tipo = Column(String, nullable=False)

    descripcion = Column(Text)

    fecha = Column(
        DateTime,
        default=func.now()
    )

    expediente_id = Column(
        Integer,
        ForeignKey("expedientes.id"),
        nullable=True
    )

    actuacion_id = Column(
        Integer,
        ForeignKey("actuaciones.id"),
        nullable=True
    )

    regla_id = Column(
        Integer,
        ForeignKey("reglas_procesales.id"),
        nullable=True
    )

    datos = Column(Text)

    expediente = relationship("Expediente")

    actuacion = relationship("Actuacion")

    regla = relationship("ReglaProcesal")