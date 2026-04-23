from sqlalchemy import Column, Integer, String
from app.db.db import Base

class EstadoProcesal(Base):
    __tablename__ = "estados_procesales"

    id = Column(Integer, primary_key=True)
    nombre = Column(String, unique=True)
    orden = Column(Integer)