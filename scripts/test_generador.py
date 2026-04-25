from app.services.action_executor import generar_documento_desde_plazo

resultado = generar_documento_desde_plazo(plazo_id=1)

print("\n--- DOCUMENTO GENERADO AUTOMÁTICAMENTE ---\n")
print(resultado)