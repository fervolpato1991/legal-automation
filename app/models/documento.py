from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.db import Base

class Documento(Base):
    __tablename__ = "documentos"

    id = Column(Integer, primary_key=True)
    tipo = Column(String)
    contenido = Column(String)

    expediente_id = Column(Integer, ForeignKey("expedientes.id"))

    expediente = relationship("Expediente")