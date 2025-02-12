import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from folium.plugins import MiniMap
from datetime import datetime
import pytz
from branca.element import Template, MacroElement
import matplotlib.pyplot as plt
import plotly.express as px

# Configurar la página
st.set_page_config(layout="wide", page_title="Mapa de Fiebre Amarilla", page_icon="\U0001F99F")

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

# URL del archivo en GitHub
url = "https://raw.githubusercontent.com/ivanromero0724/fiebre_amarilla_2025/main/2025-02-11.xlsx"
# Cargar los datos desde el archivo Excel
df = pd.read_excel(url, engine="openpyxl")
# Filtrar valores nulos en las columnas necesarias
df = df.dropna(subset=["lat_93_LOCALIZACIN_DE_LA", "long_93_LOCALIZACIN_DE_LA", "6_VIVIENDA_EFECTIVA_"])
datos = pd.read_excel(url, engine="openpyxl")
# Filtrar valores nulos en coordenadas
datos_geo = datos.dropna(subset=["lat_93_LOCALIZACIN_DE_LA", "long_93_LOCALIZACIN_DE_LA"])
# Calcular porcentaje de viviendas georreferenciadas
porcentaje_geo = (len(datos_geo) / len(datos)) * 100

# Obtener la fecha actual en la zona horaria de Colombia
tz_colombia = pytz.timezone("America/Bogota")
fecha_actual = datetime.now(tz_colombia).strftime("%d/%m/%Y")

# Mostrar el título, fecha de actualización y porcentaje de viviendas georreferenciadas juntos
st.markdown(f"""
    <h1 style='text-align: center;'>Viviendas con abordaje en búsqueda activa comunitaria por atención a brote de Fiebre Amarilla en Tolima</h1>
    <p style='text-align: center; font-size: 14px;'><b>Última fecha de actualización:</b> {fecha_actual}</p>
    <p style='text-align: center; font-size: 14px;'><b>Porcentaje de viviendas georreferenciadas:</b> {porcentaje_geo:.2f}%</p>
""", unsafe_allow_html=True)


# Definir coordenadas centrales del mapa
lat_centro, lon_centro = 3.84234302999644, -74.69905002261329
m = folium.Map(location=[lat_centro, lon_centro], zoom_start=11, tiles= None)

# Agregar minimapa
minimap = MiniMap(toggle_display=True, position="bottomright")
m.add_child(minimap)

# Crear capas para viviendas efectivas y no efectivas
capa_si = folium.FeatureGroup(name="Vivienda efectiva")
capa_no = folium.FeatureGroup(name="Vivienda no efectiva")

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

# Agregar capas base de Esri
folium.TileLayer(
    tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
    attr="Esri World Imagery",
    name="Imagen satelital"
).add_to(m)

# Agregar capas base con nombres personalizados
folium.TileLayer("CartoDB Positron").add_to(m)

# Agregar capas base con nombres personalizados
folium.TileLayer("OpenStreetMap").add_to(m)

folium.LayerControl().add_to(m)

# Mostrar el mapa en Streamlit
folium_static(m, height=650, width=1305)

# Contenedor con CSS para que la leyenda se superponga sobre el mapa en la esquina inferior izquierda
st.markdown("""
    <style>
        .legend-container {
            position: absolute;
            bottom: 35px;
            left: 10px;
            background-color: white;
            padding: 10px;
            border-radius: 5px;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.3);
            width: 190px;
            line-height: 18px;
            opacity: 0.9;
            z-index: 1000;
        }
    </style>
    <div class="legend-container">
        <i style="background: green; width: 12px; height: 12px; display: inline-block; margin-right: 8px; border-radius: 50%;"></i> Vivienda efectiva<br>
        <i style="background: red; width: 12px; height: 12px; display: inline-block; margin-right: 8px; border-radius: 50%;"></i> Vivienda no efectiva
    </div>
""", unsafe_allow_html=True)




# Sección de gráficos
col1, col2, col3 = st.columns(3)

with col1:
    fig1 = px.pie(datos, names="1_MUNICIPIO", title="Distribución por Municipio")
    fig1.update_layout(title_x=0.5)  # Centrar título
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    fig2 = px.pie(datos, names="2_AREA", title="Distribución por Área")
    st.plotly_chart(fig2, use_container_width=True)

with col3:
    fig3 = px.pie(datos, names="6_VIVIENDA_EFECTIVA_", title="Viviendas Efectivas vs No Efectivas")
    st.plotly_chart(fig3, use_container_width=True)

# Tabla resumen por municipio
st.markdown("### Resumen de Viviendas por Municipio")
tabla_resumen = datos.groupby("1_MUNICIPIO")["6_VIVIENDA_EFECTIVA_"].value_counts().unstack(fill_value=0)
tabla_resumen["Total"] = tabla_resumen.sum(axis=1)
tabla_resumen.columns = ["Viviendas No Efectivas", "Viviendas Efectivas", "Total"]

st.dataframe(tabla_resumen.style.set_properties(**{'background-color': 'white', 'border-radius': '10px', 'padding': '10px'}))
