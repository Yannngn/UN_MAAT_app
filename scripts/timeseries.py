import pandas as pd
import plotly.express as px

from colors import COLORS, COLOR_SECTOR, COLOR_STATE
from macro_dict import MACRO, STATES, SECTORS

DATA = r'data\sectors_state.csv'
STACKED = r'data\stacked_data.csv'
STATES_BORDERS = r'data\EstadosBR_IBGE_LLWGS84.shp'

def update(fig):
    fig.update_layout(
        plot_bgcolor=COLORS['background'],
        paper_bgcolor=COLORS['background'],
        font_color=COLORS['text'],
        xaxis_rangeselector_activecolor=COLORS['box'],
        xaxis_rangeselector_bgcolor=COLORS['background'],
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                        label="1 Year",
                        step="year",
                        stepmode="backward"),
                    dict(count=10,
                        label="10 Years",
                        step="year",
                        stepmode="backward"),
                    dict(step="all",
                         label="All",)
                ]),
            ),
            rangeslider=dict(
                visible=True,
            ),
            type="date"
        )
    )
    return fig

def setor_ano():
    stack_data = pd.read_csv(STACKED)
    stack_data.columns = ['State', 'Sector', 'Year', 'CO2']
    sector_re = {v: k for k, v in SECTORS.items()}
    stack_data.Sector = [sector_re[s] for s in stack_data.Sector]

    temp = stack_data.groupby(['Sector', 'Year']).sum(numeric_only=False).reset_index()
    temp['Year'] = pd.to_datetime(temp.Year, format="%Y")
    
    fig = px.line(temp, x='Year', y='CO2', color='Sector',
                  color_discrete_map=COLOR_SECTOR)

    temp = stack_data.groupby(['Year']).sum(numeric_only=False).reset_index()
    temp['Year'] = pd.to_datetime(temp.Year, format="%Y")
    
    fig.add_scatter(x=temp['Year'], y=temp['CO2'], name='Total', 
                    line={'color':'#F0F0F0'}, cliponaxis=True)
    
    return update(fig)

def estado_ano(regiao='All'):
    stack_data = pd.read_csv(STACKED)
    stack_data.columns = ['State', 'Sector', 'Year', 'CO2']
    sector_re = {v: k for k, v in SECTORS.items()}
    stack_data.Sector = [sector_re[s] for s in stack_data.Sector]
    temp = stack_data.groupby(['State','Year']).sum(numeric_only=False).reset_index()
    
    
    if regiao != 'All':
        estados = MACRO[regiao]
        temp = temp[[estado in estados for estado in temp.State]]
    
    fig = px.line(temp, x='Year', y='CO2', color='State', 
                  color_discrete_map=COLOR_STATE)
    
    # temp = stack_data.groupby(['Ano']).sum().reset_index()
    # fig.add_scatter(x=temp['Ano'], y=temp['CO2'], name='Total', 
    #                 line={'color':'#F0F0F0'}, cliponaxis=True)

    return update(fig)

def estado_isolado_ano(estado=None):
    stack_data = pd.read_csv(STACKED)
    stack_data.columns = ['State', 'Sector', 'Year', 'CO2']
    sector_re = {v: k for k, v in SECTORS.items()}
    stack_data.Sector = [sector_re[s] for s in stack_data.Sector]
    temp = stack_data#stack_data.groupby(['Estado','Ano']).sum().reset_index()
    
    dict_re = {v: k for k, v in STATES.items()}

    temp = temp[temp.State == dict_re[estado]]
    
    fig = px.line(temp, x='Year', y='CO2', color='Sector', 
                  color_discrete_map=COLOR_STATE)
    
    # temp = stack_data.groupby(['Ano']).sum().reset_index()
    # fig.add_scatter(x=temp['Ano'], y=temp['CO2'], name='Total', 
    #                 line={'color':'#F0F0F0'}, cliponaxis=True)

    return update(fig)