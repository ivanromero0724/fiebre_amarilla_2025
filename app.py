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

        # Crear mapa centrado en el Tolima
        m = folium.Map(location=[4.5, -75.2], zoom_start=8)

        # Definir colores según la variable "6_VIVIENDA_EFECTIVA_"
        colores = {"SI": "red", "NO": "blue"}

        # Agrupar puntos cercanos en clústeres
        marker_cluster = MarkerCluster().add_to(m)

        # Agregar puntos desde el DataFrame
        for _, row in df.iterrows():
            estado_vivienda = str(row["6_VIVIENDA_EFECTIVA_"]).strip().upper()
            color = colores.get(estado_vivienda, "gray")  # Usa gris si no es SI o NO

            folium.CircleMarker(
                location=[row["lat_93_LOCALIZACIN_DE_LA"], row["long_93_LOCALIZACIN_DE_LA"]],
                radius=5,
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.6,
                popup=f"Vivienda efectiva: {estado_vivienda}"
            ).add_to(marker_cluster)

        # Agregar leyenda oficial de Folium
        legend = folium.map.FeatureGroup(name="Leyenda")
        legend.add_child(folium.Marker(
            location=[4.2, -75.2],  # Ubicación arbitraria para que la leyenda aparezca
            icon=folium.DivIcon(html="""
                <div style="
                    background-color: white; padding: 10px; border-radius: 5px;
                    box-shadow: 2px 2px 5px rgba(0,0,0,0.3); font-size:14px;
                ">
                    <b>Leyenda</b><br>
                    <span style="color:red;">●</span> Vivienda efectiva (SI)<br>
                    <span style="color:blue;">●</span> No efectiva (NO)
                </div>
            """)
        ))
        m.add_child(legend)

        # Agregar control de capas
        folium.LayerControl().add_to(m)

        # Mostrar el mapa en Streamlit
        folium_static(m, width=1310, height=600)
    else:
        st.error("Las columnas requeridas no se encuentran en el archivo.")
else:
    st.error("No se pudo cargar el archivo. Verifica la URL y el formato.")
