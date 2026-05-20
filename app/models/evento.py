from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.sql import func
from app.db.db import Base

class EventoSistema(Base):
    __tablename__ = "eventos_sistema"

    id = Column(Integer, primary_key=True)

    tipo = Column(String)
    descripcion = Column(String)

    fecha = Column(DateTime, default=func.now())