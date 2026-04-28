from app.crud.crud import (
    crear_expediente,
    agregar_parte,
    listar_expedientes,
    obtener_expediente_completo,
    guardar_documento
)
from app.db.db import SessionLocal
from app.models import Actuacion
from datetime import date

from app.services.template_engine import render_template
from app.services.template_selector import seleccionar_template_por_estado
from app.services.workflow_service import procesar_actuacion


exp = crear_expediente(
    caratula="Norberto c/ LPM s/ Daños y perjuicios",
    jurisdiccion="Provincial",
    tipo_proceso="Daños y perjuicios",
)

agregar_parte(exp.id, "Norberto", "actor", domicilio="Calle Olazabal 4523")
agregar_parte(exp.id, "LPM", "demandado", domicilio="Avenida Epic 6656")

resultado = procesar_actuacion(
    expediente_id=exp.id,
    tipo="Demanda",
    descripcion="Se presenta demanda",
    contexto_extra={
        "objeto": "la cobertura integral de prestación bancaria",
        "hechos": "El actor padece deudas..."
    }
)

resultado_traslado = procesar_actuacion(
    expediente_id=exp.id,
    tipo="Traslado",
    descripcion="Se corre traslado por 55 días"
)

print("\n--- DOCUMENTO GENERADO ---\n")
print(resultado)

print("\n--- TRASLADO ---\n")
print(resultado_traslado)