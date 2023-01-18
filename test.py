from src.retrieve_from_db import retrieve
import pandas as pd
pd.set_option('display.max_columns', 20)



year=[2002]
df = retrieve ('olivares_t')

print(df.head(10))

df = df.loc [df ['anio'].isin(year)]

print(df.head(10))



df_local = df.copy()
df_local = df_local.loc[(df['provincia'] == 'Teruel')]
# df_local = df.loc[(df['comunidad'] == com_auton) & (df['provincia'] == province) & (df['anio'] == year)]

