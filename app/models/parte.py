from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.db import Base

class Parte(Base):
    __tablename__ = "partes"

    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    tipo = Column(String)
    domicilio = Column(String)

    expediente_id = Column(Integer, ForeignKey("expedientes.id"))

    expediente = relationship("Expediente", back_populates="partes")