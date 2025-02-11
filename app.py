import streamlit as st
import folium
import pandas as pd
from streamlit_folium import folium_static

# Configurar la página para que use todo el ancho disponible
st.set_page_config(layout="wide", page_title="Mapas de Fiebre Amarilla", page_icon="🦟")

# Título de la aplicación
st.markdown("<h1 style='text-align: center;'>🦟 Mapas de Fiebre Amarilla 2025 🦟</h1>", unsafe_allow_html=True)

# Cargar datos desde GitHub
@st.cache_data
def cargar_datos():
    url = "https://raw.githubusercontent.com/tu_usuario/tu_repositorio/main/form-1__geocaracterizacion.csv"
    df = pd.read_csv(url, sep=",")  # Asegúrate de que el separador es correcto
    return df

df = cargar_datos()

# Verificar si las columnas necesarias existen
if "lat_93_LOCALIZACIN_DE_LA" in df.columns and "long_93_LOCALIZACIN_DE_LA" in df.columns:
    
    # Crear un mapa con Folium
    m = folium.Map(location=[df["lat_93_LOCALIZACIN_DE_LA"].mean(), df["long_93_LOCALIZACIN_DE_LA"].mean()], zoom_start=8)

    # Agregar puntos al mapa
    for _, row in df.iterrows():
        folium.Marker(
            [row["lat_93_LOCALIZACIN_DE_LA"], row["long_93_LOCALIZACIN_DE_LA"]],
            popup=f"Vivienda Efectiva: {row['6_VIVIENDA_EFECTIVA_']}",
            icon=folium.Icon(color="blue"),
        ).add_to(m)

    # Mostrar el mapa en Streamlit
    folium_static(m, width=1310, height=600)

else:
    st.error("⚠️ No se encontraron las columnas de latitud y longitud en el archivo CSV.")
