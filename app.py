import streamlit as st
import folium
from streamlit_folium import folium_static

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

# Mostrar el mapa con un tamaño más grande
folium_static(m, width=2000, height=600)
