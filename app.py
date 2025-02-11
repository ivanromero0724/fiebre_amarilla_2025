import streamlit as st
import folium
from streamlit_folium import folium_static

# Configurar la página para que use todo el ancho disponible
st.set_page_config(layout="wide", page_title="Mapas de Fiebre Amarilla", page_icon="🦟")

# Aplicar estilo minimalista con CSS
st.markdown("""
    <style>
    /* Cambiar el fondo de la aplicación */
    body {
        background-color: white;
        font-family: Arial, sans-serif;
    }
    
    /* Centrar el título */
    .title {
        text-align: center;
        font-size: 36px;
        font-weight: bold;
        color: black;
    }

    /* Centrar el mapa */
    .mapa-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 20px;
    }

    /* Ocultar barra superior y menú de Streamlit */
    #MainMenu, header, footer {visibility: hidden;}

    </style>
    """, unsafe_allow_html=True)

# Título centrado con clase CSS personalizada
st.markdown("<h1 class='title'>🦟 Mapas de Fiebre Amarilla 2025 🦟</h1>", unsafe_allow_html=True)

# Crear columnas para centrar el mapa
col1, col2, col3 = st.columns([1, 3, 1])

with col2:  # Centrar el mapa en la columna del medio
    # Crear un mapa con Folium
    m = folium.Map(location=[11.5449, -72.9066], zoom_start=8, control_scale=True)

    # Agregar un marcador de ejemplo
    folium.Marker(
        [11.5449, -72.9066],
        popup="Ejemplo de ubicación en La Guajira",
        icon=folium.Icon(color="blue"),
    ).add_to(m)

    # Mostrar el mapa con un tamaño más grande y centrado
    st.markdown('<div class="mapa-container">', unsafe_allow_html=True)
    folium_static(m, width=1000, height=600)
    st.markdown('</div>', unsafe_allow_html=True)
