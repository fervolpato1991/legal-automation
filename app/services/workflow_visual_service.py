from app.models.evento import EventoSistema


def generar_mermaid_expediente(db, expediente_id):

    eventos = db.query(EventoSistema)\
        .filter_by(expediente_id=expediente_id)\
        .order_by(EventoSistema.fecha.asc())\
        .all()

    lines = [
        "graph TD",
        "classDef evento fill:#e8f0fe,stroke:#1a73e8,stroke-width:2px;"
    ]

    previous = None

    for evento in eventos:

        node_id = f"E{evento.id}"

        label = f"{evento.tipo}"

        if evento.descripcion:
            label += f": {evento.descripcion}"

        label = label.replace('"', "'")

        lines.append(
            f'{node_id}["{label}"]:::evento'
        )

        if previous:
            lines.append(
                f"{previous} --> {node_id}"
            )

        previous = node_id

    return "\n".join(lines)