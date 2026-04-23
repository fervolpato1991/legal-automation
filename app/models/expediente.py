from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.db import Base

class Expediente(Base):
    __tablename__ = "expedientes"

    id = Column(Integer, primary_key=True, index=True)
    caratula = Column(String, nullable=False)
    numero = Column(String)
    jurisdiccion = Column(String)
    juzgado = Column(String)
    tipo_proceso = Column(String)
    estado_id = Column(Integer, ForeignKey("estados_procesales.id"))

    estado = relationship("EstadoProcesal")
    partes = relationship("Parte", back_populates="expediente")
    actuaciones = relationship("Actuacion", back_populates="expediente")
    plazos = relationship("Plazo", back_populates="expediente")