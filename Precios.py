import streamlit as st
from src.retrieve_from_db import retrieve
from src.plots import plot_mean_price_ca
from src.maps import map_mean_price_ca, map_mean_price_pr
from src.tables import table_price_pr
import pandas as pd
import seaborn as sns

##############################################################
### PAGE SETTINGS  ###########################################
##############################################################

st.set_page_config (page_title="Precios de olivas, pistachos, uvas - Nuevos datos", layout="wide")
st.header ('Precios al agricultor ')
st.subheader ('Elige el cultivo que te interesa para ver los precios al agricultor en España')

# hide menu and footer from streamlit
hide_menu_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """
st.markdown (hide_menu_style, unsafe_allow_html=True)

##############################################################
### SPLIT IN COLUMNS    ######################################
##############################################################
col1, col2, col3 = st.columns ([1, 1, 1])

with col1:
    st.write ('#### Aceitunas')
    valores_oli = st.button ('Mostrar precios de aceitunas')

with col2:
    st.write ('#### Pistachos')
    valores_pis = st.button ('Mostrar precios de pistachos')

with col3:
    st.write ('#### Uvas')
    valores_gra = st.button ('Mostrar precios de uvas')

##############################################################
### SELECT DF AS USER INPUT         ##########################
##############################################################

if valores_oli:
    df = retrieve ('olivares_t')
    crop = 'Aceitunas'

if valores_pis:
    df = retrieve ('pistachos_t')
    crop = 'Pistachos'

if valores_gra:
    df = retrieve ('uvas_t')
    crop = 'Uvas'

if not valores_oli and not valores_pis and not valores_gra:
    st.stop ()

##############################################################
### SHOW DATA FROM DATAFRAMES       ##########################
##############################################################

# mean prices by autonomous community

st.markdown ('<hr>', unsafe_allow_html=True)
st.subheader (f'Precio medio por Comunidad Autónoma - {crop}')
col4, col5 = st.columns ([1, 1])

with col4:
    fig = plot_mean_price_ca (df)
    st.plotly_chart (fig, use_container_width=True)

with col5:
    st.write ("#")
    map = map_mean_price_ca (df)
    st.pyplot (map)

# mean prices by province

st.markdown ('<hr>', unsafe_allow_html=True)
st.subheader (f'Precio medio por Provincias - {crop}')
st.write ("#")
col6, col7 = st.columns ([1, 1])

with col6:
    table_price_pr(df)

with col7:
    # st.write("#")
    map = map_mean_price_pr (df)
    st.pyplot (map)

