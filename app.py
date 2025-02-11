import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

# Configurar la página
st.set_page_config(layout="wide", page_title="Mapas de Fiebre Amarilla", page_icon="🦟")

# Título centrado
st.markdown("<h1 style='text-align: center;'>🦟 Mapas de Fiebre Amarilla 2025 🦟</h1>", unsafe_allow_html=True)

# Cargar datos desde GitHub
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
    # Verificar si las columnas necesarias existen y no tienen valores NaN
    if "lat_93_LOCALIZACIN_DE_LA" in df.columns and "long_93_LOCALIZACIN_DE_LA" in df.columns:
        df = df.dropna(subset=["lat_93_LOCALIZACIN_DE_LA", "long_93_LOCALIZACIN_DE_LA"])

        # Crear mapa centrado en el Tolima
        m = folium.Map(location=[4.5, -75.2], zoom_start=8)

        # Definir colores según la variable de vivienda efectiva
        colores = {1: "red", 0: "blue"}  # Rojo si es 1 (Vivienda efectiva), Azul si es 0 (No efectiva)

        # Agregar puntos desde el DataFrame
        for _, row in df.iterrows():
            estado_vivienda = row.get("6_VIVIENDA_EFECTIVA_", 0)
            color = colores.get(estado_vivienda, "gray")

            folium.CircleMarker(
                location=[row["lat_93_LOCALIZACIN_DE_LA"], row["long_93_LOCALIZACIN_DE_LA"]],
                radius=5,
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.6,
                popup=f"Vivienda efectiva: {estado_vivienda}"
            ).add_to(m)

        # Agregar leyenda personalizada
        legend_html = """
        <div style="
            position: fixed; 
            bottom: 50px; left: 50px; width: 200px; height: 100px; 
            background-color: white; z-index:9999; font-size:14px;
            border-radius: 10px; padding: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.3);
        ">
            <b>Leyenda</b><br>
            <i class="fa fa-circle" style="color:red"></i> Vivienda efectiva<br>
            <i class="fa fa-circle" style="color:blue"></i> No efectiva
        </div>
        """
        m.get_root().html.add_child(folium.Element(legend_html))

        # Mostrar el mapa en Streamlit
        folium_static(m, width=1310, height=600)
    else:
        st.error("Las columnas de latitud y longitud no se encuentran en el archivo.")
else:
    st.error("No se pudo cargar el archivo. Verifica la URL y el formato.")
