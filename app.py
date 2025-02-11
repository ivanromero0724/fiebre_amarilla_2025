import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import streamlit.components.v1 as components

# Configurar la página
st.set_page_config(layout="wide", page_title="Mapas de Fiebre Amarilla", page_icon="🦟")

# Título centrado
st.markdown("<h1 style='text-align: center;'>🗺️ Mapas de Fiebre Amarilla 2025 🦟</h1>", unsafe_allow_html=True)

# URL del archivo en GitHub
url = "https://raw.githubusercontent.com/ivanromero0724/fiebre_amarilla_2025/main/form-1__geocaracterizacion.xlsx"

@st.cache_data
def cargar_datos(url):
    """Carga el archivo Excel desde GitHub."""
    try:
        df = pd.read_excel(url, engine="openpyxl")  
        return df
    except Exception as e:
        st.error(f"Error al cargar los datos: {e}")
        return None

df = cargar_datos(url)

if df is not None:
    if {"lat_93_LOCALIZACIN_DE_LA", "long_93_LOCALIZACIN_DE_LA", "6_VIVIENDA_EFECTIVA_"}.issubset(df.columns):
        df = df.dropna(subset=["lat_93_LOCALIZACIN_DE_LA", "long_93_LOCALIZACIN_DE_LA", "6_VIVIENDA_EFECTIVA_"])

        lat_centro = 3.84234302999644
        lon_centro = -74.69905002261329
        m = folium.Map(location=[lat_centro, lon_centro], zoom_start=11)

        colores = {"SI": "green", "NO": "red"}

        for _, row in df.iterrows():
            estado_vivienda = str(row["6_VIVIENDA_EFECTIVA_"]).strip().upper()
            color = colores.get(estado_vivienda, "gray")
            folium.CircleMarker(
                location=[row["lat_93_LOCALIZACIN_DE_LA"], row["long_93_LOCALIZACIN_DE_LA"]],
                radius=2,
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=1,
                popup=f"Vivienda efectiva: {estado_vivienda}"
            ).add_to(m)

        # Agregar la leyenda como HTML
        legend_html = '''
        <div style="
            position: fixed; 
            bottom: 20px; left: 20px; width: 220px; height: 50px; 
            background-color: white; z-index:9999; font-size:14px;
            border:2px solid grey; padding: 10px; border-radius: 8px;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.3);
        ">
            <b> Leyenda </b><br>
            <span style="color:green; font-size:18px;">&#9679;</span> Vivienda efectiva <br>
            <span style="color:red; font-size:18px;">&#9679;</span> Vivienda no efectiva <br>
        </div>
        '''

        # Guardar el mapa con la leyenda en un archivo HTML temporal
        m_html = m._repr_html_()
        full_map = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Mapa de Fiebre Amarilla</title>
        </head>
        <body>
            {m_html}
            {legend_html} <!-- Agregar la leyenda aquí -->
        </body>
        </html>
        """

        # Renderizar el mapa en Streamlit
        components.html(full_map, width=1310, height=600)
    else:
        st.error("Las columnas requeridas no se encuentran en el archivo.")
else:
    st.error("No se pudo cargar el archivo. Verifica la URL y el formato.")
