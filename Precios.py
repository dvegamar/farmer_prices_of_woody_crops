import streamlit as st
from src.retrieve_from_db import retrieve
from src.plots import plot_mean_price_ca
from src.maps import map_mean_price_ca, map_mean_price_pr
from src.tables import table_price_pr
import pandas as pd

##############################################################
### PAGE SETTINGS  ###########################################
##############################################################

st.set_page_config (page_title="Precios de olivas, pistachos, uvas - Nuevos datos", layout="wide")
st.header ('Precios al agricultor de cultivos de leñosas en España')
st.write('##### Precios obtenidos directamente de los agricultores mediante acceso a esta web')
st.write('Esta aplicación ofrece los precios pagados a los agricultores en las diferentes almazaras o cooperativas'
         ' en las que venden sus productos.')
st.write('Además de medias autonómicas y provinciales podemos ver qué precios se pagan a nivel local para diferentes'
         'cultivos leñosos como la viña, el olivo o el pistacho.')
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
year = st.sidebar.radio('## Elige un año', (2018,2019,2020,2021,2022,2023,'Todos'), index=4, horizontal=True)
if year == 'Todos': year=[2018,2019,2020,2021,2022,2023]
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

# filter the dataframe with the crop and years list selected
df = df.loc [df ['anio'].isin(year)]

st.sidebar.markdown ('<hr>', unsafe_allow_html=True)

##############################################################
### EMPTY DATAFRAME                 ##########################
##############################################################
if df.empty:
    st.write ('#### No hay datos para este cultivo y en este año.')
    st.write ('#### Selecciona otros valores en el menú izquierdo')
    st.stop()

##############################################################
### SHOW DATA FROM DATAFRAMES       ##########################
##############################################################

# mean prices by autonomous community

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
    st.write (" Si la región aparece en blanco es porque no hay datos de ella.")
    map = map_mean_price_pr (df)
    st.pyplot (map)


# local prices by province

st.markdown ('<hr>', unsafe_allow_html=True)
st.subheader (f'Consulta el precio en tu región - {crop}')
st.write ("Formulario para comunidad y provincia y que de un listado en df con los municipios y el precio, sólo los no nulos")

col8, col9, col10 = st.columns ([1,0.1, 2])

with col8:

    df_mun = pd.read_csv('data/municipios.csv', header=0, index_col=0, delimiter=';')
    df_mun = df_mun.loc[(df_mun['Autonomía'] != 'Ceuta (Ciudad de)') & (df_mun['Autonomía'] != 'Melilla (Ciudad de)')]

    list_com_auton = df_mun['Autonomía'].unique()
    list_com_auton.sort()
    com_auton = st.selectbox('Selecciona la Comunidad Autónoma:', list_com_auton, index=0)

    list_provinces = df_mun['Provincia'][df_mun['Autonomía'] == com_auton].unique()
    province = st.selectbox('Selecciona una Provincia:', list_provinces, index=0)

with col9:
    st.empty ()

with col10:

    st.write('##')
    df_local = df.copy()

    # rename columns
    df_local = df_local.rename (columns={
        'provincia': 'Provincia',
        'municipio': 'Municipio',
        'precio': 'Precio',
        'anio': 'Año',
        'comunidad': 'Autonomía',
        'ecologico': 'Cultivo Eco',
        'variedad': 'Variedad' })

    # reorder columns need to strip the values from the database as they come with blank spaces
    df_local = df_local [['Autonomía', 'Provincia', 'Municipio', 'Año', 'Precio', 'Cultivo Eco', 'Variedad']]
    df_local = df_local.drop('Autonomía',axis=1)
    df_local = df_local.loc[(df_local['Provincia'].str.rstrip () == province) ]
    if df_local.empty:
        st.write ('No hay datos para esta región en este año.')
    else:
        st.dataframe(df_local)