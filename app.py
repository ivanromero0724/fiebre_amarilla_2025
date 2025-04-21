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
from folium.plugins import HeatMap
from folium.plugins import Draw
import streamlit.components.v1 as components

# Obtener usuarios y contraseñas desde secrets
usernames = [
    st.secrets["auth"]["user1_username"], 
    st.secrets["auth"]["user2_username"], 
    st.secrets["auth"]["user3_username"],
    st.secrets["auth"]["user4_username"], 
    st.secrets["auth"]["user5_username"]
]

passwords = [
    st.secrets["auth"]["user1_password"], 
    st.secrets["auth"]["user2_password"], 
    st.secrets["auth"]["user3_password"],
    st.secrets["auth"]["user4_password"], 
    st.secrets["auth"]["user5_password"]
]

# Iniciar sesión
def login():
    st.title("Fiebre Amarilla 2025")
    user = st.text_input("Usuario")
    pwd = st.text_input("Contraseña", type="password")
    if st.button("Ingresar"):
        if user in usernames:
            user_index = usernames.index(user)
            if pwd == passwords[user_index]:
                st.session_state["authenticated"] = True
                st.rerun()  
            else:
                st.error("Contraseña incorrecta")
        else:
            st.error("Usuario no encontrado")

# Revisar si ya está autenticado
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    login()
else:
        # Configurar la página
        
        st.set_page_config(layout="wide", page_title="Mapa Fiebre Amarilla Tolima", page_icon='🦟')
        
        # Reducir espacio superior con CSS
        st.markdown(
            """
            <style>
                .block-container {
                    padding-top: 0rem !important;
                }
            </style>
            """,
            unsafe_allow_html=True
        )
        
        #LOGO
        st.markdown(
            """
            <style>
                .logo-container {
                    position: absolute;
                    top: 45px;
                    left: -10px;
                    z-index: 1000;
                }
                .logo-container img {
                    width: 80px;  /* Ajusta el tamaño del logo */
                    height: auto;
                }
            </style>
            <div class="logo-container">
                <img src="https://raw.githubusercontent.com/ivanromero0724/fiebre_amarilla_2025/main/Logo.png">
            </div>
            """,
            unsafe_allow_html=True
        )
        
        
        # URL del archivo en GitHub
        url = "https://raw.githubusercontent.com/ivanromero0724/fiebre_amarilla_2025/main/2025-02-17.xlsx"
        # Cargar los datos desde el archivo Excel
        df = pd.read_excel(url, engine="openpyxl")
        # Filtrar valores nulos en las columnas necesarias
        df = df.dropna(subset=["lat_93_LOCALIZACIN_DE_LA", "long_93_LOCALIZACIN_DE_LA", "6_VIVIENDA_EFECTIVA_"])
        datos = pd.read_excel(url, engine="openpyxl")
        # Filtrar valores nulos en coordenadas
        datos_geo = datos.dropna(subset=["lat_93_LOCALIZACIN_DE_LA", "long_93_LOCALIZACIN_DE_LA"])
        # Calcular porcentaje de viviendas georreferenciadas
        total_viviendas = len(datos)
        viviendas_geo = len(datos_geo)
        porcentaje_geo = (viviendas_geo / total_viviendas) * 100
        fa_datos = pd.read_excel("https://raw.githubusercontent.com/ivanromero0724/fiebre_amarilla_2025/main/FA_2025-04-15_FINAL.xlsx",engine="openpyxl")
        epizootias = pd.read_excel("https://raw.githubusercontent.com/ivanromero0724/fiebre_amarilla_2025/main/EPIZOOTIAS_FINAL_2.xlsx",engine="openpyxl")
        # Contar los valores no NAN en la columna LATITUD
        casos_geo_fa = fa_datos['LATITUD'].notna().sum()
        casos_geo_fa_total = len(fa_datos)
        porcentaje_geo_fa = (casos_geo_fa / casos_geo_fa_total) * 100
        fa_datos_2 = fa_datos.dropna(subset=["LATITUD", "LONGITUD"])
        
        # Obtener la fecha actual en la zona horaria de Colombia
        tz_colombia = pytz.timezone("America/Bogota")
        fecha_actual = datetime.now(tz_colombia).strftime("%d/%m/%Y")
        
        st.text("")
        st.text("")
        st.text("")
        # Mostrar el título, fecha de actualización y porcentaje de viviendas georreferenciadas juntos
        st.markdown(f"""
            <h1 style='text-align: center;'>Viviendas con abordaje en búsqueda activa comunitaria por atención a brote de Fiebre Amarilla en Tolima</h1>
            <p style='text-align: center; font-size: 14px;margin-bottom: 0px;'><b>Última fecha de actualización:</b> 15/04/2025</p>
            <p style='text-align: center; font-size: 14px;margin-bottom: 0px;'><b>Porcentaje de viviendas georreferenciadas:</b> {porcentaje_geo:.2f}% ({viviendas_geo} de {total_viviendas})</p>
            <p style='text-align: center; font-size: 14px;'><b>Porcentaje de casos de Fiebre Amarilla georreferenciados:</b> {porcentaje_geo_fa:.2f}% ({casos_geo_fa} de {casos_geo_fa_total})</p>
        """, unsafe_allow_html=True)
        
        
        # Crear el mapa 
        m = folium.Map(tiles=None,location=[4.5, -74.0], zoom_start=6)

        # Agregar minimapa
        minimap = MiniMap(toggle_display=True, position="bottomright", tile_layer="CartoDB Positron")
        m.add_child(minimap)
        
        # Crear capas para viviendas efectivas y no efectivas
        capa_si = folium.FeatureGroup(name="Viviendas efectivas",show=False)
        capa_no = folium.FeatureGroup(name="Viviendas no efectivas",show=False)
        capa_fa = folium.FeatureGroup(name="Casos confirmados de Fiebre Amarilla")
        capa_epizootias = folium.FeatureGroup(name="Epizootias")

        from branca.element import Template, MacroElement

        legend = """
        {% macro html(this, kwargs) %}
        
        <div id='maplegend' class='maplegend'
             style='position: absolute; z-index:9999; border:2px solid grey; background-color:rgba(255, 255, 255, 0.8);
             border-radius:6px; padding: 10px; font-size:14px; bottom: 20px; left: 20px;'>
        
        <div class='legend-title'>Leyenda</div>
        <div class='legend-scale'>
          <ul class='legend-labels'>
            <li><span style='background:green;opacity:0.7;'></span>Viviendas efectivas</li>
            <li><span style='background:red;opacity:0.7;'></span>Viviendas no efectivas</li>
            <li><span style='background:blue;opacity:0.7;'></span>Casos confirmados de Fiebre Amarilla</li>
            <li><span style='background:purple;opacity:0.7;'></span>Epizootias</li>
          </ul>
        </div>
        </div>
        
        <style type='text/css'>
          .maplegend .legend-title {
            text-align: left;
            margin-bottom: 5px;
            font-weight: bold;
            font-size: 90%;
            }
          .maplegend .legend-scale ul {
            margin: 0;
            padding: 0;
            list-style: none;
            }
          .maplegend .legend-scale ul li {
            font-size: 80%;
            list-style: none;
            margin-left: 0;
            line-height: 18px;
            margin-bottom: 2px;
            }
          .maplegend ul.legend-labels li span {
            display: block;
            float: left;
            height: 16px;
            width: 16px;
            margin-right: 5px;
            margin-left: 0;
            border: 1px solid #999;
            }
        </style>
        
        {% endmacro %}
        """
        
        macro = MacroElement()
        macro._template = Template(legend)
        mapa.get_root().add_child(macro)

        
        # Definir colores para los estados de las viviendas
        colores = df["6_VIVIENDA_EFECTIVA_"].str.strip().str.upper().map({"SI": "green", "NO": "red"}).fillna("gray")
        
        # Crear los marcadores en el mapa
        df_si = df[colores == "green"]
        df_no = df[colores == "red"]
        
        for lat, lon, mun, vereda, vivienda in zip(df_si["lat_93_LOCALIZACIN_DE_LA"], df_si["long_93_LOCALIZACIN_DE_LA"],df_si["1_MUNICIPIO"],df_si["4_VEREDA"],df_si["6_VIVIENDA_EFECTIVA_"]):
            popup_text = f"""
            <b>VIVIENDA EFECTIVA:</b> {vivienda} <br>
            <b>MUNICIPIO:</b> {mun} <br>
            <b>VEREDA:</b> {vereda} <br>
            """
            folium.CircleMarker(
                location=[lat, lon],
                radius=2, color="green", fill=True, fill_color="green", fill_opacity=1,
                popup=folium.Popup(popup_text, max_width=300)
            ).add_to(capa_si)
        
        for lat, lon, mun, vereda, vivienda in zip(df_no["lat_93_LOCALIZACIN_DE_LA"], df_no["long_93_LOCALIZACIN_DE_LA"],df_no["1_MUNICIPIO"],df_no["4_VEREDA"],df_no["6_VIVIENDA_EFECTIVA_"]):
            popup_text = f"""
            <b>VIVIENDA EFECTIVA:</b> {vivienda} <br>
            <b>MUNICIPIO:</b> {mun} <br>
            <b>VEREDA:</b> {vereda} <br>
            """
            
            folium.CircleMarker(
                location=[lat, lon],
                radius=2, color="red", fill=True, fill_color="red", fill_opacity=1,
                popup=folium.Popup(popup_text, max_width=300)
            ).add_to(capa_no)
        
        for lat, lon, caso, municipio, vereda, estado_caso in zip(
            fa_datos_2["LATITUD"], fa_datos_2["LONGITUD"], fa_datos_2["Caso"], 
            fa_datos_2["nmun_proce"], fa_datos_2["Vereda"], fa_datos_2["Estado del caso"]
        ):
            popup_text = f"""
            <b>CASO:</b> {caso} <br>
            <b>MUNICIPIO:</b> {municipio} <br>
            <b>VEREDA:</b> {vereda} <br>
            <b>ESTADO DEL CASO:</b> {estado_caso}
            """
            
            folium.CircleMarker(
                location=[lat, lon],
                radius=3, 
                color="gold", 
                fill=True, 
                fill_color="gold", 
                fill_opacity=1,
                popup=folium.Popup(popup_text, max_width=300)
            ).add_to(capa_fa)


        for lat, lon, municipio, vereda, notificacion, resultado in zip(
            epizootias["Latitud"], epizootias["Longitud"], epizootias["Municipio"], epizootias["Vereda"],
            epizootias["Notificacion"], epizootias["Resultado"]
        ):
            popup_text = f"""
            <b>MUNICIPIO:</b> {municipio} <br>
            <b>VEREDA:</b> {vereda} <br>
            <b>FECHA DE NOTIFICACION:</b> {notificacion}<br>
            <b>FECHA DE RESULTADO:</b> {resultado}<br>
            """
            
            folium.CircleMarker(
                location=[lat, lon],
                radius=3, 
                color="brown", 
                fill=True, 
                fill_color="brown", 
                fill_opacity=1,
                popup=folium.Popup(popup_text, max_width=300)
            ).add_to(capa_epizootias)
        
        
        
        
        # Crear la lista de coordenadas para el mapa de calor
        heat_data = [[lat, lon] for lat, lon in zip(fa_datos_2["LATITUD"], fa_datos_2["LONGITUD"])]
        # Crear la capa de calor
        heat_layer = HeatMap(heat_data, name="Mapa de Calor Casos de FA")
        # Crear un grupo de capas para el mapa de calor
        heat_group = folium.FeatureGroup(name="Mapa de calor casos confirmados de FA", show=False)  # show=False para no activar la capa
        # Añadir la capa de calor al grupo
        heat_group.add_child(heat_layer)
        
        # Agregar las capas al mapa
        m.add_child(capa_fa)
        m.add_child(capa_epizootias)
        m.add_child(heat_group)
        m.add_child(capa_si)
        m.add_child(capa_no)
        
        # Agregar capas base de Esri
        folium.TileLayer(
            tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
            attr="Esri World Imagery",
            name="Imagen satelital"
        ).add_to(m)
        
        # Agregar Google Maps como capa de mosaico
        folium.TileLayer(
            tiles="https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}",
            attr="Google",
            name="Google Maps"
        ).add_to(m)
        
        # Agregar capas base con nombres personalizados
        folium.TileLayer("OpenStreetMap").add_to(m)
        
        # Agregar capas base con nombres personalizados
        folium.TileLayer("CartoDB Positron").add_to(m)
    
        # Agregar LayerControl
        layer_control = folium.LayerControl(collapsed=False)  # No colapsado por defecto
        layer_control.add_to(m)
        
        Draw(export=True).add_to(m)

        # Mostrar el mapa en Streamlit
        folium_static(m, height=650, width=2000)

        # Contenedor con CSS para que la leyenda se superponga sobre el mapa en la esquina inferior izquierda
        # Leyenda con barra de calor continua vertical
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
                    line-height: 18px;
                    opacity: 0.9;
                    z-index: 1000;
                }
            </style>
            <div class="legend-container" style="font-size: 14px;">
                <i style="background: green; width: 12px; height: 12px; display: inline-block; margin-right: 8px; border-radius: 50%;"></i> Viviendas efectivas<br>
                <i style="background: red; width: 12px; height: 12px; display: inline-block; margin-right: 8px; border-radius: 50%;"></i> Viviendas no efectivas<br>
                <i style="background: gold; width: 12px; height: 12px; display: inline-block; margin-right: 8px; border-radius: 50%;"></i> Casos confirmados de FA<br>
                <i style="background: brown; width: 12px; height: 12px; display: inline-block; margin-right: 8px; border-radius: 50%;"></i> Epizootias
            </div>
        """, unsafe_allow_html=True)
    
        # Insertar el iframe de Looker Studio
        
        st.components.v1.iframe(
            "https://lookerstudio.google.com/embed/reporting/cd506bb2-116f-4d30-8c1d-081dd48fbeb2/page/GV0EF",
            width=2000,  # Ajusta según tu diseño
            height=2050,  # Ajusta según tu diseño
            scrolling=True
        )
