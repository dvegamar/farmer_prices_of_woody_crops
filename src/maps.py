import geopandas as gpd
import pandas as pd
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.pyplot as plt


# this funcion plots a map with the mean prices of the crop
def map_mean_price_ca(df):

    # get the mean values of price por autonomous community, this is a pandas series where the index is comunidad
    # the groupby adds a few blank spaces at the end of the index value, so need to strip, otherway wont merge
    series_mean_price = df.groupby ("comunidad").mean (numeric_only=True) ["precio"]
    series_mean_price.index = series_mean_price.index.str.rstrip ()

    # convert the series to a dataframe and reset index to get a new column with the index names = communities
    df_mean_price = pd.DataFrame (series_mean_price).reset_index ()

    # load the shp file with autonomous communities shapes, remove all but geometry and comunidad
    map_data = gpd.read_file ('geo/gadm36_ESP_1.shp')
    map_data = map_data.loc [:,['NAME_1','geometry']]
    map_data = map_data.rename (columns={'NAME_1': 'comunidad'})
    map_data = map_data.loc [(map_data ['comunidad'] != 'Ceuta y Melilla')]



    # change the names of the autonomous communities map_data to match the names of df_mean_price
    map_data ['comunidad'] = map_data ['comunidad'].replace (
        {'Comunidad de Madrid': 'Madrid (Comunidad de)',
         'Comunidad Foral de Navarra': 'Navarra (Comunidad Foral de)',
         'Islas Baleares': 'Balears (Illes)',
         'Islas Canarias': 'Canarias)',
         'La Rioja': 'Rioja (La)',
         'Principado de Asturias': 'Asturias (Principado de)',
         'Región de Murcia': 'Murcia (Región de)'
         })
    map_data = map_data.sort_values (by='comunidad').reset_index ()

    # merge the geometry dataframe with the prices dataframe
    merged_data = map_data.merge (df_mean_price, on='comunidad', how='inner')

    # generate the map
    fig, ax = plt.subplots (figsize=(10,10))
    ax.axis ([-9.9, 5, 35.5, 44.5]) # line not valid for all crops except vines, as the canary islands has this crop
    ax.tick_params (left=False, right=False, labelleft=False,
                     labelbottom=False, bottom=False)
    ax.patch.set_alpha (0.2)
    fig.patch.set_alpha (0.0)

    # Separated legend
    divider = make_axes_locatable (ax)
    cax = divider.append_axes ("right", size="5%", pad=0.2)

    merged_data.plot (column='precio', cmap='viridis', ax=ax, legend=True, cax=cax)

    return fig


def map_mean_price_pr(df):

    # get the mean values of price por autonomous community, this is a pandas series where the index is province
    # the groupby adds a few blank spaces at the end of the index value, so need to strip, otherway wont merge
    series_mean_price = df.groupby ("provincia").mean (numeric_only=True) ["precio"]
    series_mean_price.index = series_mean_price.index.str.rstrip ()

    # convert the series to a dataframe and reset index to get a new column with the index names = communities
    df_mean_price = pd.DataFrame (series_mean_price).reset_index ()

    # load the shp file with provinces shapes, remove all but geometry and province
    map_data = gpd.read_file ('geo/gadm36_ESP_2.shp')
    map_data = map_data.loc [:, ['NAME_2', 'geometry']]
    map_data = map_data.rename (columns={'NAME_2': 'provincia'})
    map_data = map_data.loc [~map_data ['provincia'].isin (['Ceuta', 'Melilla'])]
    map_data ['provincia'] = map_data ['provincia'].replace (
        {'Álava': 'Araba/Álava',
         'Vizcaya': 'Bizkaia',
         'Baleares': 'Balears (Illes)',
         'Guipúzcoa': 'Gipuzkoa',
         'La Rioja': 'Rioja (La)',
         'Las Palmas': 'Palmas (Las)',
         'A Coruña': 'Coruña (A)',
         'Castellón': 'Castellón/Castelló',
         'Alicante': 'Alicante/Alacant',
         'Valencia': 'Valencia/València',
         })

    map_data = map_data.sort_values (by='provincia').reset_index ()

    # merge the geometry dataframe with the prices dataframe
    merged_data = map_data.merge (df_mean_price, on='provincia', how='inner')

    # generate the map
    fig, ax = plt.subplots (figsize=(10,10))
    ax.axis ([-9.9, 5, 35.5, 44.5]) # line not valid for all crops except vines, as the canary islands has this crop
    ax.tick_params (left=False, right=False, labelleft=False,
                     labelbottom=False, bottom=False)
    ax.patch.set_alpha (0.2)
    fig.patch.set_alpha (0.0)

    # Separated legend
    divider = make_axes_locatable (ax)
    cax = divider.append_axes ("right", size="5%", pad=0.2)

    merged_data.plot (column='precio', cmap='viridis', ax=ax, legend=True, cax=cax)

    return fig