import pandas as pd
import plotly.express as px

COLORS = {
    'background': '#1F1F1F',
    'box': '#2F2F2F',
    'text': '#7FDBFF'
}

DATA = r'data\sectors_state.csv'
STACKED = r'data\stacked_data.csv'
STATES_BORDERS = r'data\EstadosBR_IBGE_LLWGS84.shp'

data = pd.read_csv(DATA, index_col='Unnamed: 0')
data.columns = ['Setor'] + list(data.columns[1:])
data = data.groupby(['Setor', 'Estado']).sum().reset_index()
data['Geral'] = data[data.columns[2:34]].sum(axis=1)

setores = data.Setor.unique()

COLOR_SECTOR = {k: v for k, v in \
             zip(setores, px.colors.sample_colorscale(px.colors.qualitative.Plotly_r, 
                                                      [n/(len(setores)-1) for n in range(len(setores))]
                                                      )
                 )
             }

estados = data.Estado.unique()

COLOR_STATE = {k: v for k, v in \
             zip(estados, px.colors.sample_colorscale(px.colors.qualitative.Plotly_r, 
                                                      [n/(len(estados)-1) for n in range(len(estados))]
                                                      )
                 )
             }