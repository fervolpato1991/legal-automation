from datetime import date


def calcular_prioridad(expediente):

    score = 0
    motivos = []

    plazos_pendientes = [
        p for p in expediente.plazos
        if not p.cumplido
    ]

    # =====================
    # PLAZOS
    # =====================

    for plazo in plazos_pendientes:

        dias = (plazo.fecha_vencimiento - date.today()).days

        if dias < 0:
            score += 100
            motivos.append("Plazo vencido")

        elif dias <= 1:
            score += 80
            motivos.append("Vence en 24h")

        elif dias <= 3:
            score += 50
            motivos.append("Vence pronto")

    # =====================
    # CANTIDAD DE PLAZOS
    # =====================

    if len(plazos_pendientes) >= 3:
        score += 20
        motivos.append("Muchos plazos activos")

    # =====================
    # DOCUMENTOS
    # =====================

    if len(expediente.documentos) == 0:
        score += 10
        motivos.append("Sin documentos")

    # =====================
    # ESTADO
    # =====================

    if expediente.estado:

        nombre = expediente.estado.nombre.lower()

        if "urgente" in nombre:
            score += 50
            motivos.append("Estado urgente")

    # =====================
    # NIVEL
    # =====================

    if score >= 100:
        nivel = "CRITICA"

    elif score >= 70:
        nivel = "ALTA"

    elif score >= 40:
        nivel = "MEDIA"

    else:
        nivel = "BAJA"

    return {
        "score": score,
        "nivel": nivel,
        "motivos": motivos
    }