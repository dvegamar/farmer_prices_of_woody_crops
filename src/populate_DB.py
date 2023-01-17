# script to populate the three tables in the database with random values
import numpy as np
import psycopg2
import pandas as pd
import random


conexion = psycopg2.connect (
        user='dvega',
        password='dvega123',
        host='127.0.0.1',
        port='5432',
        database='olivares')
cursor = conexion.cursor ()


## generate variables

df_mun = pd.read_csv('./data/municipios.csv', header=0, index_col=0, delimiter=';')
df_mun = df_mun.loc[(df_mun['Autonomía'] != 'Ceuta (Ciudad de)') & (df_mun['Autonomía'] != 'Melilla (Ciudad de)')]
list_years = [2021]


for i in range(120):

    list_com_auton = df_mun['Autonomía'].unique()
    com_auton = random.choice(list_com_auton)
    list_provinces = df_mun['Provincia'][df_mun['Autonomía'] == com_auton].unique()
    province = random.choice(list_provinces)
    list_municip = df_mun['Municipio'][df_mun['Provincia'] == province].unique()
    municipality = random.choice(list_municip)

    year = random.choice(list_years)

    '''# populate olivares_t
    price_oli = round(random.uniform(0.25,1.00),2)
    variety_oli = random.choice(['Cornicabra', 'Picual', 'Manzanilla', 'Hojiblanca'])
    booleans = [True,False]
    weights =[0.1,0.9]
    verdeo = random.choices(booleans,weights)[0]
    ecologico_oli = random.choices(booleans,weights)[0]
    print(municipality,price_oli,variety_oli,verdeo,ecologico_oli)
    variables = (com_auton, province, municipality, year, price_oli, variety_oli,verdeo,ecologico_oli)
    sentencia = "INSERT INTO olivares_t (comunidad,provincia,municipio,anio,precio,variedad,verdeo,ecologico) " \
                        "VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"'''

    '''# populate pistachos_t
    price_pis = round (random.uniform (1.00, 10.00), 2)
    variety_pis = random.choice (['Kerman', 'Silora', 'Aegina', 'Larnaka'])
    booleans = [True, False]
    weights = [0.2, 0.9]
    cerrado = random.choices (booleans, weights) [0]
    ecologico_pis = random.choices (booleans, weights) [0]
    variables = (com_auton, province, municipality, year, price_pis, variety_pis, cerrado, ecologico_pis)
    sentencia = "INSERT INTO pistachos_t (comunidad,provincia,municipio,anio,precio,variedad,cerrado,ecologico) " \
                "VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"'''

    '''# populate uvas_t
    price_gra = round (random.uniform (0.20, 7.00), 2)
    variety_gra = random.choice (['Granacha', 'Tempranillo', 'Mencía', 'Monastrell','Airén','Malvar'])
    booleans = [True, False]
    weights = [0.1, 0.9]
    mesa = random.choices (booleans, weights) [0]
    ecologico_gra = random.choices (booleans, weights) [0]
    variables = (com_auton, province, municipality, year, price_gra, variety_gra, mesa, ecologico_gra)
    sentencia = "INSERT INTO uvas_t (comunidad,provincia,municipio,anio,precio,variedad,mesa,ecologico) " \
                "VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"'''


    try:
        cursor.execute (sentencia, variables)
        registros_insertados = cursor.rowcount
        print ('Se han insertado los registros:  ', registros_insertados)
    except psycopg2.Error as e:
        print ('Algo ha ido mal al insertar los datos', e)

conexion.commit ()
cursor.close ()
conexion.close ()