import streamlit as st
import folium
from streamlit_folium import folium_static

# Configurar la página para que use todo el ancho disponible
st.set_page_config(layout="wide", page_title="Mapas de Fiebre Amarilla", page_icon="🦟")

# Título de la aplicación
st.markdown("<h1 style='text-align: center;'>🦟 Mapas de Fiebre Amarilla 2025 🦟</h1>", unsafe_allow_html=True)

# Crear un mapa con Folium
m = folium.Map(location=[11.5449, -72.9066], zoom_start=8)

# Agregar un marcador de ejemplo
folium.Marker(
    [11.5449, -72.9066],
    popup="Ejemplo de ubicación en La Guajira",
    icon=folium.Icon(color="blue"),
).add_to(m)

# Mostrar el mapa con un tamaño más grande
folium_static(m, width=1310, height=600)
