import streamlit as st
import pandas as pd
import psycopg2


##############################################################
### PAGE SETTINGS  ###########################################
##############################################################

st.set_page_config(page_title="Precios de las aceitunas - Nuevos datos", layout="wide")
st.header('Introduce nuevos datos')
st.subheader('Rellena el formulario para compartir nuevos datos en la plataforma')

# hide menu and footer from streamlit
hide_menu_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """
st.markdown (hide_menu_style, unsafe_allow_html=True)

##############################################################
### FORM LOCATION  ###########################################
##############################################################

df_mun = pd.read_csv('data/municipios.csv', header=0, index_col=0, delimiter=';')
df_mun = df_mun.loc[(df_mun['Autonomía'] != 'Ceuta (Ciudad de)') & (df_mun['Autonomía'] != 'Melilla (Ciudad de)')]

list_years = [2018,2019,2020,2021,2022,2023,2024]

list_com_auton = df_mun['Autonomía'].unique()
list_com_auton.sort()
com_auton = st.selectbox('Selecciona la Comunidad Autónoma:', list_com_auton, index=0)

list_provinces = df_mun['Provincia'][df_mun['Autonomía'] == com_auton].unique()
province = st.selectbox('Selecciona una Provincia:', list_provinces, index=0)

list_municip = df_mun['Municipio'][df_mun['Provincia'] == province]
municipality = st.selectbox('Selecciona un municipio:', list_municip, index=0)

year = st.selectbox('Selecciona el año de la campaña:', list_years, index=4)

##############################################################
### SPLIT IN COLUMNS    ######################################
##############################################################
col1,col2,col3 = st.columns([1,1,1])

##############################################################
### FORM OLIVES    ###########################################
##############################################################

with col1:

    st.write('### Aceitunas')
    price_oli = st.slider ('Precio del Kg de aceituna al agricultor en euros', min_value=0.00, max_value=2.00, step=0.01, value=0.50)
    variety_oli = st.text_input ("Variedad de aceituna:", max_chars=30)
    verdeo = st.checkbox ('Marca esta casilla si aceituna de mesa')
    ecologico_oli = st.checkbox ('Marca esta casilla si es olivar ecológico')

##############################################################
### FORM PISTACHIO ###########################################
##############################################################

with col2:
    st.write ('### Pistachos')
    price_pis = st.slider ('Precio del Kg de pistacho al agricultor en euros', min_value=0.00, max_value=10.00, step=0.01, value=2.00)
    variety_pis = st.text_input ("Variedad de pistacho:", max_chars=30)
    cerrado = st.checkbox ('Marca esta casilla si pistacho cerrado')
    ecologico_pis = st.checkbox ('Marca esta casilla si es pistacho ecológico')


##############################################################
### FORM VINES     ###########################################
##############################################################

with col3:
    st.write ('### Uvas')
    price_gra = st.slider ('Precio del Kg de uva al agricultor en euros', min_value=0.00, max_value=10.00, step=0.01, value=1.00)
    variety_gra = st.text_input ("Variedad de uva:", max_chars=30)
    mesa = st.checkbox ('Marca esta casilla si es uva de mesa')
    ecologico_gra = st.checkbox ('Marca esta casilla si es uva ecológica')



##############################################################
### DATABASE UPDATE FUNCTION         #########################
##############################################################

def insert_data(variables,sentencia):

    conexion = psycopg2.connect (
        user='dvega',
        password='dvega123',
        host='127.0.0.1',
        port='5432',
        database='olivares')
    cursor = conexion.cursor ()

    try:
        cursor.execute (sentencia, variables)
        registros_insertados = cursor.rowcount
        st.write ('Se han insertado los registros:  ', registros_insertados)
    except psycopg2.Error as e:
        st.write ('Algo ha ido mal al insertar los datos', e)

    conexion.commit ()
    cursor.close ()
    conexion.close ()

##############################################################
### UPDATES PER CROP                 #########################
##############################################################

with col1:
    enviar_oli = st.button('Enviar nuevos datos olivar')
    if enviar_oli:
        variables = (com_auton, province, municipality, year, price_oli, variety_oli,verdeo,ecologico_oli)
        sentencia = "INSERT INTO olivares_t (comunidad,provincia,municipio,anio,precio,variedad,verdeo,ecologico) " \
                    "VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        insert_data (variables,sentencia)

with col2:
    enviar_pis = st.button('Enviar nuevos datos pistachos')
    if enviar_pis:
        variables = (com_auton, province, municipality, year, price_pis, variety_pis, cerrado, ecologico_pis)
        sentencia = "INSERT INTO pistachos_t (comunidad,provincia,municipio,anio,precio,variedad,cerrado,ecologico) " \
                    "VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        insert_data (variables,sentencia)

with col3:
    enviar_gra = st.button('Enviar nuevos datos uvas')
    if enviar_gra:
        variables = (com_auton, province, municipality, year, price_gra, variety_gra, mesa, ecologico_gra)
        sentencia = "INSERT INTO uvas_t (comunidad,provincia,municipio,anio,precio,variedad,mesa,ecologico) " \
                    "VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        insert_data (variables,sentencia)