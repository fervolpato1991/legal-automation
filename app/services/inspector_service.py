
from sqlalchemy.orm import joinedload

from app.models.evento import EventoSistema


def obtener_detalle_evento(db, expediente_id, evento_id):
    """
    Recupera el detalle de un evento perteneciente a un expediente.

    Devuelve un diccionario con los datos del evento y sus relaciones.
    Si el evento no existe o no pertenece al expediente, devuelve None.
    """

    evento = (
        db.query(EventoSistema)
        .options(
            joinedload(EventoSistema.expediente),
            joinedload(EventoSistema.actuacion),
            joinedload(EventoSistema.regla)
        )
        .filter(
            EventoSistema.id == evento_id,
            EventoSistema.expediente_id == expediente_id
        )
        .one_or_none()
    )

    if evento is None:
        return None

    expediente = evento.expediente
    actuacion = evento.actuacion
    regla = evento.regla

    return {
        "evento": {
            "id": evento.id,
            "tipo": evento.tipo,
            "descripcion": evento.descripcion,
            "fecha": evento.fecha,
            "datos": evento.datos
        },

        "expediente": {
            "id": expediente.id,
            "caratula": expediente.caratula,
            "numero": expediente.numero,
            "jurisdiccion": expediente.jurisdiccion,
            "juzgado": expediente.juzgado,
            "tipo_proceso": expediente.tipo_proceso
        } if expediente else None,

        "actuacion": {
            "id": actuacion.id,
            "tipo": actuacion.tipo,
            "fecha": actuacion.fecha,
            "descripcion": actuacion.descripcion
        } if actuacion else None,

        "regla": {
            "id": regla.id,
            "evento": regla.evento,
            "estado_destino": regla.estado_destino,
            "generar_documento": regla.generar_documento,
            "template": regla.template,
            "crear_plazo": regla.crear_plazo,
            "dias_plazo": regla.dias_plazo,
            "condicion": regla.condicion,
            "activa": regla.activa,
            "unica": regla.unica
        } if regla else None
    }