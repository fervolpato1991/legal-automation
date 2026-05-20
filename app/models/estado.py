from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.db import Base

class EstadoProcesal(Base):
    __tablename__ = "estados_procesales"

    id = Column(Integer, primary_key=True)
    nombre = Column(String, unique=True)
    orden = Column(Integer)

    expedientes = relationship("Expediente", back_populates="estado")