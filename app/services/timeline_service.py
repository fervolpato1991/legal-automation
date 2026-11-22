from app.models.evento import EventoSistema


def obtener_timeline_expediente(db, expediente_id):

    eventos = db.query(EventoSistema)\
        .filter_by(expediente_id=expediente_id)\
        .order_by(EventoSistema.fecha.desc())\
        .all()

    timeline = []

    for evento in eventos:

        item = {
            "id": evento.id,
            "tipo": evento.tipo,
            "descripcion": evento.descripcion,
            "fecha": evento.fecha,
            "actuacion_id": evento.actuacion_id,
            "expediente_id": evento.expediente_id,
            "regla_id": evento.regla_id
        }

        timeline.append(item)

    return timeline