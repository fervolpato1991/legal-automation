from app.db.db import SessionLocal
from app.models import EstadoProcesal

db = SessionLocal()

estados = [
    ("INICIO", 1),
    ("DEMANDA_PRESENTADA", 2),
    ("TRASLADO", 3),
    ("CONTESTACION", 4),
    ("PRUEBA", 5),
    ("SENTENCIA", 6),
]

for nombre, orden in estados:
    estado = EstadoProcesal(nombre=nombre, orden=orden)
    db.add(estado)

db.commit()
db.close()