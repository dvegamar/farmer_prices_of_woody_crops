import geopandas as gpd
import pandas as pd
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.pyplot as plt
from src.retrieve_from_db import retrieve


# get the mean values of price por autonomous community, this is a pandas series where the index is province

df = retrieve ('uvas_t')
series_mean_price = df.groupby ("provincia").mean (numeric_only=True) ["precio"]
# convert the series to a dataframe and reset index to get a new column with the index names = communities
df_mean_price = pd.DataFrame (series_mean_price).reset_index ()

print(df_mean_price.head(50))

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
     'A Coruña': 'Coruña (La)'
     })

map_data = map_data.sort_values (by='provincia').reset_index ()

# merge the geometry dataframe with the prices dataframe
merged_data = map_data.merge (df_mean_price,  left_index=True, right_index=True)

print(merged_data.head(50))
