# this script will connect to the database and query for all the data in each cropfrom sqlalchemy import create_engine
# pandas only supports SQLAlchemy connectable (engine/connection)
import streamlit as st
from sqlalchemy import create_engine
import pandas as pd

# Load the service account JSON
service_account = st.secrets["postgres_olivares"]

# Create the connection string
connection_string = "postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}".format(
    username=service_account["username"],
    password=service_account["password"],
    host=service_account["host"],
    port=service_account["port"],
    database=service_account["database"]
)

# Create the engine
@st.experimental_memo(ttl=600)
def retrieve (crop_t):

    engine = create_engine (connection_string)
    table_name = crop_t
    df = pd.read_sql_table(table_name, engine)
    return df




# for local
'''
def retrieve (crop_t):

    engine = create_engine ('postgresql://dvegamar:dvega123@127.0.0.1:5432/olivares')
    table_name = crop_t
    df = pd.read_sql_table(table_name, engine)
    return df
'''

