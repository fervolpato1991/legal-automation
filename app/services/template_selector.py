def seleccionar_template_por_estado(expediente):

    estado = expediente.estado.nombre

    if expediente.tipo_proceso == "Amparo":

        if estado == "INICIO":
            return "amparo_demanda.txt"

        elif estado == "TRASLADO":
            return "amparo_contestacion.txt"

        elif estado == "PRUEBA":
            return "amparo_oficio.txt"

    return None

def seleccionar_template_por_estado(expediente):
    if expediente.estado is None:
        raise Exception(f"Expediente {expediente.id} sin estado")

    estado = expediente.estado.nombre

    if estado == "INICIO":
        return "amparo_demanda.txt"

    return "default.txt"