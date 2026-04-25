from app.services.alert_service import obtener_dashboard_plazos
from app.services.action_rules import sugerir_accion

data = obtener_dashboard_plazos()

def mostrar_seccion(titulo, plazos):
    print(f"\n{titulo}\n")

    for p in plazos:
        sugerencia = sugerir_accion(p)

        print(f"{p.expediente.caratula}")
        print(f"Tipo: {p.tipo}")
        print(f"Vence: {p.fecha_vencimiento}")

        if sugerencia:
            print(f"👉 Acción: {sugerencia['accion']}")
            print(f"📄 Documento sugerido: {sugerencia['documento']}")

        print("-" * 40)


mostrar_seccion("🔴 VENCIDOS", data["vencidos"])
mostrar_seccion("🟠 PRÓXIMOS (≤3 días)", data["proximos"])
mostrar_seccion("🟢 FUTUROS", data["futuros"])