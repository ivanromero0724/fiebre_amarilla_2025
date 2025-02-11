import streamlit as st
import folium
from streamlit_folium import folium_static

# Configurar la página para que use todo el ancho disponible
st.set_page_config(layout="wide")

# Aplicar estilos CSS para fondo blanco, texto negro y centrar el contenido
st.markdown(
    """
    <style>
        /* Fondo blanco */
        .stApp {
            background-color: white;
        }
        /* Color negro para título y texto */
        h1, h2, h3, h4, h5, h6, p, span, div {
            color: black !important;
        }
        /* Centrar el mapa */
        .map-container {
            display: flex;
            justify-content: center;
            align-items: center;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Título de la aplicación
st.title("Mapa Interactivo con Streamlit")

# Instrucciones
st.write("Este es un mapa interactivo de ejemplo con Streamlit y Folium.")

# Crear un mapa con Folium
m = folium.Map(location=[11.5449, -72.9066], zoom_start=8)

# Agregar un marcador de ejemplo
folium.Marker(
    [11.5449, -72.9066],
    popup="Ejemplo de ubicación en La Guajira",
    icon=folium.Icon(color="blue"),
).add_to(m)

# Centrar el mapa usando un contenedor
st.markdown('<div class="map-container">', unsafe_allow_html=True)
folium_static(m, width=900, height=600)
st.markdown('</div>', unsafe_allow_html=True)
