import plotly.graph_objs as go

def plot_mean_price_ca(df,year):
    # Get the dataframe and create a new one for plotly
    df = df.loc [df ['anio'].isin(year)]
    df_mean_price = df.groupby("comunidad").mean()["precio"].sort_values(ascending=False)
    # Create a horizontal bar graph
    fig = go.Figure(data=[go.Bar(x=df_mean_price.values,
                                 y=df_mean_price.index,
                                 orientation='h'
                                 )])
    # Set the color scale
    fig.update_layout(xaxis=dict(title='Precio medio del Kg por Comunidad Autónoma en Euros'),
                      yaxis=dict(
                          position=0,
                          tickfont=dict(color='#292828'),
                          side='left'),
                      barmode='group',
                      bargap=0.,
                      bargroupgap=0.2,
                      margin=dict(l=5,
                                  r=50,
                                  t=30,
                                  b=20),
                      showlegend=False,
                      )

    fig.update_traces (marker=dict (color=df_mean_price.tolist()))
    fig.update_traces (marker_colorscale='viridis')
    return fig


'''
def plot_mean_price_pr(df):
    # aqui no van barras, va una tabla dataframe con colores si puede ser'''