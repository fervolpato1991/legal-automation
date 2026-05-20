from app.db.db import SessionLocal
from app.models.estado import EstadoProcesal


def seed():

    db = SessionLocal()

    estados = [
        "INICIO",
        "TRASLADO",
        "CONTESTACION",
        "PRUEBA",
        "SENTENCIA"
    ]

    for nombre in estados:

        existente = db.query(EstadoProcesal).filter_by(
            nombre=nombre
        ).first()

        if not existente:

            estado = EstadoProcesal(
                nombre=nombre
            )

            db.add(estado)

    db.commit()
    db.close()

    print("✅ Estados creados")


if __name__ == "__main__":
    seed()