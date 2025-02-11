import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

# Configurar la página
st.set_page_config(layout="wide", page_title="Mapas de Fiebre Amarilla", page_icon="🦟")

# Título centrado
st.markdown("<h1 style='text-align: center;'>🦟 Mapas de Fiebre Amarilla 2025 🦟</h1>", unsafe_allow_html=True)

# Cargar datos desde GitHub (Asegúrate de que la URL sea correcta y pública)
url = "https://raw.githubusercontent.com/ivanromero0724/fiebre_amarilla_2025/main/form-1__geocaracterizacion.xlsx"

@st.cache_data
def cargar_datos(url):
    try:
        df = pd.read_excel(url, engine="openpyxl")  # Asegura que pandas pueda leer archivos .xlsx
        return df
    except Exception as e:
        st.error(f"Error al cargar los datos: {e}")
        return None

df = cargar_datos(url)

if df is not None:
    # Verificar si las columnas necesarias existen y no tienen valores NaN
    if "lat_93_LOCALIZACIN_DE_LA" in df.columns and "long_93_LOCALIZACIN_DE_LA" in df.columns:
        df = df.dropna(subset=["lat_93_LOCALIZACIN_DE_LA", "long_93_LOCALIZACIN_DE_LA"])

        # Crear mapa centrado en el Tolima
        m = folium.Map(location=[4.5, -75.2], zoom_start=8)

        # Agregar puntos desde el CSV según latitud y longitud
        for _, row in df.iterrows():
            folium.CircleMarker(
                location=[row["lat_93_LOCALIZACIN_DE_LA"], row["long_93_LOCALIZACIN_DE_LA"]],
                radius=5,
                color="red" if row.get("6_VIVIENDA_EFECTIVA_", 0) == 1 else "blue",
                fill=True,
                fill_color="red" if row.get("6_VIVIENDA_EFECTIVA_", 0) == 1 else "blue",
                fill_opacity=0.6,
                popup=f"Vivienda efectiva: {row.get('6_VIVIENDA_EFECTIVA_', 'Desconocido')}"
            ).add_to(m)

        # Mostrar el mapa en Streamlit
        folium_static(m, width=1310, height=600)
    else:
        st.error("Las columnas de latitud y longitud no se encuentran en el archivo.")
else:
    st.error("No se pudo cargar el archivo. Verifica la URL y el formato.")
