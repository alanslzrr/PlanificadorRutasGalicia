# app.py
import os
import streamlit as st
from journey import Journey
import networkx as nx
from pyvis.network import Network
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Configuración de la página
st.set_page_config(page_title="Planificador de Rutas de Trenes de Galicia", layout="wide")

# Título de la aplicación
st.title("Planificador de Rutas de Trenes de Galicia")
st.subheader("UIE - Base de Datos y Big Data")

# Credenciales de Neo4j desde variables de entorno
uri = os.getenv("NEO4J_URI")
user = os.getenv("NEO4J_USER")
password = os.getenv("NEO4J_PASSWORD")

# Inicializar la clase Journey
neo4j_journey = Journey(uri, user, password)

# Obtener la lista de estaciones
stations = neo4j_journey.get_all_stations()

# Inicializar delays en session_state si no existen
if 'delays' not in st.session_state:
    st.session_state.delays = {}

# Panel lateral para la administración
with st.sidebar:
    st.header("Panel de Administración")
    st.subheader("Simular retrasos en las estaciones")
    delayed_stations = st.multiselect("Selecciona estaciones con retraso", stations)

    # Actualizar delays en session_state
    for station in delayed_stations:
        if station not in st.session_state.delays:
            st.session_state.delays[station] = 5  # Valor predeterminado

    # Eliminar estaciones que ya no están seleccionadas
    for station in list(st.session_state.delays.keys()):
        if station not in delayed_stations:
            del st.session_state.delays[station]

    # Sliders para cada estación retrasada
    delays = {}
    for station in delayed_stations:
        delays[station] = st.slider(
            f"Retraso en {station} (minutos)",
            min_value=0,
            max_value=60,
            value=st.session_state.delays.get(station, 5),
            step=5,
            key=f"delay_{station}"
        )
        st.session_state.delays[station] = delays[station]

# Selección de estación de inicio y fin
start_station = st.selectbox("Estación de inicio", stations)
end_station = st.selectbox("Estación de destino", stations)

# Botón para calcular la ruta
if st.button("Calcular Ruta Más Corta"):
    if start_station == end_station:
        st.warning("Por favor, selecciona estaciones diferentes.")
    else:
        # Obtener los datos del grafo
        edges = neo4j_journey.get_graph()

        # Construir el grafo original (sin retrasos)
        G_original = nx.DiGraph()
        for f, t, time in edges:
            G_original.add_edge(f, t, weight=time, original_time=time, delay=0)

        # Construir el grafo ajustado (con retrasos)
        G_adjusted = nx.DiGraph()
        for f, t, time in edges:
            delay = st.session_state.delays.get(f, 0)
            effective_time = time + delay
            G_adjusted.add_edge(f, t, weight=effective_time, original_time=time, delay=delay)

        # Calcular la ruta original sin retrasos
        try:
            path_original = nx.dijkstra_path(G_original, start_station, end_station, weight='weight')
            total_time_original = nx.dijkstra_path_length(G_original, start_station, end_station, weight='weight')
        except nx.NetworkXNoPath:
            path_original = None
            total_time_original = None

        # Calcular la ruta ajustada considerando retrasos
        try:
            path_adjusted = nx.dijkstra_path(G_adjusted, start_station, end_station, weight='weight')
            total_time_adjusted = nx.dijkstra_path_length(G_adjusted, start_station, end_station, weight='weight')
        except nx.NetworkXNoPath:
            path_adjusted = None
            total_time_adjusted = None

        if path_adjusted:
            # Identificar estaciones con retraso en la ruta original
            delayed_in_original = set(path_original).intersection(delayed_stations) if path_original else set()
            # Identificar estaciones con retraso en la ruta ajustada
            delayed_in_adjusted = set(path_adjusted).intersection(delayed_stations)
            # Determinar si se ha evitado alguna estación con retraso
            avoided_delays = delayed_in_original - delayed_in_adjusted

            if avoided_delays:
                avoided_stations_str = ", ".join([s for s in avoided_delays])
                st.warning(
                    f"Tu ruta más corta desde **{start_station}** hacia **{end_station}** se veía afectada por **{avoided_stations_str}**. "
                    "Se ha modificado la ruta para evitar mayores retrasos."
                )

            # Mostrar el tiempo total de viaje
            st.success(f"Tiempo total de viaje: {total_time_adjusted} minutos")
            # Mostrar la ruta ajustada
            st.write("Ruta:")
            for s in path_adjusted:
                d = st.session_state.delays.get(s, 0)
                if d > 0:
                    st.write(f"- {s} (Retraso de {d} minutos)")
                else:
                    st.write(f"- {s}")

            # Visualización del grafo
            st.subheader("Visualización de la Ruta")
            path_edges = list(zip(path_adjusted[:-1], path_adjusted[1:]))

            # Configuración de PyVis
            net = Network(height="600px", width="100%", directed=True)
            net.toggle_physics(True)
            net.set_options("""
                var options = {
                  "nodes": {
                    "font": {"size": 14},
                    "scaling": {"min": 15, "max": 30},
                    "color": {
                      "border": "#2B7CE9",
                      "background": "#97C2FC",
                      "highlight": {
                        "border": "#2B7CE9",
                        "background": "#D2E5FF"
                      }
                    }
                  },
                  "edges": {
                    "color": {
                      "color": "#2B7CE9",
                      "highlight": "#D2E5FF",
                      "inherit": false
                    },
                    "arrows": {"to": {"enabled": true, "scaleFactor":1.2}},
                    "smooth": {
                      "enabled": true,
                      "type": "dynamic"
                    }
                  },
                  "interaction": {
                    "hover": true,
                    "zoomView": true,
                    "dragView": true,
                    "navigationButtons": true,
                    "keyboard": true
                  },
                  "physics": {
                    "enabled": true,
                    "stabilization": {"iterations": 200}
                  }
                }
            """)

            # Definir colores en una paleta de azules
            def get_node_color(node):
                if node == start_station:
                    return "#003f5c"  # Azul marino oscuro
                elif node == end_station:
                    return "#2f4b7c"  # Azul intermedio oscuro
                elif node in delayed_stations:
                    return "#1f77b4"  # Azul estándar para retrasos
                elif node in path_adjusted:
                    return "#aec7e8"  # Azul claro para nodos en la ruta
                else:
                    return "#c7c7c7"  # Celeste para nodos generales

            def get_edge_color(edge):
                if (edge[0], edge[1]) in path_edges:
                    return "#003f5c"  # Azul marino para la ruta seleccionada
                elif edge[2]['delay'] > 0:
                    return "#1f77b4"  # Azul estándar para aristas con retraso
                else:
                    return "#7f7f7f"  # Gris para aristas normales

            # Añadir nodos al grafo
            for node in G_adjusted.nodes:
                node_color = get_node_color(node)
                title_info = f"<b>{node}</b>"
                if node in delayed_stations:
                    title_info += f"<br>Retraso: {st.session_state.delays[node]} minutos"
                if node in path_adjusted:
                    title_info += "<br>Parte de la ruta seleccionada"
                if node == start_station:
                    title_info += "<br>Estación de inicio"
                if node == end_station:
                    title_info += "<br>Estación de destino"

                net.add_node(
                    node,
                    label=node,
                    color=node_color,
                    title=title_info
                )

            # Añadir aristas al grafo
            for edge in G_adjusted.edges(data=True):
                edge_color = get_edge_color(edge)
                edge_width = 2 if (edge[0], edge[1]) in path_edges else 1
                base_title = f"Tiempo original: {edge[2]['original_time']} min"
                if edge[2]['delay'] > 0:
                    base_title += f"<br>Retraso: +{edge[2]['delay']} min"
                if (edge[0], edge[1]) in path_edges:
                    base_title += "<br>Parte de la ruta seleccionada"

                net.add_edge(
                    edge[0],
                    edge[1],
                    title=base_title,
                    color=edge_color,
                    width=edge_width
                )

            # Generar y mostrar el grafo
            net.save_graph("graph.html")
            with open("graph.html", "r", encoding="utf-8") as f:
                html_content = f.read()
            st.components.v1.html(html_content, height=600)

        else:
            st.error("No hay ruta disponible entre las estaciones seleccionadas.")

# Cerrar la conexión al finalizar
neo4j_journey.close()
