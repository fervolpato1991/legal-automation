from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.db import Base

class Plazo(Base):
    __tablename__ = "plazos"

    id = Column(Integer, primary_key=True)
    tipo = Column(String)
    fecha_inicio = Column(Date)
    fecha_vencimiento = Column(Date)
    cumplido = Column(Boolean, default=False)

    expediente_id = Column(Integer, ForeignKey("expedientes.id"))

    expediente = relationship("Expediente", back_populates="plazos")

    __table_args__ = (
        UniqueConstraint(
            "expediente_id",
            "tipo",
            "fecha_vencimiento",
            name="uq_plazo_unico"
        ),
    )