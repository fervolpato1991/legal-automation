from app.models.evento import EventoSistema

def registrar_evento(db, tipo, descripcion):

    evento = EventoSistema(
        tipo=tipo,
        descripcion=descripcion
    )

    db.add(evento)