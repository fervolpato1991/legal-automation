from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.db.db import Base

class Actuacion(Base):
    __tablename__ = "actuaciones"

    id = Column(Integer, primary_key=True)
    tipo = Column(String)
    fecha = Column(Date)
    descripcion = Column(String)

    expediente_id = Column(Integer, ForeignKey("expedientes.id"))

    expediente = relationship("Expediente", back_populates="actuaciones")