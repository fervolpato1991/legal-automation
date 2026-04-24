from app.services.alert_service import obtener_plazos_proximos
from datetime import date

plazos = obtener_plazos_proximos(dias=3)
hoy = date.today()

print("\n--- ALERTAS DE VENCIMIENTOS ---\n")

print(f"Cantidad de plazos encontrados: {len(plazos)}")

for p in plazos:
    if p.fecha_vencimiento < hoy:
        estado = "🔴 VENCIDO"
    elif p.fecha_vencimiento == hoy:
        estado = "🟡 VENCE HOY"
    else:
        estado = "🟢 PRÓXIMO"

    print(f"[{estado}] Expediente ID: {p.expediente_id}")
    print(f"Tipo: {p.tipo}")
    print(f"Vence: {p.fecha_vencimiento}")
    print("-" * 30)