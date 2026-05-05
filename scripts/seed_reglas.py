from app.db.db import SessionLocal
from app.models.regla import ReglaProcesal

def seed():
    db = SessionLocal()

    regla = ReglaProcesal(
        evento="traslado",
        estado_destino="TRASLADO",
        generar_documento=True,
        template="amparo_contestacion.txt",
        crear_plazo=True,
        dias_plazo=5
    )

    db.add(regla)
    db.commit()
    db.close()

    print("✅ Regla creada")

if __name__ == "__main__":
    seed()