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
st.header ('Precios al agricultor de cultivos de leñosas en España')

# hide menu and footer from streamlit
hide_menu_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """
st.markdown (hide_menu_style, unsafe_allow_html=True)

##############################################################
### SIDEBAR USER OPTIONS                 #####################
##############################################################
st.markdown ('<hr>', unsafe_allow_html=True)

# user selects the year
st.sidebar.subheader ('Elige un año')
year = st.sidebar.radio('## Elige un año', ('Todos',2019,2020,2021,2022),horizontal=True)
if year == 'Todos': year=[2019,2020,2021,2022]
else: year = [year]

st.sidebar.markdown ('<hr>', unsafe_allow_html=True)

# user selects the crop
st.sidebar.subheader ('Elige un cultivo')
crop = st.sidebar.radio('## Elige un cultivo', ('Aceitunas','Pistachos','Uvas'))

if crop == 'Aceitunas':
    df = retrieve ('olivares_t')

elif crop == 'Pistachos':
    df = retrieve ('pistachos_t')

elif crop == 'Uvas':
    df = retrieve ('uvas_t')

st.sidebar.markdown ('<hr>', unsafe_allow_html=True)

##############################################################
### SHOW DATA FROM DATAFRAMES       ##########################
##############################################################

# mean prices by autonomous community

st.subheader (f'Precio medio por Comunidad Autónoma - {crop}')
col4, col5 = st.columns ([1, 1])

with col4:
    fig = plot_mean_price_ca (df,year)
    st.plotly_chart (fig, use_container_width=True)

with col5:
    st.write ("#")
    map = map_mean_price_ca (df,year)
    st.pyplot (map)

# mean prices by province

st.markdown ('<hr>', unsafe_allow_html=True)
st.subheader (f'Precio medio por Provincias - {crop}')
st.write ("#")
col6, col7 = st.columns ([1, 1])

with col6:
    table_price_pr(df,year)

with col7:
    st.write (" Si la región aparece en blanco es porque no hay datos de ella.")
    map = map_mean_price_pr (df,year)
    st.pyplot (map)


# mean prices by province

st.markdown ('<hr>', unsafe_allow_html=True)
st.subheader (f'Consulta el precio en tu región - {crop}')
st.write ("#")
st.write ("Formulario para comunidad y provincia y que de un listado en df con los municipios y el precio, sólo los no nulos")