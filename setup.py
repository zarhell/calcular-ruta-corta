import os
import subprocess
import sys
import platform

VENV_DIR = ".venv"
IS_WINDOWS = platform.system() == "Windows"
PYTHON_BIN = os.path.join(VENV_DIR, "Scripts" if IS_WINDOWS else "bin", "python")

def crear_entorno_virtual():
    if not os.path.exists(VENV_DIR):
        print("📦 Creando entorno virtual...")
        subprocess.check_call([sys.executable, "-m", "venv", VENV_DIR])
    else:
        print("✅ Entorno virtual ya existe.")

def instalar_dependencias():
    print("📚 Instalando dependencias...")

    # Actualiza pip, setuptools y wheel
    subprocess.check_call([PYTHON_BIN, "-m", "pip", "install", "--upgrade", "pip", "setuptools", "wheel"])

    # Cython es necesario para jnius (solo si está en requirements.txt)
    if "jnius" in open("requirements.txt", encoding="utf-8").read():
        print("🔧 Instalando Cython (dependencia para jnius)...")
        subprocess.check_call([PYTHON_BIN, "-m", "pip", "install", "Cython"])

    try:
        subprocess.check_call([PYTHON_BIN, "-m", "pip", "install", "-r", "requirements.txt"])
    except subprocess.CalledProcessError as e:
        print("❌ Error al instalar dependencias.")
        print("💡 Verifica si hay paquetes incompatibles en requirements.txt.")
        raise e

def ejecutar_app():
    print("🚀 Ejecutando la aplicación...")
    subprocess.run([PYTHON_BIN, "main.py"])

if __name__ == "__main__":
    crear_entorno_virtual()
    instalar_dependencias()
    ejecutar_app()
