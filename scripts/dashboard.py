from app.services.alert_service import obtener_dashboard_plazos

data = obtener_dashboard_plazos()

print("\n🔴 VENCIDOS\n")
for p in data["vencidos"]:
    print(f"{p.expediente.caratula} | {p.tipo} | {p.fecha_vencimiento}")

print("\n🟠 PRÓXIMOS (≤3 días)\n")
for p in data["proximos"]:
    print(f"{p.expediente.caratula} | {p.tipo} | {p.fecha_vencimiento}")

print("\n🟢 FUTUROS\n")
for p in data["futuros"]:
    print(f"{p.expediente.caratula} | {p.tipo} | {p.fecha_vencimiento}")