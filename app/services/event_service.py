from app.models.evento import EventoSistema


def registrar_evento(
    db,
    tipo,
    descripcion,
    expediente_id=None,
    actuacion_id=None,
    regla_id=None,
    datos=None
):

    evento = EventoSistema(
        tipo=tipo,
        descripcion=descripcion,
        expediente_id=expediente_id,
        actuacion_id=actuacion_id,
        regla_id=regla_id,
        datos=datos
    )

    db.add(evento)