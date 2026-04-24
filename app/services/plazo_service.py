from datetime import timedelta

def sumar_dias_habiles(fecha_inicio, dias):
    fecha = fecha_inicio
    dias_sumados = 0

    while dias_sumados < dias:
        fecha += timedelta(days=1)

        if fecha.weekday() < 5:  # 0-4 = lunes a viernes
            dias_sumados += 1

    return fecha