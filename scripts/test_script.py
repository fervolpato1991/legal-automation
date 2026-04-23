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

# =========================
# 1. CREAR DATOS (setup)
# =========================

exp = crear_expediente(
    caratula="Perez c/ PAMI s/ Amparo",
    jurisdiccion="Federal",
    tipo_proceso="Amparo"
)

agregar_parte(exp.id, "Perez", "actor", domicilio="Calle Falsa 123")
agregar_parte(exp.id, "PAMI", "demandado", domicilio="Avenida Siempre Viva 456")

db = SessionLocal()

act = Actuacion(
    tipo="Demanda",
    fecha=date.today(),
    descripcion="Se presenta demanda",
    expediente_id=exp.id
)

db.add(act)
db.commit()
db.close()

# =========================
# 2. OBTENER EXPEDIENTE REAL
# =========================

data = obtener_expediente_completo(1)
expediente = data["expediente"]

# =========================
# 3. DEFINIR TIPO DOCUMENTO
# =========================

tipo_documento = "demanda"

# =========================
# 4. SELECCIÓN AUTOMÁTICA TEMPLATE
# =========================

template_name = seleccionar_template_por_estado(expediente)

# =========================
# 5. ARMAR CONTEXTO
# =========================

contexto = {
    "actor": data["actor"],
    "demandado": data["demandado"],
    "objeto": "la cobertura integral de prestación médica",
    "hechos": "El actor padece una patología que requiere tratamiento urgente..."
}

# =========================
# 6. GENERAR DOCUMENTO
# =========================

resultado = render_template(template_name, contexto)

print("\n--- DOCUMENTO GENERADO ---\n")
print(resultado)

# =========================
# 7. GUARDAR DOCUMENTO
# =========================

guardar_documento(expediente.id, tipo_documento, resultado)