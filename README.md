
# 🗺️ Calculadora de Ruta Más Corta - Bogotá

Este proyecto es una aplicación de escritorio interactiva creada con **Python**, que permite calcular la ruta más corta desde un punto de origen seleccionado en el mapa hasta la sede Av. 68 de la Fundación Universitaria Compensar en Bogotá. Utiliza algoritmos clásicos como **Dijkstra** y **Bellman-Ford**, y se apoya en bibliotecas como `osmnx`, `networkx` y `tkintermapview`.

---

## ⚙️ Requisitos

- Python **3.10 o superior**
- Sistemas compatibles: **Windows / Linux / macOS / WSL**
- Conexión a internet (para descargar dependencias y datos de OpenStreetMap)

---

## 📦 Instalación y ejecución

Sigue estos pasos para ejecutar la aplicación:

### 1. Clona el repositorio

```bash
https://github.com/zarhell/calcular-ruta-corta.git
cd calcular-ruta-corta
```

### 2. Ejecuta el script de configuración

Este script realiza lo siguiente automáticamente:

- Crea un entorno virtual `.venv` si no existe.
- Activa el entorno virtual.
- Actualiza `pip`, `setuptools` y `wheel`.
- Instala **Cython** si es necesario (por ejemplo, si usas `jnius`).
- Instala las dependencias del archivo `requirements.txt`.
- Ejecuta la aplicación principal `main.py`.

```bash
./setup.sh
```

---

## 🖥️ Uso de la aplicación

1. Al ejecutar el script, se abrirá una ventana con un mapa.
2. Selecciona el **punto de origen** haciendo clic izquierdo sobre el mapa.
3. El **punto de destino** es fijo (Sede Av. 68).
4. Haz clic en **Aceptar Coordenadas** para abrir la ventana principal.
5. Elige el **algoritmo** y el **color** de la ruta.
6. Haz clic en **Calcular Ruta** para visualizar el recorrido en el mapa.

---

## 🧪 ¿Problemas comunes?

- Si aparece el error: `ModuleNotFoundError: No module named 'osmnx'`, asegúrate de estar usando el entorno virtual correcto (`source .venv/bin/activate`).
- Para sistemas Windows, se recomienda usar **WSL** o crear un script equivalente en `.bat`.

---

## 🧠 Créditos

Desarrollado por:

- Pedro J. Villanueva H.
- Johan E. Zubieta M.

Presentado a: **Luis Eduardo Ibáñez Forero**  
Curso: Modelamiento y Optimización  
**Fundación Universitaria Compensar**
```