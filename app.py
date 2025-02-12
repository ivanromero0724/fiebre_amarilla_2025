import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from folium.plugins import MiniMap
from datetime import datetime
import pytz
from folium import Element

st.set_page_config(layout="wide", page_title="Mapas de Fiebre Amarilla", page_icon="\U0001F99F")

st.markdown("""
    <style>
        .block-container {
            padding-top: 2rem !important;
        }
    </style>
    """, unsafe_allow_html=True)

fecha_actual = datetime.now(pytz.timezone("America/Bogota")).strftime("%d/%m/%Y")

st.markdown(f"""
    <h1 style='text-align: center;'>Viviendas con abordaje en búsqueda activa comunitaria por atención a brote de Fiebre Amarilla en Tolima</h1>
    <p style='text-align: center; font-size: 14px;'><b>Fecha de actualización:</b> {fecha_actual}</p>
    """, unsafe_allow_html=True)

url = "https://raw.githubusercontent.com/ivanromero0724/fiebre_amarilla_2025/main/form-1__geocaracterizacion.xlsx"
df = pd.read_excel(url, engine="openpyxl")
df = df.dropna(subset=["lat_93_LOCALIZACIN_DE_LA", "long_93_LOCALIZACIN_DE_LA", "6_VIVIENDA_EFECTIVA_"])

lat_centro, lon_centro = 3.84234302999644, -74.69905002261329
m = folium.Map(location=[lat_centro, lon_centro], zoom_start=11)

minimap = MiniMap(toggle_display=True, position="bottomright")
m.add_child(minimap)

capa_si, capa_no = folium.FeatureGroup(name="Viviendas efectivas"), folium.FeatureGroup(name="No efectivas")
colores = {"SI": "green", "NO": "red"}

for _, row in df.iterrows():
    estado_vivienda = str(row["6_VIVIENDA_EFECTIVA_"]).strip().upper()
    color = colores.get(estado_vivienda, "gray")
    marker = folium.CircleMarker(
        location=[row["lat_93_LOCALIZACIN_DE_LA"], row["long_93_LOCALIZACIN_DE_LA"]],
        radius=2, color=color, fill=True, fill_color=color, fill_opacity=1,
        popup=f"Vivienda efectiva: {estado_vivienda}"
    )
    (capa_si if estado_vivienda == "SI" else capa_no).add_child(marker)

m.add_child(capa_si)
m.add_child(capa_no)
folium.LayerControl().add_to(m)

legend_html = """
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
"""
legend = Element(legend_html)
m.get_root().html.add_child(legend)

folium_static(m, width=1305, height=600)
