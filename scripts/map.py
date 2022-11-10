import folium
import pandas as pd
import geopandas as gpd
import plotly.express as px
import json

DATA = r'data\sectors_state.csv'
STACKED = r'data\stacked_data.csv'
STATES_BORDERS = r'data\EstadosBR_IBGE_LLWGS84.shp'

from macro_dict import SECTORS
from colors import COLORS

def update(fig):

    return fig

def get_data():
    data = pd.read_csv(DATA, index_col='Unnamed: 0')
    data.columns = ['Setor'] + list(data.columns[1:])
    data = data.groupby(['Setor', 'Estado']).sum(numeric_only=False).reset_index()
    data['Geral'] = data[data.columns[2:34]].sum(axis=1,numeric_only=False)
    
    return data

def get_geo_data():
    #stack_data = pd.read_csv(STACKED)
    estados_borders = gpd.read_file(STATES_BORDERS)
    estados_borders['State'] = estados_borders.ESTADO
    estados_borders = estados_borders.drop(columns=['object_id_', 'agreount_', 'ESTADO'])

    #stack_data = pd.merge(left=stack_data, right=estados_borders, on=['Estado'])
    
    return estados_borders.to_json()


def mapa_brasil(sector):
    stack_data = pd.read_csv(STACKED)
    stack_data.columns = ['State', 'Sector', 'Year', 'CO2']
    geo_j = get_geo_data()
    j = json.loads(geo_j)
    
    crange = (stack_data['CO2'].quantile((0, 1))).tolist()
    
    m = px.choropleth(stack_data[stack_data.Sector == SECTORS[sector]],               
                  geojson=j,
                  locations='State',
                  featureidkey="properties.State",         
                  color="CO2",
                  hover_name="State",  
                  animation_frame="Year",
                  range_color=crange,
                  color_continuous_scale='viridis')
    
    m.update_geos(fitbounds="locations", visible=True)
    m.update_layout(
        plot_bgcolor=COLORS['background'],
        paper_bgcolor=COLORS['background'],
        font_color=COLORS['text'],
        margin={"r":0,"t":0,"l":0,"b":0}      
    )
    return m

def pesado_mapa_brasil():
    data = get_data()
    custom_scale = (data['Geral'].quantile((0, .2, .4, .6, .8, 1))).tolist()
    df = data[['Setor', 'Estado', 'Geral']]
    
    geo_j = get_geo_data()
    br_map = folium.Map(location=[-3.11, -60], zoom_start=6,name="Open Street Map")

    figures = [folium.FeatureGroup(name=setor,
                                overlay=True, 
                                show=False).add_to(br_map)
            for setor in data.Setor.unique().tolist()]

    layers = [folium.Choropleth(geo_data=geo_j,
                                data=df[df.Setor == setor],
                                columns=['Estado', 'Geral'],
                                key_on='feature.properties.Estado',
                                threshold_scale=custom_scale,
                                fill_color='YlOrRd',
                                nan_fill_color="White",
                                fill_opacity=0.7,
                                line_opacity=0.2,
                                legend_name=setor,
                                highlight=True,
                                overlay=False,
                                line_color='black').geojson.add_to(figure)
            for figure, setor in zip(figures, data.Setor.unique().tolist())]

    #folium.TileLayer(overlay=False,name="Open Street Map").add_to(br_map)
    folium.TileLayer('Stamen Terrain',overlay=False,name="Terrain").add_to(br_map)
    folium.LayerControl(collapsed=False).add_to(br_map)

    return br_map