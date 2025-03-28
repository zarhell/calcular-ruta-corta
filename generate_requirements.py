import os

print("🔄 Generando requirements.txt con codificación UTF-8...")

exit_code = os.system("pipreqs ./ --force --encoding=utf-8")
if exit_code == 0:
    print("✅ Archivo requirements.txt generado correctamente.")
else:
    print("❌ Error generando requirements.txt. Verifica posibles errores de codificación o módulos inválidos.")
