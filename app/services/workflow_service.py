from app.models.estado import EstadoProcesal

def cambiar_estado(expediente, nombre_estado, db):
    estado = db.query(EstadoProcesal).filter_by(nombre=nombre_estado).first()
    if estado:
        expediente.estado_id = estado.id