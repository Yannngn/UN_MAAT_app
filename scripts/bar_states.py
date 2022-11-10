import pandas as pd
import plotly.express as px

from colors import COLORS, COLOR_SECTOR
from macro_dict import MACRO

DATA = r'data\sectors_state.csv'
STACKED = r'data\stacked_data.csv'
STATES_BORDERS = r'data\EstadosBR_IBGE_LLWGS84.shp'

def get_data():
    data = pd.read_csv(DATA, index_col='Unnamed: 0')
    data.columns = ['Setor'] + list(data.columns[1:])
    data = data.groupby(['Setor', 'Estado']).sum(numeric_only=False).reset_index()
    data['Geral'] = data[data.columns[2:34]].sum(axis=1,numeric_only=False)
    
    return data

def update(fig):
    fig.update_layout(
        plot_bgcolor=COLORS['background'],
        paper_bgcolor=COLORS['background'],
        font_color=COLORS['text'],
        
    )
    return fig


def estados_setores(regiao='All'):
    data = get_data()
    
    df = data[['Setor', 'Estado', 'Geral']]
    df.columns = ['Sector', 'State', 'CO2']
    temp = df.groupby(['State', 'Sector']).sum(numeric_only=False).reset_index()
    if regiao != 'All':
        estados = MACRO[regiao]
        temp = temp[[estado in estados for estado in temp.State]]
    fig = px.bar(temp, x='State', y='CO2', color='Sector', color_discrete_map=COLOR_SECTOR)

    return update(fig)
