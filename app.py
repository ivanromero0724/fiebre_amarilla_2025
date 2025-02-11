import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from folium.plugins import MiniMap
import requests
from io import BytesIO

# Configurar la página
st.set_page_config(layout="wide", page_title="Mapas de Fiebre Amarilla", page_icon="🦟")

# Título centrado
st.markdown("<h1 style='text-align: center;'>🗺️ Mapas de Fiebre Amarilla 2025 🦟</h1>", unsafe_allow_html=True)

# URL del archivo en GitHub
url = "https://raw.githubusercontent.com/ivanromero0724/fiebre_amarilla_2025/main/form-1__geocaracterizacion.xlsx"

def cargar_datos(url):
    """Carga el archivo Excel desde GitHub sin usar caché."""
    try:
        response = requests.get(url, timeout=10)  # Forzar nueva descarga
        response.raise_for_status()
        df = pd.read_excel(BytesIO(response.content), engine="openpyxl")  
        return df
    except requests.exceptions.RequestException:
        st.warning("⚠️ No se pudo descargar el archivo. Puede que haya sido eliminado o la URL sea incorrecta.")
        return None
    except Exception as e:
        st.error(f"Error al leer el archivo: {e}")
        return None

df = cargar_datos(url)

if df is not None:
    if {"lat_93_LOCALIZACIN_DE_LA", "long_93_LOCALIZACIN_DE_LA", "6_VIVIENDA_EFECTIVA_"}.issubset(df.columns):
        df = df.dropna(subset=["lat_93_LOCALIZACIN_DE_LA", "long_93_LOCALIZACIN_DE_LA", "6_VIVIENDA_EFECTIVA_"])

        # Coordenadas para centrar el mapa en Tolima
        lat_centro = 3.84234302999644
        lon_centro = -74.69905002261329

        # Crear mapa centrado en Tolima
        m = folium.Map(location=[lat_centro, lon_centro], zoom_start=11)

        # Agregar MiniMap
        minimap = MiniMap(toggle_display=True, position="bottomright")
        m.add_child(minimap)

        # Crear capas de leyenda
        capa_si = folium.FeatureGroup(name="Viviendas efectivas").add_to(m)
        capa_no = folium.FeatureGroup(name="No efectivas").add_to(m)

        # Colores según la variable "6_VIVIENDA_EFECTIVA_"
        colores = {"SI": "green", "NO": "red"}

        # Agregar puntos desde el DataFrame
        for _, row in df.iterrows():
            estado_vivienda = str(row["6_VIVIENDA_EFECTIVA_"]).strip().upper()
            color = colores.get(estado_vivienda, "gray")

            marker = folium.CircleMarker(
                location=[row["lat_93_LOCALIZACIN_DE_LA"], row["long_93_LOCALIZACIN_DE_LA"]],
                radius=2,
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=1,
                popup=f"Vivienda efectiva: {estado_vivienda}"
            )

            if estado_vivienda == "SI":
                marker.add_to(capa_si)
            elif estado_vivienda == "NO":
                marker.add_to(capa_no)

        # Agregar botón de pantalla completa
        folium.plugins.Fullscreen(
            position="topleft",
            title="Expandir",
            title_cancel="Salir",
            force_separate_button=True,
        ).add_to(m)

        # Agregar control de capas
        folium.LayerControl().add_to(m)

        # Mostrar el mapa
        folium_static(m, width=1305, height=600)

    else:
        st.error("Las columnas requeridas no se encuentran en el archivo.")
else:
    st.warning("⚠️ No hay datos disponibles. Puede que el archivo haya sido eliminado o la URL sea incorrecta.")
