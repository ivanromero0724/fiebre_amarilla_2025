import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

# Configurar la página
st.set_page_config(layout="wide", page_title="Mapas de Fiebre Amarilla", page_icon="🦟")

# Título centrado
st.markdown("<h1 style='text-align: center;'>🦟 Mapas de Fiebre Amarilla 2025 🦟</h1>", unsafe_allow_html=True)

# URL del archivo CSV en GitHub
url = "https://raw.githubusercontent.com/ivanromero0724/fiebre_amarilla_2025/main/form-1__geocaracterizacion.csv"

# Cargar datos
try:
    df = pd.read_csv(url, sep=",", encoding="utf-8")
    st.success("✅ Datos cargados con éxito")
    
    # Mostrar los primeros datos
    st.dataframe(df.head())

    # Verificar si las columnas de latitud y longitud existen
    if "lat_93_LOCALIZACIN_DE_LA" in df.columns and "long_93_LOCALIZACIN_DE_LA" in df.columns:
        
        # Convertir a tipo numérico (evitar errores)
        df["lat_93_LOCALIZACIN_DE_LA"] = pd.to_numeric(df["lat_93_LOCALIZACIN_DE_LA"], errors="coerce")
        df["long_93_LOCALIZACIN_DE_LA"] = pd.to_numeric(df["long_93_LOCALIZACIN_DE_LA"], errors="coerce")

        # Filtrar filas con valores válidos
        df = df.dropna(subset=["lat_93_LOCALIZACIN_DE_LA", "long_93_LOCALIZACIN_DE_LA"])

        # Crear el mapa centrado en la ubicación promedio
        lat_media = df["lat_93_LOCALIZACIN_DE_LA"].mean()
        lon_media = df["long_93_LOCALIZACIN_DE_LA"].mean()
        m = folium.Map(location=[lat_media, lon_media], zoom_start=8)

        # Agregar puntos según la variable 6_VIVIENDA_EFECTIVA_
        for _, row in df.iterrows():
            folium.Marker(
                location=[row["lat_93_LOCALIZACIN_DE_LA"], row["long_93_LOCALIZACIN_DE_LA"]],
                popup=f"Vivienda efectiva: {row['6_VIVIENDA_EFECTIVA_']}",
                icon=folium.Icon(color="blue")
            ).add_to(m)

        # Mostrar el mapa en Streamlit
        folium_static(m, width=1310, height=600)

    else:
        st.error("⚠️ Las columnas de latitud y longitud no están en el archivo CSV.")

except Exception as e:
    st.error(f"⚠️ Error al cargar los datos: {e}")
