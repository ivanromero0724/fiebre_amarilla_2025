import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from folium.plugins import MiniMap
from datetime import datetime
import pytz
from branca.element import Template, MacroElement

# Configurar la página
st.set_page_config(layout="wide", page_title="Mapas de Fiebre Amarilla", page_icon="\U0001F99F")

# Reducir espacio superior con CSS
st.markdown(
    """
    <style>
        .block-container {
            padding-top: 2rem !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Obtener la fecha actual en la zona horaria de Colombia
tz_colombia = pytz.timezone("America/Bogota")
fecha_actual = datetime.now(tz_colombia).strftime("%d/%m/%Y")

# Mostrar el título y la fecha de actualización
st.markdown("""
    <h1 style='text-align: center;'>Viviendas con abordaje en búsqueda activa comunitaria por atención a brote de Fiebre Amarilla en Tolima</h1>
    <p style='text-align: center; font-size: 14px;'><b>Fecha de actualización:</b> {}</p>
    """.format(fecha_actual), unsafe_allow_html=True)

# URL del archivo en GitHub
url = "https://raw.githubusercontent.com/ivanromero0724/fiebre_amarilla_2025/main/form-1__geocaracterizacion.xlsx"

# Cargar los datos desde el archivo Excel
df = pd.read_excel(url, engine="openpyxl")

# Filtrar valores nulos en las columnas necesarias
df = df.dropna(subset=["lat_93_LOCALIZACIN_DE_LA", "long_93_LOCALIZACIN_DE_LA", "6_VIVIENDA_EFECTIVA_"])

# Definir coordenadas centrales del mapa
lat_centro, lon_centro = 3.84234302999644, -74.69905002261329
m = folium.Map(location=[lat_centro, lon_centro], zoom_start=11)

# Agregar minimapa
minimap = MiniMap(toggle_display=True, position="bottomright")
m.add_child(minimap)

# Crear capas para viviendas efectivas y no efectivas
capa_si = folium.FeatureGroup(name="Viviendas efectivas")
capa_no = folium.FeatureGroup(name="No efectivas")

# Definir colores para los estados de las viviendas
colores = df["6_VIVIENDA_EFECTIVA_"].str.strip().str.upper().map({"SI": "green", "NO": "red"}).fillna("gray")

# Crear los marcadores en el mapa
df_si = df[colores == "green"]
df_no = df[colores == "red"]

for lat, lon in zip(df_si["lat_93_LOCALIZACIN_DE_LA"], df_si["long_93_LOCALIZACIN_DE_LA"]):
    folium.CircleMarker(
        location=[lat, lon],
        radius=2, color="green", fill=True, fill_color="green", fill_opacity=1,
        popup="Vivienda efectiva: SI"
    ).add_to(capa_si)

for lat, lon in zip(df_no["lat_93_LOCALIZACIN_DE_LA"], df_no["long_93_LOCALIZACIN_DE_LA"]):
    folium.CircleMarker(
        location=[lat, lon],
        radius=2, color="red", fill=True, fill_color="red", fill_opacity=1,
        popup="Vivienda efectiva: NO"
    ).add_to(capa_no)

# Agregar las capas al mapa
m.add_child(capa_si)
m.add_child(capa_no)
folium.LayerControl().add_to(m)

# Agregar leyenda con branca
legend_html = '''
<div style="position: fixed; 
            bottom: 50px; left: 50px; width: 200px; height: 90px; 
            background-color: white; z-index:9999; font-size:14px;
            border-radius: 8px; padding: 10px; box-shadow: 2px 2px 6px rgba(0,0,0,0.3);">
    <p style="margin: 0; font-weight: bold; text-align: center;">Leyenda</p>
    <p style="margin: 5px 0;">
        <span style="display: inline-block; width: 12px; height: 12px; background-color: green; border-radius: 50%;"></span> 
        Vivienda efectiva
    </p>
    <p style="margin: 5px 0;">
        <span style="display: inline-block; width: 12px; height: 12px; background-color: red; border-radius: 50%;"></span> 
        No efectiva
    </p>
</div>
'''
legend = MacroElement()
legend._template = Template(legend_html)
m.get_root().html.add_child(legend)

# Mostrar el mapa en Streamlit
folium_static(m)
