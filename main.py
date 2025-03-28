import tkinter as tk
from tkinter import messagebox, ttk
import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
import tkintermapview
from geopy.geocoders import Nominatim

# Variables globales para coordenadas
coordenadas_seleccionadas = {}

def seleccionar_en_mapa():
    ventana_mapa = tk.Tk()
    ventana_mapa.title("Seleccionar Punto de Origen")
    ventana_mapa.geometry("800x750")

    mapa = tkintermapview.TkinterMapView(
        ventana_mapa, width=800, height=500, corner_radius=0)
    mapa.pack(pady=10)

    # Centrar mapa en ubicación inicial
    mapa.set_position(4.6209565, -74.0749507)
    mapa.set_zoom(15)

    punto_origen = None
    marcador_origen = None

    # Marcar destino fijo (Av.68 UCompensar)
    mapa.set_marker(4.6758718, -74.0900838, text="Destino",
                    marker_color_circle="red", marker_color_outside="red")

    leyenda = tk.Label(
        ventana_mapa,
        text=(
            "🟢 Clic izquierdo para seleccionar o mover el punto de Origen\n"
            "🔴 Punto de destino fijo: Sede Av. 68 UCompensar"
        ),
        font=("Arial", 10, "bold"),
    )
    leyenda.pack(pady=5)

    direccion_label = tk.Label(ventana_mapa, text="Dirección: ", wraplength=750, justify="left")
    direccion_label.pack(pady=5)

    def manejar_click_mapa(coords):
        # coords es una tupla (lat, lon) que pasa tkintermapview
        nonlocal punto_origen, marcador_origen
        lat, lon = coords
        punto_origen = (lat, lon)

        # Si ya había un marcador de origen, se borra
        if marcador_origen:
            marcador_origen.delete()

        # Crear marcador verde para el origen
        marcador_origen = mapa.set_marker(
            lat, lon, text="Origen",
            marker_color_circle="green", marker_color_outside="green"
        )
        # Habilitar botón de guardar
        boton_guardar.config(state="normal")

        # Mostrar dirección con geopy (opcional)
        try:
            geolocator = Nominatim(user_agent="ruta_mas_corta_app")
            location = geolocator.reverse((lat, lon), language='es')
            if location and location.address:
                direccion_label.config(text=f"Dirección: {location.address}")
            else:
                direccion_label.config(text="Dirección: No encontrada")
        except Exception as e:
            direccion_label.config(text=f"Error obteniendo dirección: {e}")

    def guardar_coordenadas():
        """Asigna el punto de origen y el destino fijo, cierra el mapa y abre la ventana principal."""
        nonlocal punto_origen
        if punto_origen:
            coordenadas_seleccionadas['lat_origen'], coordenadas_seleccionadas['lon_origen'] = punto_origen
            # Destino fijo
            coordenadas_seleccionadas['lat_destino'] = 4.6758718
            coordenadas_seleccionadas['lon_destino'] = -74.0900838

            # Evitar error invalid command name update_canvas_tile_images
            mapa.cancel_current_tile_downloads()

            ventana_mapa.destroy()
            iniciar_ventana_principal()
        else:
            messagebox.showwarning("Ubicación requerida", "Seleccione el punto de origen haciendo clic sobre el mapa.")

    # Cuando haces clic en el mapa, se ejecuta manejar_click_mapa
    mapa.add_left_click_map_command(manejar_click_mapa)

    boton_guardar = tk.Button(
        ventana_mapa,
        text="Aceptar Coordenadas",
        state="disabled",
        command=guardar_coordenadas
    )
    boton_guardar.pack(pady=10)

    ventana_mapa.mainloop()

def iniciar_ventana_principal():
    """Crea la interfaz para ingresar/editar las coordenadas y calcular la ruta."""
    global entry_lat_origen, entry_lon_origen
    global entry_lat_destino, entry_lon_destino

    root = tk.Tk()
    root.title("Calculadora de Ruta Más Corta - Bogotá")

    # Entradas para coordenadas
    tk.Label(root, text="Latitud Origen:").grid(row=0, column=0, padx=10, pady=5)
    entry_lat_origen = tk.Entry(root)
    entry_lat_origen.grid(row=0, column=1, padx=10, pady=5)
    entry_lat_origen.insert(0, coordenadas_seleccionadas.get('lat_origen', ''))

    tk.Label(root, text="Longitud Origen:").grid(row=1, column=0, padx=10, pady=5)
    entry_lon_origen = tk.Entry(root)
    entry_lon_origen.grid(row=1, column=1, padx=10, pady=5)
    entry_lon_origen.insert(0, coordenadas_seleccionadas.get('lon_origen', ''))

    tk.Label(root, text="Latitud Destino:").grid(row=2, column=0, padx=10, pady=5)
    entry_lat_destino = tk.Entry(root)
    entry_lat_destino.grid(row=2, column=1, padx=10, pady=5)
    entry_lat_destino.insert(0, coordenadas_seleccionadas.get('lat_destino', ''))

    tk.Label(root, text="Longitud Destino:").grid(row=3, column=0, padx=10, pady=5)
    entry_lon_destino = tk.Entry(root)
    entry_lon_destino.grid(row=3, column=1, padx=10, pady=5)
    entry_lon_destino.insert(0, coordenadas_seleccionadas.get('lon_destino', ''))

    # Algoritmo
    tk.Label(root, text="Seleccionar Algoritmo:").grid(row=4, column=0, padx=10, pady=5)
    algoritmo_var = tk.StringVar(value="Dijkstra")
    ttk.Combobox(root, textvariable=algoritmo_var, values=["Dijkstra", "Bellman-Ford"], state="readonly").grid(
        row=4, column=1, padx=10, pady=5
    )

    # Color
    tk.Label(root, text="Color de la Ruta:").grid(row=5, column=0, padx=10, pady=5)
    color_var = tk.StringVar(value="red")
    ttk.Combobox(root, textvariable=color_var, values=["red", "blue", "green", "purple", "orange", "pink"], state="readonly").grid(
        row=5, column=1, padx=10, pady=5
    )

    # Botón para calcular ruta
    tk.Button(
        root, text="Calcular Ruta",
        command=lambda: calcular_ruta(algoritmo_var, color_var)
    ).grid(row=6, column=0, columnspan=2, pady=10)

    # Información
    tk.Label(
        root,
        text=(
            "Desarrollado por Pedro J. Villanueva H. y Johan E. Zubieta M.\n"
            "Presentado a Luis Eduardo Ibanez Forero\n"
            "Modelamiento y Optimizacion\n"
            "Fundacion Universitaria Compensar"
        ),
        font=("TkDefaultFont", 9),
        justify="center"
    ).grid(row=7, column=0, columnspan=2, padx=10, pady=5)

    root.mainloop()

def obtener_coordenadas():
    """Convierte lo ingresado en los campos de texto a float."""
    try:
        return {
            'lat_origen': float(entry_lat_origen.get()),
            'lon_origen': float(entry_lon_origen.get()),
            'lat_destino': float(entry_lat_destino.get()),
            'lon_destino': float(entry_lon_destino.get())
        }
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingrese coordenadas válidas.")
        return None

def calcular_ruta(algoritmo_var, color_var):
    """Calcula y visualiza la ruta más corta según el algoritmo y color elegidos."""
    try:
        # Lee coordenadas
        datos = obtener_coordenadas()
        if not datos:
            return

        lat_origen = datos['lat_origen']
        lon_origen = datos['lon_origen']
        lat_destino = datos['lat_destino']
        lon_destino = datos['lon_destino']

        # Algoritmo y color
        algoritmo = algoritmo_var.get()
        color_ruta = color_var.get()

        if not algoritmo:
            messagebox.showwarning("Advertencia", "Selecciona un algoritmo para calcular la ruta.")
            return

        # Descargar y proyectar el grafo
        G = ox.graph_from_place("Bogotá, Colombia", network_type="drive")
        G = ox.project_graph(G)

        nodo_origen = ox.distance.nearest_nodes(G, lon_origen, lat_origen)
        nodo_destino = ox.distance.nearest_nodes(G, lon_destino, lat_destino)

        metodos = {
            "Dijkstra": "dijkstra",
            "Bellman-Ford": "bellman-ford"
        }
        if algoritmo not in metodos:
            messagebox.showwarning("Advertencia", "Algoritmo no válido.")
            return

        ruta = nx.shortest_path(G, nodo_origen, nodo_destino, weight="length", method=metodos[algoritmo])

        # Calcula distancia
        distancia_total = sum(nx.shortest_path_length(G, u, v, weight="length") for u, v in zip(ruta[:-1], ruta[1:]))

        # Visualiza
        fig, ax = plt.subplots(figsize=(10, 8))
        ox.plot_graph(G, ax=ax, node_size=0, edge_color="gray", edge_linewidth=0.5, show=False)
        ox.plot_graph_route(G, ruta, route_linewidth=3, node_size=0, route_color=color_ruta, ax=ax, show=True)

        messagebox.showinfo("Ruta Calculada", f"Algoritmo: {algoritmo}\nDistancia total: {distancia_total / 1000:.2f} km")

    except ValueError:
        messagebox.showerror("Error", "Por favor, ingrese coordenadas válidas.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un problema: {e}")

def obtener_ruta(grafo, origen, destino, algoritmo):
    metodos = {
        "Dijkstra": "dijkstra",
        "Bellman-Ford": "bellman-ford"
    }
    metodo = metodos.get(algoritmo)
    if not metodo:
        messagebox.showwarning("Advertencia", "Algoritmo no válido.")
        return None

    return nx.shortest_path(grafo, origen, destino, weight="length", method=metodo)


def calcular_distancia(grafo, ruta):
    return sum(nx.shortest_path_length(grafo, u, v, weight="length") for u, v in zip(ruta[:-1], ruta[1:])) / 1000


def visualizar_ruta(grafo, ruta, distancia_km, algoritmo, color):
    fig, ax = plt.subplots(figsize=(10, 8))
    ox.plot_graph(grafo, ax=ax, node_size=0, edge_color="gray",
                  edge_linewidth=0.5, show=False)
    ox.plot_graph_route(grafo, ruta, route_linewidth=3,
                        node_size=0, route_color=color, ax=ax, show=True)
    messagebox.showinfo(
        "Ruta Calculada", f"Algoritmo: {algoritmo}\nDistancia total: {distancia_km:.2f} km")


# Inicia la app con el mapa
seleccionar_en_mapa()
