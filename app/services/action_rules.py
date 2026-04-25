def sugerir_accion(plazo):

    reglas = {
        "Traslado": {
            "accion": "Preparar contestación de demanda",
            "documento": "amparo_constestacion.txt"
        },
        "Contestacion": {
            "accion": "Revisar contestación presentada",
            "documento": None
        },
        "Apelacion": {
            "accion": "Fundar recurso",
            "documento": "recurso_apelacion.txt"
        }
    }

    return reglas.get(plazo.tipo, {
        "accion": "Sin acción definida",
        "documento": None
    })