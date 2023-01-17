import streamlit as st
import pandas as pd

# To style the dataframe:  https://pandas.pydata.org/docs/reference/api/pandas.io.formats.style.Styler.html
# but many styles do not work in streamlit, backgrounds work, but font styles dont with set properties, or other sytles
# so text formatting is nearly impossible

def table_price_pr(df):

    series_mean_price = df.groupby ("provincia").mean () ["precio"].sort_values (ascending=False)
    df_mean_price = pd.DataFrame (series_mean_price).reset_index ().sort_values (by='provincia')

    df_mean_price.rename (columns={'provincia': 'Provincia', 'precio': 'Precio    ', 'index':'Orden'}, inplace=True)

    return st.dataframe (df_mean_price.style.
                  background_gradient (axis=0, gmap=df_mean_price ['Precio    '], cmap='viridis').
                  format (subset=['Precio    '], precision=2)
                  )