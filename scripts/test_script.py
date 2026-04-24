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
    caratula="Perez c/ PAMI s/ Amparo",
    jurisdiccion="Federal",
    tipo_proceso="Amparo"
)

agregar_parte(exp.id, "Perez", "actor", domicilio="Calle Falsa 123")
agregar_parte(exp.id, "PAMI", "demandado", domicilio="Avenida Siempre Viva 456")

resultado = procesar_actuacion(
    expediente_id=exp.id,
    tipo="Demanda",
    descripcion="Se presenta demanda",
    contexto_extra={
        "objeto": "la cobertura integral de prestación médica",
        "hechos": "El actor padece una patología..."
    }
)

resultado_traslado = procesar_actuacion(
    expediente_id=exp.id,
    tipo="Traslado",
    descripcion="Se corre traslado por 5 días"
)

print("\n--- DOCUMENTO GENERADO ---\n")
print(resultado)

print("\n--- TRASLADO ---\n")
print(resultado_traslado)