import dash
import dash_auth
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash_html_components.Hr import Hr
import dash_table 
from getKoboData import GetKoboData
from dash.dependencies import Input, Output, State
#from getKoboData import GetKoboData
import numpy as np
import pandas as pd
from plotly.offline import iplot 
import plotly as py
import cufflinks as cf 
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from plotly.subplots import make_subplots
import folium
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import random
from datetime import timedelta
import warnings

warnings.filterwarnings('ignore')
#color palette
cnf='#393e46'
dth='#ff2e63'
rec='#21bf73'
act='#fe9801'
import plotly.express as px

#definition des controls
# the style arguments for the sidebar.

# fig.add_trace(go.Scatter(x=confirmed['Date'],y=confirmed['Confirmed'] ,mode='lines',name="confirmed",line=dict(color="Orange",width=4)))
# fig.add_trace(go.Scatter(x=recovered['Date'],y=recovered['Recovered'] ,mode='lines',name="Recovered",line=dict(color="Green",width=4)))
# fig.add_trace(go.Scatter(x=deaths['Date'],y=deaths['Deaths'] ,mode='lines',name="Deaths",line=dict(color="Red",width=4)))
# fig.update_layout(title='wordwide covid-19 caes ' ,xaxis_tickfont_size=14,yaxis=dict(title='Number of cases '))
# fig.show()

kobdata=GetKoboData()
labeld_results=kobdata.getAllData()
print(labeld_results)
df1=kobdata.getDapsDataFrame(labeld_results)
df1.rename(columns={'Quel est le statut de votre structure  ?':'statut'}, inplace=True)

df_medaille=df1.groupby(['Quel est le nom de votre structure','statut'])[["Combien de médailles d'or avez-vous gagné niveau international","Combien de médailles d'or avez-vous gagné par les femmes niveau international","Combien de médailles d'or avez-vous gagné par les hommes niveau international"]].sum().reset_index()

count_statut=df1['statut'].value_counts(sort=True, ascending=True)
test1=df1['Le nombre de femmes actives élèves arbitres'].sum()
nbre=int(test1[-1])
df1.rename(columns={"Date d’interview(jj/mm/aa) ":'Date'}, inplace=True)
df1.rename(columns={'Numero questionnaire ':'nombre enquetes'}, inplace=True)

nbr_enquete_par_jour=df1.groupby("Date").count()['nombre enquetes'].reset_index()
nbr_enquete_par_jour[['Date','nombre enquetes']]

fig2 = px.bar(nbr_enquete_par_jour, x='Date', y='nombre enquetes',color='nombre enquetes',title="Nombre d'enquetes par jour")

fig3=go.Figure()

fig3.add_trace(go.Scatter(x=df_medaille['Quel est le nom de votre structure'],y=df_medaille["Combien de médailles d'or avez-vous gagné niveau international"] ,mode='lines',name="Combien de médailles d'or avez-vous gagné niveau international",line=dict(color="Orange",width=4))),
fig3.add_trace(go.Scatter(x=df_medaille['Quel est le nom de votre structure'],y=df_medaille["Combien de médailles d'or avez-vous gagné par les femmes niveau international"] ,mode='lines',name="Combien de médailles d'or avez-vous gagné par les femmes niveau international",line=dict(color="Green",width=4))),
fig3.add_trace(go.Scatter(x=df_medaille['Quel est le nom de votre structure'],y=df_medaille["Combien de médailles d'or avez-vous gagné par les hommes niveau international"] ,mode='lines',name="Combien de médailles d'or avez-vous gagné par les hommes niveau international",line=dict(color="Red",width=4))),
fig3.update_layout(title='Nombre de medailles gagné par les structures ' ,xaxis_tickfont_size=14,yaxis=dict(title='Nombre de medailles  '))   
section =df1[['Quel est le nom de votre structure','La date de création de votre structure (jj/mm/aa)',"Quelle est la durée de votre mandant (nombre d'années) "]]
fig = px.bar(df1, x="Quel est le nom de votre structure", y="Quel est le nombre de membres dans le comité directeur ?", color="Quel est le nom de votre structure", barmode="group",width=800,title='Nombre de membres dans lee comite directeur')

count_locaux=df1['Votre structure dispose-t-elle de locaux'].value_counts(sort=True, ascending=True).reset_index()
fig4 = px.pie(count_locaux, values='Votre structure dispose-t-elle de locaux',names='index',title='Locaux')



count_sexe=df1['Etes vous'].value_counts(sort=True, ascending=True).reset_index()
fig5 = px.pie(count_sexe, values='Etes vous',names='index',title='Repartition des Sexes')
SIDEBAR_STYLE = {
    'position': 'fixed',
    'top': 0,
    'left': 0,
    'bottom': 0,
    'width': '20%',
    'padding': '20px 10px',
    'background-color': '#1f2c56'
}

# the style arguments for the main content page.
CONTENT_STYLE = {
    'margin-left': '21%',
    'margin-right': '0%',
    'top': 0,
    'padding': '20px 10px',
    'background-color': '#192444'
}

TEXT_STYLE = {
    'textAlign': 'center',
    'color': '#ffffff'
}

CARD_TEXT_STYLE = {
    'textAlign': 'center',
    'color': '#0074D9'
}
# card_container={
#     'border-radius': '5px',
#     'background-color': '#1f2c56',
#     'margin': '25px',
#     'padding': '15px',
#     'position': 'relative',
#     'box-shadow': '2px 2px 2px #1f2c56'
# }
# kobdata=GetKoboData()
# labeld_results=kobdata.getAllData()
# print(labeld_results)
# data=kobdata.getDapsDataFrame(labeld_results)
# print(data.head())
controls = dbc.FormGroup(
    [
        html.P('Dropdown', style={
            'textAlign': 'center'
        }),
        dcc.Dropdown(
            id='dropdown',
            options=[{
                'label': 'Value One',
                'value': 'value1'
            }, {
                'label': 'Value Two',
                'value': 'value2'
            },
                {
                    'label': 'Value Three',
                    'value': 'value3'
                }
            ],
            value=['value1'],  # default value
            multi=True
        ),
        html.Br(),
        html.P('Range Slider', style={
            'textAlign': 'center'
        }),
        dcc.RangeSlider(
            id='range_slider',
            min=0,
            max=20,
            step=0.5,
            value=[5, 15]
        ),
        html.P('Check Box', style={
            'textAlign': 'center'
        }),
        dbc.Card([dbc.Checklist(
            id='check_list',
            options=[{
                'label': 'Value One',
                'value': 'value1'
            },
                {
                    'label': 'Value Two',
                    'value': 'value2'
                },
                {
                    'label': 'Value Three',
                    'value': 'value3'
                }
            ],
            value=['value1', 'value2'],
            inline=True
        )]),
        html.Br(),
        html.P('Radio Items', style={
            'textAlign': 'center'
        }),
        dbc.Card([dbc.RadioItems(
            id='radio_items',
            options=[{
                'label': 'Value One',
                'value': 'value1'
            },
                {
                    'label': 'Value Two',
                    'value': 'value2'
                },
                {
                    'label': 'Value Three',
                    'value': 'value3'
                }
            ],
            value='value1',
            style={
                'margin': 'auto'
            }
        )]),
        html.Br(),
        dbc.Button(
            id='submit_button',
            n_clicks=0,
            children='Submit',
            color='primary',
            block=True
        ),
    ]
)
###creation sidebar
sidebar = html.Div(
    [
        html.H2('DAPS', style=TEXT_STYLE),
        html.Hr(),

        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact",),
                dbc.NavLink("Base de Donnés ", href="/page-1", active="exact"),
                dbc.NavLink("Visualisation graphique", href="/page-2", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
        #controls
    ],
    style=SIDEBAR_STYLE,
)
##first  row
content_first_row = dbc.Row([
    dbc.Col(
       html.Div([
            html.H6(children='Nombre de fédérations',
                    style={
                        'textAlign': 'center',
                        'color': 'white'}
                    ),
 
            html.P(f"{count_statut['FEDERATION']:,.0f}",
                   style={
                       'textAlign': 'center',
                       'color': 'orange',
                       'fontSize': 40}
                   ),
 
            html.P(' ' + f"{(count_statut['FEDERATION']/len(df1.index)*100):,.0f} "
                   + '%',
                   style={
                       'textAlign': 'center',
                       'color': 'orange',
                       'fontSize': 15,
                       'margin-top': '-18px'}
                   )], className="card_container",
        ),
        md=3 
    ),
     dbc.Col(
       html.Div([
            html.H6(children='Le nombre de femmes actives élèves arbitres:',
                    style={
                        'textAlign': 'center',
                        'color': 'white'}
                    ),
 
            html.P(f"{nbre:,.0f}",
                   style={
                       'textAlign': 'center',
                       'color': 'orange',
                       'fontSize': 40}
                   ),
 
            html.P('new:  ' + f"{70:,.0f} "
                   + ' (' + str(round(56,344)) + '%)',
                   style={
                       'textAlign': 'center',
                       'color': 'orange',
                       'fontSize': 15,
                       'margin-top': '-18px'}
                   )], className="card_container",
        ),
        md=3 
    ),
     dbc.Col(
      html.Div([
            html.H6(children='Nombre de CNP',
                    style={
                        'textAlign': 'center',
                        'color': 'white'}
                    ),
 
            html.P(f"{count_statut['CNP']:,.0f}",
                   style={
                       'textAlign': 'center',
                       'color': 'orange',
                       'fontSize': 40}
                   ),
 
            html.P(' ' + f"{(count_statut['CNP']/len(df1.index)*100):,.0f} "
                   + '%',
                   style={
                       'textAlign': 'center',
                       'color': 'orange',
                       'fontSize': 15,
                       'margin-top': '-18px'}
                   )], className="card_container",
        ),
        md=3 
    ),
     dbc.Col(
       html.Div([
            html.H6(children='Nombre de CNG',
                    style={
                        'textAlign': 'center',
                        'color': 'white'}
                    ),
 
            html.P(f"{count_statut['CNG']:,.0f}",
                   style={
                       'textAlign': 'center',
                       'color': 'orange',
                       'fontSize': 40}
                   ),
 
            html.P(' ' + f"{(count_statut['CNG']/len(df1.index)*100):,.0f} "
                   + '%',
                   style={
                       'textAlign': 'center',
                       'color': 'orange',
                       'fontSize': 15,
                       'margin-top': '-18px'}
                   )], className="card_container",
        ),
        md=3 
    ),
    
])
#####second row
content_second_row = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(id='graph_1',
            figure =fig4
            ), md=4
        ),
        dbc.Col(
            dcc.Graph(id='graph_2',
            
  figure=fig2


#              figure ={'data':[
# go.Scatter(x=confirmed['Date'],y=confirmed['Confirmed'] ,mode='lines',name="confirmed",line=dict(color="Orange",width=4)),
# go.Scatter(x=recovered['Date'],y=recovered['Recovered'] ,mode='lines',name="Recovered",line=dict(color="Green",width=4)),
# go.Scatter(x=deaths['Date'],y=deaths['Deaths'] ,mode='lines',name="Deaths",line=dict(color="Red",width=4))
# #fig.update_layout(title='wordwide covid-19 caes ' ,xaxis_tickfont_size=14,yaxis=dict(title='Number of cases ')),
#             ]   
#             }
            # figure={
            #     'data':[
            #         px.area(temp,x='Date',y='Count',color='Case',height=400,title ='cases over time',color_discrete_sequence=[rec,dth,act]),]
            # }
            ), md=4
        ),
        dbc.Col(
            dcc.Graph(id='graph_3',figure=fig5), md=4
        )
    ]
)
####third row
content_third_row = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(id='graph_4',
            figure =fig
#             {'data':[
# go.Scatter(x=confirmed['Date'],y=confirmed['Confirmed'] ,mode='lines',name="confirmed",line=dict(color="Orange",width=4)),
# go.Scatter(x=recovered['Date'],y=recovered['Recovered'] ,mode='lines',name="Recovered",line=dict(color="Green",width=4)),
# go.Scatter(x=deaths['Date'],y=deaths['Deaths'] ,mode='lines',name="Deaths",line=dict(color="Red",width=4))
# #fig.update_layout(title='wordwide covid-19 caes ' ,xaxis_tickfont_size=14,yaxis=dict(title='Number of cases ')),
#             ] } 
             ), md=12,
        )
    ]
)
#########
content_fourth_row = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(id='graph_5',figure=fig3), md=12
        ),
        
        
    ]
)
content = html.Div(id="page-content",

  
    style=CONTENT_STYLE
)

app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = html.Div([ dcc.Location(id="url"),sidebar, content])
VALID_USERNAME_PASSWORD_PAIRS = [
    ['hello', 'world']]
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)
server=app.server
#####calback for grphe 1

# @app.callback(
#     Output('graph_1', 'figure'),
#     [Input('submit_button', 'n_clicks')],
#     [State('dropdown', 'value'), State('range_slider', 'value'), State('check_list', 'value'),
#      State('radio_items', 'value')
#      ])
# def update_graph_1(n_clicks, dropdown_value, range_slider_value, check_list_value, radio_items_value):
#     print(n_clicks)
#     print(dropdown_value)
#     print(range_slider_value)
#     print(check_list_value)
#     print(radio_items_value)
#     fig = {
#         'data': [{
#             'x': data['Combien de médailles d\'argent avez-vous gagné niveau international :'],
#             'y': [3, 4, 5]
#         }]
#     }
#     return fig

#card calback
# @app.callback(
#     Output('card_title_1', 'children'),
#     [Input('submit_button', 'n_clicks')],
#     [State('dropdown', 'value'), State('range_slider', 'value'), State('check_list', 'value'),
#      State('radio_items', 'value')
#      ])
# def update_card_title_1(n_clicks, dropdown_value, range_slider_value, check_list_value, radio_items_value):
#     print(n_clicks)
#     print(dropdown_value)
#     print(range_slider_value)
#     print(check_list_value)
#     print(radio_items_value)  # Sample data and figure
#     return 'Nombre de fédération '


# @app.callback(
#     Output('card_text_1', 'children'),
#     [Input('submit_button', 'n_clicks')],
#     [State('dropdown', 'value'), State('range_slider', 'value'), State('check_list', 'value'),
#      State('radio_items', 'value')
#      ])
# def update_card_text_1(n_clicks, dropdown_value, range_slider_value, check_list_value, radio_items_value):
#     print(n_clicks)
#     print(dropdown_value)
#     print(range_slider_value)
#     print(check_list_value)
#     print(radio_items_value)  # Sample data and figure
#     return '108'

@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return html.Div(
              [
        html.H2('Dashboard de visualisations des fédérations du sénégal', style=TEXT_STYLE),
        html.Hr(),
        content_first_row,
         content_second_row,
        content_third_row,

        content_fourth_row
    ],
        )
    elif pathname == "/page-1":
        return html.Div([dbc.Row(
            dbc.Col(
                html.Div(
                    dash_table.DataTable(
                        
                        style_table={'overflowX': 'auto'},
    style_cell={
        'height': 'auto',
        # all three widths are needed
        'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
        'whiteSpace': 'normal'
    },
                        id='table',
         columns=[{"name": i, "id": i} for i in df1.columns],
         data=df1.to_dict("records"))
         )

         )
         
         )
        ]
        )
         #return   html.Div(dash_table.DataTable(
        #  id='table',
        #  columns=[{"name": i, "id": i} for i in df.columns],
        #  data=df.to_dict("rows"),
        # pagination_settings={
        #     'current_page': 0,
        #     'page_size': 2
        # },
    #))
    elif pathname == "/page-2":
        return html.P("Oh cool, this is page 2!")
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )

if __name__ == "__main__":
    app.run_server(debug=True,port=8040)