import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from folium.plugins import MiniMap
from branca.element import Template, MacroElement
from datetime import datetime
import pytz

# Configurar la página
st.set_page_config(layout="wide", page_title="Mapas de Fiebre Amarilla", page_icon="🦟")

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

# Título centrado
st.markdown("<h1 style='text-align: center;'>Viviendas con abordaje en búsqueda activa comunitaria por atención a brote de Fiebre Amarilla en Tolima</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; font-size: 14px;'><b>Fecha de actualización:</b> {fecha_actual}</p>", unsafe_allow_html=True)

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
    # Verificar que las columnas requeridas existen
    if {"lat_93_LOCALIZACIN_DE_LA", "long_93_LOCALIZACIN_DE_LA", "6_VIVIENDA_EFECTIVA_"}.issubset(df.columns):
        df = df.dropna(subset=["lat_93_LOCALIZACIN_DE_LA", "long_93_LOCALIZACIN_DE_LA", "6_VIVIENDA_EFECTIVA_"])

        # Coordenadas para centrar el mapa en Tolima
        lat_centro = 3.84234302999644
        lon_centro = -74.69905002261329

        # Crear mapa centrado en Tolima
        m = folium.Map(location=[lat_centro, lon_centro], zoom_start=11)

        # Agregar el plugin MiniMap
        minimap = MiniMap(toggle_display=True, position="bottomright")
        m.add_child(minimap)

        # Crear grupos de capas para la leyenda
        capa_si = folium.FeatureGroup(name="Viviendas efectivas").add_to(m)
        capa_no = folium.FeatureGroup(name="No efectivas").add_to(m)

        # Colores según la variable "6_VIVIENDA_EFECTIVA_"
        colores = {"SI": "green", "NO": "red"}

        # Agregar puntos desde el DataFrame
        for _, row in df.iterrows():
            estado_vivienda = str(row["6_VIVIENDA_EFECTIVA_"]).strip().upper()
            color = colores.get(estado_vivienda, "gray")  # Gris si el valor es desconocido

            marker = folium.CircleMarker(
                location=[row["lat_93_LOCALIZACIN_DE_LA"], row["long_93_LOCALIZACIN_DE_LA"]],
                radius=2,
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=1,
                popup=f"Vivienda efectiva: {estado_vivienda}"
            )

            # Asignar el marcador a la capa correspondiente
            if estado_vivienda == "SI":
                marker.add_to(capa_si)
            elif estado_vivienda == "NO":
                marker.add_to(capa_no)

        # Agregar control de capas (esto actúa como la leyenda)
        folium.LayerControl().add_to(m)

        # 📌 **Definir la leyenda personalizada**
        legend_html = """
        {% macro html(this, kwargs) %}
        <div id='maplegend' class='maplegend' 
            style='position: absolute; z-index: 9999; background-color: rgba(255, 255, 255, 0.7);
            border-radius: 6px; padding: 10px; font-size: 12px; right: 20px; bottom: 20px;'>     
        
        <b>🦟 Leyenda</b>
        <div class='legend-scale'>
          <ul class='legend-labels' style='list-style: none; padding-left: 10px;'>
            <li><span style='background: green; display: inline-block; width: 12px; height: 12px; margin-right: 5px;'></span> Viviendas efectivas</li>
            <li><span style='background: red; display: inline-block; width: 12px; height: 12px; margin-right: 5px;'></span> No efectivas</li>
          </ul>
        </div>
        </div> 
        <style type='text/css'>
          .maplegend .legend-scale ul {margin: 0; padding: 0; color: #333;}
          .maplegend .legend-scale ul li {list-style: none; line-height: 18px; margin-bottom: 5px;}
        </style>
        {% endmacro %}
        """

        # 📌 **Agregar la leyenda al mapa**
        macro = MacroElement()
        macro._template = Template(legend_html)
        m.get_root().add_child(macro)

        # Mostrar el mapa en Streamlit
        folium_static(m, width=1305, height=600)
    else:
        st.error("Las columnas requeridas no se encuentran en el archivo.")
else:
    st.error("No se pudo cargar el archivo. Verifica la URL y el formato.")
