# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px

from colors import COLORS
from macro_dict import *

from scripts.bar_states import estados_setores
from scripts.timeseries import setor_ano, estado_ano, estado_isolado_ano
from scripts.map import mapa_brasil

app = Dash(__name__)

app.layout = html.Div(children=[
    html.Div(className="app-header",
        children=[
            html.Div(children=[html.H1(children='United Nations Hackaton')],
                     className="app-header--title",
                     style={'textAlign': 'center',
                            }),
            html.Div(html.H2(children='''Dash: Visualization.'''),
                     className='app-header--subtitle',
                     style={'textAlign': 'center',
                            }),
        ]
    ),
   
    html.Div(children=[
        html.H3(children='''CO2 Emission in Billions of Tons per year''',
             style={'textAlign': 'left',
                    'margin-left': '20px',
                    'color': COLORS['text']}),]),
    
    html.Div(children=[
        html.H4(children='''Per Sector''',
             style={'textAlign': 'left',
                    'margin-left': '20px',
                    'color': COLORS['text']}),
        dcc.Graph(id='CO2 Emission per Year',
                  figure=setor_ano()
                  ),
        html.Div(style={'width': '80%',
                        'textAlign': 'left',                         
                        'margin-left': '80px',},
                 children=[
                     html.B('''On national level, we observed a peak on CO2 emissions in 2003-2004, followed by a quick drop until 2010, when the number hit its lowest figure. Since then, we've observed a rising trend in these numbers, with a sharp rise from 2011-2013 and another one on last observed year, 2021.''',
                     style={'color': COLORS['text']})
            ])
        ]),
    
    html.Div(children=[
        html.H4(children='''Per Region''',
             style={'textAlign': 'left',
                    'margin-left': '20px',
                    'color': COLORS['text']}),
        html.Div(children=[
                    dcc.Dropdown(list(MACRO.keys()), 
                                'North', 
                                id='region-dropdown-time',
                                style={"width": "50%",
                                        'margin-left': '20px',
                                        }),
                    html.Div(id='dd-output-container-time'),],      
        ),
        html.Div(style={'width': '80%',
                'textAlign': 'left',                         
                'margin-left': '80px',},
            children=[
                html.B('''Analyzing by macrorregions, we noticed that, until 2009 the North and Center-West regions varied similarly to the national numbers, being the two main contributors. However, the same pattern is not seen in the most recent spike. In the past years, the Center-West has stalled their emissions, losing the second place in most emissions to the Southeast region for a few years, while the North has increased their participation and became the the biggest source of emission by far.''',
                style={'color': COLORS['text']})
            ])
    ]),

    html.Div(children=[
        html.H5(children='''Per State''',
             style={'textAlign': 'left',
                    'margin-left': '20px',
                    'color': COLORS['text']}),
        dcc.Dropdown(list(STATES.values()), 
                    'Pará', 
                    id='region-dropdown-state',
                    style={"width": "50%",
                            'margin-left': '40px',
                            }),
        html.Div(id='dd-output-container-state'),
                html.Div(style={'width': '80%',
                        'textAlign': 'left',                         
                        'margin-left': '80px',
                        'color': COLORS['text'],},
                 children=[
                     html.B('''
                            When we take a look at the states, we can make a few observations:
                            '''),
                     html.Ul([
                        html.Li('''
                                Northeast: Maranhão (MA) had a sharp rise in emissions in the past year, way above all other states. In fact, the other states appear to be on a downward trend or stable. 
                                '''),
                        html.Li('''
                                South: That was another region that caught our attention, given that all three states presented big rises in emissions in the past year. 
                                '''),

                        html.Li('''
                                Center-West: In this graph, we can see Brazil's former main pollutor, Mato Grosso. It is notable that, after terrible years during Brazil's peak deforestation, during 2003 and 2004, MT has decreased its emissions by around 80% and, even though it has shown a rising trend, it has not increased its levels in the same rhythm as the National numbers, indicating that it'is not one of the main contributors to the rise as it was in the beggining of the decade, although it still represents a big part of Brazil's emissions. 
                                '''),
                        html.Li('''
                                North: Amazonas (AM) and Roraima (RR) show a positive trend in emissions in the past years. But the main problem here is Pará. It emissions are trending upwards since 2011 and, as the second biggest contributor among states, seems to be the driving force behind Brazil's worsening numbers. 
                                '''),]),
                     ]),
        ],
         
    ),
    
    html.Div(children=[
        html.H4('''KEY STATES''',
                style={'textAlign': 'left',
                    'margin-left': '20px',
                    'color': COLORS['text']}),
        html.Div(style={'width': '80%',
                                'textAlign': 'left',                         
                                'margin-left': '80px',
                                'color': COLORS['text'],},
                 children=[
                     html.Ul([
                         html.Li('''
                                 Pará: It would be important to focus our effort of reducing emissions in Pará, given that it is now responsible for 20% of all national emissions, a number that has been constantly rising throughout the past decade. 
                                 '''),]),]),]),    

    html.Div(children=[
        html.H4(children='''Brasil HeatMap''',
                style={'textAlign': 'left',
                    'margin-left': '20px',
                    'color': COLORS['text']}),
        
        dcc.Dropdown(list(SECTORS.keys()),
                     list(SECTORS.keys())[2], 
                     id='region-dropdown-map',
                     style={"width": "50%",
                            'margin-left': '20px',
                            }),
        html.Div(id='dd-output-container-map'),],
             
    ),
    
    html.Div(children=[
        html.H4(children='''Per State [All Years]''',
                style={'textAlign': 'left',
                    'margin-left': '20px',
                    'color': COLORS['text']}),
        dcc.Dropdown(list(MACRO.keys())+['All'],
                     'All', 
                     id='region-dropdown-sector',
                     style={"width": "50%",
                            'margin-left': '20px',
                            }),
        html.Div(id='dd-output-container-sector'),],
             
    ),
])

@app.callback(
    Output('dd-output-container-time', 'children'),
    Input('region-dropdown-time', 'value')
    )
def update_estado_ano(value):
    return dcc.Graph(
        id='CO2 Emission per State per Year',
        figure=estado_ano(value)
    )

@app.callback(
    Output('dd-output-container-state', 'children'),
    Input('region-dropdown-state', 'value')
    )
def update_estado_isolado_ano(value):
    return dcc.Graph(
        id='CO2 Emission per State per Year',
        figure=estado_isolado_ano(value)
    )

@app.callback(
    Output('dd-output-container-sector', 'children'),
    Input('region-dropdown-sector', 'value')
    )
def update_estados_setores(value):
    return dcc.Graph(
        id='CO2 Emission per State per Sector',
        figure=estados_setores(value)
    )
     
@app.callback(
    Output('dd-output-container-map', 'children'),
    Input('region-dropdown-map', 'value')
    )
def update_mapa_brasil(value):
    return dcc.Graph(
        id='Brazil Heatmap',
        figure=mapa_brasil(value)
    )

if __name__ == '__main__':
    app.run_server(debug=True)