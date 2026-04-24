def obtener_nuevo_estado_por_actuacion(tipo_actuacion):

    reglas = {
        "Demanda": "DEMANDA_PRESENTADA",
        "Traslado": "TRASLADO",
        "Contestacion": "CONTESTACION",
        "Apertura a prueba": "PRUEBA",
        "Sentencia": "SENTENCIA"
    }

    return reglas.get(tipo_actuacion)

def obtener_plazo_por_actuacion(tipo_actuacion):

    reglas_plazos = {
        "Traslado": 5,
        "Contestacion": 5,
        "Apelacion": 3
    }

    return reglas_plazos.get(tipo_actuacion)