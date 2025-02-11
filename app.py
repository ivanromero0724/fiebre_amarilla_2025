import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster

# Configurar la página
st.set_page_config(layout="wide", page_title="Mapas de Fiebre Amarilla", page_icon="🦟")

# Título centrado
st.markdown("<h1 style='text-align: center;'>🦟 Mapas de Fiebre Amarilla 2025 🦟</h1>", unsafe_allow_html=True)

# URL del archivo en GitHub
url = "https://raw.githubusercontent.com/ivanromero0724/fiebre_amarilla_2025/main/form-1__geocaracterizacion.xlsx"

@st.cache_data
def cargar_datos(url):
    try:
        df = pd.read_excel(url, engine="openpyxl")  
        return df
    except Exception as e:
        st.error(f"Error al cargar los datos: {e}")
        return None

df = cargar_datos(url)

if df is not None:
    # Verificar que las columnas necesarias existen y eliminar filas con valores NaN
    if {"lat_93_LOCALIZACIN_DE_LA", "long_93_LOCALIZACIN_DE_LA", "6_VIVIENDA_EFECTIVA_"}.issubset(df.columns):
        df = df.dropna(subset=["lat_93_LOCALIZACIN_DE_LA", "long_93_LOCALIZACIN_DE_LA", "6_VIVIENDA_EFECTIVA_"])

        # Crear mapa centrado en Tolima
        m = folium.Map(location=[4.5, -75.2], zoom_start=8)

        # Definir capas para cada categoría de vivienda efectiva
        capa_si = folium.FeatureGroup(name="Vivienda efectiva (SI)").add_to(m)
        capa_no = folium.FeatureGroup(name="No efectiva (NO)").add_to(m)

        # Definir colores según la variable "6_VIVIENDA_EFECTIVA_"
        colores = {"SI": "red", "NO": "blue"}

        # Agrupar puntos cercanos en clústeres
        marker_cluster_si = MarkerCluster().add_to(capa_si)
        marker_cluster_no = MarkerCluster().add_to(capa_no)

        # Agregar puntos desde el DataFrame
        for _, row in df.iterrows():
            estado_vivienda = str(row["6_VIVIENDA_EFECTIVA_"]).strip().upper()
            color = colores.get(estado_vivienda, "gray")  # Gris si el valor es desconocido

            marker = folium.CircleMarker(
                location=[row["lat_93_LOCALIZACIN_DE_LA"], row["long_93_LOCALIZACIN_DE_LA"]],
                radius=5,
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.6,
                popup=f"Vivienda efectiva: {estado_vivienda}"
            )

            # Asignar el marcador a la capa correspondiente
            if estado_vivienda == "SI":
                marker.add_to(marker_cluster_si)
            elif estado_vivienda == "NO":
                marker.add_to(marker_cluster_no)

        # Agregar control de capas (esto actúa como leyenda)
        folium.LayerControl().add_to(m)

        # Mostrar el mapa en Streamlit
        folium_static(m, width=1310, height=600)
    else:
        st.error("Las columnas requeridas no se encuentran en el archivo.")
else:
    st.error("No se pudo cargar el archivo. Verifica la URL y el formato.")
