@echo off
setlocal

echo 📦 Creando entorno virtual si no existe...
if not exist .venv (
    python -m venv .venv
)

echo ✅ Activando entorno virtual...
call .venv\Scripts\activate.bat

echo 📚 Actualizando pip, setuptools y wheel...
python -m pip install --upgrade pip setuptools wheel

echo 🔧 Instalando módulos requeridos por main.py...
python -m pip install osmnx networkx matplotlib tkintermapview geopy

echo 🚀 Ejecutando la aplicación...
python main.py

endlocal
pause
