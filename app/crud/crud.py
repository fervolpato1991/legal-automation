from app.db.db import SessionLocal
from app.models import Expediente, Parte, Actuacion, Plazo, Documento, EstadoProcesal
from app.services.rules import obtener_nuevo_estado_por_actuacion
from sqlalchemy.orm import selectinload, joinedload

def crear_expediente(caratula, jurisdiccion, tipo_proceso):
    db = SessionLocal()

    estado_inicial = db.query(EstadoProcesal)\
        .filter(EstadoProcesal.nombre == "INICIO")\
        .first()

    if not estado_inicial:
        raise Exception("No existe el estado INICIO")

    exp = Expediente(
        caratula=caratula,
        jurisdiccion=jurisdiccion,
        tipo_proceso=tipo_proceso,
        estado_id=estado_inicial.id
    )

    db.add(exp)
    db.commit()
    db.refresh(exp)
    db.close()

    return exp

def agregar_parte(expediente_id, nombre, tipo, domicilio):
    db = SessionLocal()
    
    parte = Parte(
        nombre=nombre,
        tipo=tipo,
        domicilio=domicilio,
        expediente_id=expediente_id
    )
    
    db.add(parte)
    db.commit()
    db.close()

def listar_expedientes():
    db = SessionLocal()
    
    exps = db.query(Expediente)\
        .options(
            selectinload(Expediente.partes),
            selectinload(Expediente.actuaciones)
        )\
        .all()
    
    db.close()
    return exps

def obtener_expediente_completo(expediente_id):
    db = SessionLocal()
    
    exp = db.query(Expediente)\
        .options(
            joinedload(Expediente.partes),
            joinedload(Expediente.estado)
        )\
        .filter(Expediente.id == expediente_id)\
        .first()
    
    actor = None
    demandado = None
    
    for p in exp.partes:
        if p.tipo == "actor":
            actor = p
        elif p.tipo == "demandado":
            demandado = p
    
    db.close()
    
    return {
        "expediente": exp,
        "actor": actor,
        "demandado": demandado
    }

def guardar_documento(expediente_id, tipo, contenido):
    db = SessionLocal()
    
    doc = Documento(
        expediente_id=expediente_id,
        tipo=tipo,
        contenido=contenido
    )
    
    db.add(doc)
    db.commit()
    db.close()

def cambiar_estado(expediente_id, nuevo_estado_nombre):
    db = SessionLocal()

    exp = db.query(Expediente).get(expediente_id)

    nuevo_estado = db.query(EstadoProcesal).filter_by(nombre=nuevo_estado_nombre).first()

    exp.estado = nuevo_estado

    db.commit()
    db.close()

def crear_actuacion(expediente_id, tipo, fecha, descripcion):
    db = SessionLocal()

    act = Actuacion(
        tipo=tipo,
        fecha=fecha,
        descripcion=descripcion,
        expediente_id=expediente_id
    )

    db.add(act)

    nuevo_estado_nombre = obtener_nuevo_estado_por_actuacion(tipo)

    if nuevo_estado_nombre:
        exp = db.query(Expediente).get(expediente_id)

        nuevo_estado = db.query(EstadoProcesal)\
            .filter_by(nombre=nuevo_estado_nombre)\
            .first()

        if nuevo_estado:
            exp.estado = nuevo_estado

    db.commit()
    db.close()