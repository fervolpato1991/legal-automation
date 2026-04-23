def obtener_nuevo_estado_por_actuacion(tipo_actuacion):

    reglas = {
        "Demanda": "DEMANDA_PRESENTADA",
        "Traslado": "TRASLADO",
        "Contestacion": "CONTESTACION",
        "Apertura a prueba": "PRUEBA",
        "Sentencia": "SENTENCIA"
    }

    return reglas.get(tipo_actuacion)