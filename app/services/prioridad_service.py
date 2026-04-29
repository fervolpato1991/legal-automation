from datetime import date

def calcular_prioridad(plazo):
    if plazo.cumplido:
        return "ok"

    hoy = date.today()
    dias = (plazo.fecha_vencimiento - hoy).days

    if dias < 0:
        return "critico"
    elif dias <= 2:
        return "urgente"
    elif dias <= 5:
        return "medio"
    else:
        return "bajo"