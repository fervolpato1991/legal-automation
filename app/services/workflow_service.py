from app.models.estado import EstadoProcesal
from app.models.historial_estado import HistorialEstado
from datetime import datetime

def cambiar_estado(expediente, nuevo_estado, db, actuacion=None, regla=None):

    estado_anterior = None

    if expediente.estado:
        estado_anterior = expediente.estado.nombre

    estado = db.query(EstadoProcesal).filter_by(
        nombre=nuevo_estado
    ).first()

    if not estado:
        print("❌ Estado no encontrado")
        return

    historial = HistorialEstado(
        expediente_id=expediente.id,
        actuacion_id=actuacion.id if actuacion else None,
        regla_id=regla.id if regla else None,
        estado_anterior=estado_anterior,
        estado_nuevo=nuevo_estado,
        fecha=datetime.utcnow()
    )
    print("📌 Creando historial")

    db.add(historial)

    expediente.estado = estado
    print("✅ Estado actualizado")