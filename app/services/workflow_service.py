from datetime import date

from app.db.db import SessionLocal
from app.models.actuacion import Actuacion
from app.models.expediente import Expediente
from app.models.estado import EstadoProcesal
from app.models.documento import Documento
from app.models.plazo import Plazo

from app.services.rules import obtener_nuevo_estado_por_actuacion
from app.services.template_selector import seleccionar_template_por_estado
from app.services.template_engine import render_template
from app.services.plazo_service import sumar_dias_habiles
from app.services.rules import obtener_plazo_por_actuacion


def procesar_actuacion(expediente_id, tipo, descripcion, contexto_extra=None):
    db = SessionLocal()

    exp = db.get(Expediente, expediente_id)

    act = Actuacion(
        tipo=tipo,
        fecha=date.today(),
        descripcion=descripcion,
        expediente_id=expediente_id
    )
    db.add(act)

    nuevo_estado_nombre = obtener_nuevo_estado_por_actuacion(tipo)

    if nuevo_estado_nombre:
        nuevo_estado = db.query(EstadoProcesal)\
            .filter_by(nombre=nuevo_estado_nombre)\
            .first()

        if nuevo_estado:
            exp.estado = nuevo_estado

    dias_plazo = obtener_plazo_por_actuacion(tipo)

    if dias_plazo:
        fecha_inicio = act.fecha
        fecha_vencimiento = sumar_dias_habiles(fecha_inicio, dias_plazo)

        plazo = Plazo(
            tipo=tipo,
            fecha_inicio=fecha_inicio,
            fecha_vencimiento=fecha_vencimiento,
            expediente_id=expediente_id
        )

        db.add(plazo)

    template_name = seleccionar_template_por_estado(exp)

    documento_generado = None

    if template_name:
        actor = None
        demandado = None

        for p in exp.partes:
            print(f"TIPO RAW: '{p.tipo}' | NOMBRE: {p.nombre}")

        actor = next(
             (p for p in exp.partes if p.tipo.strip().lower() == "actor"),
             None
        )
        demandado = next(
            (p for p in exp.partes if p.tipo.strip().lower() == "demandado"),
            None
        )

        contexto = {
            "expediente": exp,
            "actor": actor.nombre if actor else "",
            "demandado": demandado.nombre if demandado else "",
        }

        if contexto_extra:
            contexto.update(contexto_extra)

        contenido = render_template(template_name, contexto)

        doc = Documento(
            expediente_id=expediente_id,
            tipo=tipo.lower(),
            contenido=contenido
        )

        db.add(doc)

        documento_generado = contenido

    db.commit()
    db.close()

    return documento_generado