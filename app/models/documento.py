from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.db import Base
from datetime import datetime
from sqlalchemy import DateTime
class Documento(Base):
    __tablename__ = "documentos"

    id = Column(Integer, primary_key=True)
    tipo = Column(String)
    contenido = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    expediente_id = Column(Integer, ForeignKey("expedientes.id"))

    expediente = relationship("Expediente", back_populates="documentos")