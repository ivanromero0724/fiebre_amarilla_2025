import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

# Configurar la página
st.set_page_config(layout="wide", page_title="Mapas de Fiebre Amarilla", page_icon="🦟")

# Título centrado
st.markdown("<h1 style='text-align: center;'>🦟 Mapas de Fiebre Amarilla 2025 🦟</h1>", unsafe_allow_html=True)

# Cargar datos desde GitHub (repositorio público)
url = "https://raw.githubusercontent.com/ivanromero0724/fiebre_amarilla_2025/main/form-1__geocaracterizacion.xlsx"
df = pd.read_excel(url, engine="openpyxl")  # Asegura que pandas pueda leer archivos .xlsx

# Crear mapa centrado en La Guajira
m = folium.Map(location=[11.5449, -72.9066], zoom_start=8)

# Agregar puntos desde el Excel según latitud y longitud
for _, row in df.iterrows():
    folium.CircleMarker(
        location=[row["lat_93_LOCALIZACIN_DE_LA"], row["long_93_LOCALIZACIN_DE_LA"]],
        radius=5,
        color="red" if row["6_VIVIENDA_EFECTIVA_"] == 1 else "blue",
        fill=True,
        fill_color="red" if row["6_VIVIENDA_EFECTIVA_"] == 1 else "blue",
        fill_opacity=0.6,
        popup=f"Vivienda efectiva: {row['6_VIVIENDA_EFECTIVA_']}"
    ).add_to(m)

# Mostrar el mapa en Streamlit
folium_static(m, width=1310, height=600)
