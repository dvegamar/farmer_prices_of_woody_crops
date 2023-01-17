# this script will connect to the database and query for all the data in each cropfrom sqlalchemy import create_engine
# pandas only supports SQLAlchemy connectable (engine/connection)
import pandas as pd
from sqlalchemy import create_engine


def retrieve (crop_t):

    engine = create_engine ('postgresql://dvega:dvega123@127.0.0.1:5432/olivares')
    table_name = crop_t
    df = pd.read_sql_table(table_name, engine)
    return df


