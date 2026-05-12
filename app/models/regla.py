from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.db.db import Base

class ReglaProcesal(Base):
    __tablename__ = "reglas_procesales"

    id = Column(Integer, primary_key=True)
    evento = Column(String)
    estado_destino = Column(String)
    generar_documento = Column(Boolean)
    template = Column(String)
    crear_plazo = Column(Boolean)
    dias_plazo = Column(Integer)
    condicion = Column(String)
    activa = Column(Boolean, default=True)
    unica = Column(Boolean, default=False)