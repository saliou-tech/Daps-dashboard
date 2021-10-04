import dash
import dash_auth
import dash_bootstrap_components as dbc
from dash_bootstrap_components._components.CardBody import CardBody
import dash_core_components as dcc
import dash_html_components as html
#from dash_html_components.Hr import Hr
#import dash_table 
from getKoboData import GetKoboData
from dash.dependencies import Input, Output
#from getKoboData import GetKoboData
#import numpy as np
#import pandas as pd
#from plotly.offline import iplot 
#import plotly as py
#import cufflinks as cf 
import plotly.express as px
import plotly.graph_objects as go
#import plotly.figure_factory as ff
#from plotly.subplots import make_subplots
#import folium
import pandas as pd
#import numpy as np
#import matplotlib.pyplot as plt
#import math
#import random
#from datetime import timedelta
import warnings

warnings.filterwarnings('ignore')
#color palette
cnf='#393e46'
dth='#ff2e63'
rec='#21bf73'
act='#fe9801'
import plotly.express as px
from whitenoise import WhiteNoise
import dash_table


#definition des controls
# the style arguments for the sidebar.

# fig.add_trace(go.Scatter(x=confirmed['Date'],y=confirmed['Confirmed'] ,mode='lines',name="confirmed",line=dict(color="Orange",width=4)))
# fig.add_trace(go.Scatter(x=recovered['Date'],y=recovered['Recovered'] ,mode='lines',name="Recovered",line=dict(color="Green",width=4)))
# fig.add_trace(go.Scatter(x=deaths['Date'],y=deaths['Deaths'] ,mode='lines',name="Deaths",line=dict(color="Red",width=4)))
# fig.update_layout(title='wordwide covid-19 caes ' ,xaxis_tickfont_size=14,yaxis=dict(title='Number of cases '))
# fig.show()

kobdata=GetKoboData()
labeld_results=kobdata.getAllData()
df1=kobdata.getDapsDataFrame(labeld_results)
print(df1.columns)
df1.rename(columns={'Quel est le statut de votre structure  ?':'statut'}, inplace=True)
#df1.rename(columns={'Numero questionnaire ':'Numero questionnaire :' }, inplace=True)
df_medaille=df1.groupby(['Quel est le nom de votre structure','statut'])[["Combien de médailles d'or avez-vous gagné niveau international","Combien de médailles d'or avez-vous gagné par les femmes niveau international","Combien de médailles d'or avez-vous gagné par les hommes niveau international"]].sum().reset_index()
df_org=""
count_statut=df1['statut'].value_counts(sort=True, ascending=True)
test1=df1['Le nombre de femmes actives élèves arbitres'].sum()
nbre=int(test1[-1])
df1.rename(columns={"Date d’interview(jj/mm/aa) ":'Date'}, inplace=True)


nbr_enquete_par_jour=df1.groupby("Date").count()['Numero questionnaire :' ].reset_index()
nbr_enquete_par_jour[['Date','Numero questionnaire :' ]]

fig2 = px.bar(nbr_enquete_par_jour, x='Date', y='Numero questionnaire :' ,color='Numero questionnaire :' ,title="Nombre d'enquetes par jour")

fig3=go.Figure()

fig3.add_trace(go.Scatter(x=df_medaille['Quel est le nom de votre structure'],y=df_medaille["Combien de médailles d'or avez-vous gagné niveau international"] ,mode='lines',name="Combien de médailles d'or avez-vous gagné niveau international",line=dict(color="Orange",width=4))),
fig3.add_trace(go.Scatter(x=df_medaille['Quel est le nom de votre structure'],y=df_medaille["Combien de médailles d'or avez-vous gagné par les femmes niveau international"] ,mode='lines',name="Combien de médailles d'or avez-vous gagné par les femmes niveau international",line=dict(color="Green",width=4))),
fig3.add_trace(go.Scatter(x=df_medaille['Quel est le nom de votre structure'],y=df_medaille["Combien de médailles d'or avez-vous gagné par les hommes niveau international"] ,mode='lines',name="Combien de médailles d'or avez-vous gagné par les hommes niveau international",line=dict(color="Red",width=4))),
fig3.update_layout(title='Nombre de medailles gagné par les structures ' ,xaxis_tickfont_size=14,yaxis=dict(title='Nombre de medailles  '))   
section =df1[['Quel est le nom de votre structure','La date de création de votre structure (jj/mm/aa)',"Quelle est la durée de votre mandant (nombre d'années) "]]
fig = px.bar(df1, x="Quel est le nom de votre structure", y="Quel est le nombre de membres dans le comité directeur ?", color="Quel est le nom de votre structure", barmode="group",width=800,

title='Nombre de membres dans lee comite directeur')

count_locaux=df1['Votre structure dispose-t-elle de locaux'].value_counts(sort=True, ascending=True).reset_index()
fig4 = px.pie(count_locaux, values='Votre structure dispose-t-elle de locaux',names='index',title='Locaux')
 
statut = ['FEDERATION','CNP','CNG']


count_sexe=df1['Etes vous'].value_counts(sort=True, ascending=True).reset_index()
fig5 = px.pie(count_sexe, values='Etes vous',names='index',title='Repartition des Sexes')
##################NOMBRE OF CNP ,CNG,FEDERATION###########"# 


NOMBRE_CNP=0
try:
    NOMBRE_CNP=count_statut['CNP']
except:
    NOMBRE_CNP=0

NOMBRE_CNG=0
try:
    NOMBRE_CNG=count_statut['CNG']
except:
    NOMBRE_CNG=0
NOMBRE_FEDERATION=0
try:
    NOMBRE_FEDERATION=count_statut['FEDERATION']
except:
    NOMBRE_FEDERATION=0


##############disposition de structure by statut########""
##############""oui structure##########
count_locaux1=df1[["statut",'Votre structure dispose-t-elle de locaux']]
count_locaux_oui=count_locaux1['Votre structure dispose-t-elle de locaux'].astype(str).str.contains('OUI')
df_oui=count_locaux1[count_locaux_oui]
df_oui['OUI']=df_oui['Votre structure dispose-t-elle de locaux']
oui_strucuture=df_oui.groupby("statut")['OUI'].count().reset_index()
########non structure ####################"
count_locaux_non=count_locaux1['Votre structure dispose-t-elle de locaux'].astype(str).str.contains('NON')
df_non=count_locaux1[count_locaux_non]
df_non['NON']=df_non['Votre structure dispose-t-elle de locaux']
non_strucuture=df_non.groupby("statut")['NON'].count().reset_index()
locaux_by_structure = pd.merge(oui_strucuture, non_strucuture)
OUI=go.Bar(
    x=locaux_by_structure['statut'],
    y=locaux_by_structure['OUI'],
    name="OUI"
)
NON=go.Bar(
    x=locaux_by_structure['statut'],
    y=locaux_by_structure['NON'],
    name="NON"
)
data=[OUI,NON]
layout=go.Layout(title='Possesion de structure en fonction de locaux ')
figure_bar=go.Figure(data=data,layout=layout ,  )
SIDEBAR_STYLE = {
    'position': 'fixed',
    'top': 0,
    'left': 0,
    'bottom': 0,
    'width': '20%',
    'padding': '20px 10px',
    'background-color': '#1f2c56'
}
test=df1.groupby("statut").count().reset_index()
temp=test.melt(id_vars='statut',value_vars=["Combien de médailles d'or avez-vous gagné niveau international","Combien de médailles d'or avez-vous gagné par les femmes niveau international","Combien de médailles d'or avez-vous gagné par les hommes niveau international",],var_name="medailles",value_name='Count')
fig_test=px.area(temp,x='statut',y='Count',color='medailles',height=400,title ='medailles par structure',color_discrete_sequence=[rec,dth,act])
fig_test.update_layout(xaxis_rangeslider_visible=True)
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
# controls = dbc.FormGroup(
#     [
#         html.P('Dropdown', style={
#             'textAlign': 'center'
#         }),
#         dcc.Dropdown(
#             id='dropdown',
#             options=[{
#                 'label': 'Value One',
#                 'value': 'value1'
#             }, {
#                 'label': 'Value Two',
#                 'value': 'value2'
#             },
#                 {
#                     'label': 'Value Three',
#                     'value': 'value3'
#                 }
#             ],
#             value=['value1'],  # default value
#             multi=True
#         ),
#         html.Br(),
#         html.P('Range Slider', style={
#             'textAlign': 'center'
#         }),
#         dcc.RangeSlider(
#             id='range_slider',
#             min=0,
#             max=20,
#             step=0.5,
#             value=[5, 15]
#         ),
#         html.P('Check Box', style={
#             'textAlign': 'center'
#         }),
#         dbc.Card([dbc.Checklist(
#             id='check_list',
#             options=[{
#                 'label': 'Value One',
#                 'value': 'value1'
#             },
#                 {
#                     'label': 'Value Two',
#                     'value': 'value2'
#                 },
#                 {
#                     'label': 'Value Three',
#                     'value': 'value3'
#                 }
#             ],
#             value=['value1', 'value2'],
#             inline=True
#         )]),
#         html.Br(),
#         html.P('Radio Items', style={
#             'textAlign': 'center'
#         }),
#         dbc.Card([dbc.RadioItems(
#             id='radio_items',
#             options=[{
#                 'label': 'Value One',
#                 'value': 'value1'
#             },
#                 {
#                     'label': 'Value Two',
#                     'value': 'value2'
#                 },
#                 {
#                     'label': 'Value Three',
#                     'value': 'value3'
#                 }
#             ],
#             value='value1',
#             style={
#                 'margin': 'auto'
#             }
#         )]),
#         html.Br(),
#         dbc.Button(
#             id='submit_button',
#             n_clicks=0,
#             children='Submit',
#             color='primary',
#             block=True
#         ),
#     ]
# )
###creation sidebar
# sidebar = html.Div(
#     [
#         html.H2(html.Img(id="logo", src=app.get_asset_url("dash-logo-new.png"),), style=TEXT_STYLE),
#         html.Hr(),

#         dbc.Nav(
#             [
#                 dbc.NavLink("Home", href="/", active="exact",),
#                 # dbc.NavLink("Base de Donnés ", href="/page-1", active="exact"),
#                 # dbc.NavLink("Visualisation graphique", href="/page-2", active="exact"),
#             ],
#             vertical=True,
#             pills=True,
#         ),
#         #controls
#     ],
#     style=SIDEBAR_STYLE,
# )
##first  row
content_first_row = dbc.Row([
    dbc.Col(
       html.Div([
            html.H6(children='Nombre de fédérations',
                    style={
                        'textAlign': 'center',
                        'color': 'white'}
                    ),
 
            html.P(f"{NOMBRE_FEDERATION:,.0f}",
                   style={
                       'textAlign': 'center',
                       'color': 'orange',
                       'fontSize': 40}
                   ),
 
            html.P(' ' + f"{(NOMBRE_FEDERATION/len(df1.index)*100):,.0f} "
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
 
            # html.P(':  ' + f"{:,.0f} "
            #        + ' (' + str(round(56,344)) + '%)',
            #        style={
            #            'textAlign': 'center',
            #            'color': 'orange',
            #            'fontSize': 15,
            #            'margin-top': '-18px'}
            #        )
                   ], className="card_container",
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
 
            html.P(f"{NOMBRE_CNP:,.0f}",
                   style={
                       'textAlign': 'center',
                       'color': 'orange',
                       'fontSize': 40}
                   ),
 
            html.P(' ' + f"{(NOMBRE_CNP/len(df1.index)*100):,.0f} "
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
 
            html.P(f"{NOMBRE_CNG:,.0f}",
                   style={
                       'textAlign': 'center',
                       'color': 'orange',
                       'fontSize': 40}
                   ),
 
            html.P(' ' + f"{(NOMBRE_CNG/len(df1.index)*100):,.0f} "
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

content_five_row = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(id='graph_6',figure=figure_bar), md=12
        ),
        #  dbc.Col(
        #     dcc.Graph(id='graph_7',figure=fig_test), md=6
        # ),
        
        
    ]
)

content_six_row = dbc.Row(
    [
        # dbc.Col(
        #     dcc.Graph(id='graph_6',figure=figure_bar), md=6
        # ),
         dbc.Col(
            dcc.Graph(id='graph_7',figure=fig_test), md=12
        ),
        
        
    ]
)
content = html.Div(id="page-content",style=CONTENT_STYLE
)

app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP],suppress_callback_exceptions=True,)

sidebar = html.Div(
    [
        html.H2(html.Img(id="logo", src="static/logo.PNG",width="auto",height="150"), style=TEXT_STYLE),
        html.Hr(),

        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact",),
                # dbc.NavLink("Base de Donnés ", href="/page-1", active="exact"),
                dbc.NavLink("Information Structure", href="/page-2", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
        #controls
    ],
    style=SIDEBAR_STYLE,
)
app.layout = html.Div([ dcc.Location(id="url"),sidebar, content])
VALID_USERNAME_PASSWORD_PAIRS = [
    ['update', 'update']]
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)
server=app.server
server.wsgi_app = WhiteNoise(server.wsgi_app, root='static/')

#####calback for grphe 1





@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return html.Div(
              [
        html.H2('DIRECTION DES ACTIVITES PHYSIQUE ET SPORTIVES', style=TEXT_STYLE),
        html.Hr(),
        content_first_row,
        html.Hr(),
        content_second_row,
        content_third_row,
        content_fourth_row,
        content_five_row,
        content_six_row
    ],
        )
    # elif pathname == "/page-1":
    #     return html.Div([dbc.Row(
    #         dbc.Col(
    #             html.Div(
    #                 dash_table.DataTable(
                        
    #                     style_table={'overflowX': 'auto'},
    # style_cell={
    #     'height': 'auto',
    #     # all three widths are needed
    #     'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
    #     'whiteSpace': 'normal'
    # },
    #                     id='table',
    #      columns=[{"name": i, "id": i} for i in df1.columns],
    #      data=df1.to_dict("records"))
    #      )

    #      )
         
    #      )
    #     ]
    #     )
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
        

        return html.Div([
                html.Div([(
                    dcc.Dropdown(
                        id='demo-dropdown',
                        options=[{'label':i,'value':i} for i in statut],
                        value='displacement',
            
                        )
                        )],style={'width':'100%','display':'inline-block'}
                        ),
                        dcc.Dropdown(
                        id='dd-output-container',
                     
                        ),
                       # dash_table.DataTable(
   # id='data',columns=[{"name": i, "id": i} for i in df1.columns]),
   
   
  html.Div(id="page-content1",style=CONTENT_STYLE,
  
  )  ,
  dbc.Row(id="col1",
   
    
)
      
]
       
)
    
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )

# @app.callback(
#             Output('feature-graphic','figure'),
#             [Input('xaxis','value')]
#         )
# def update_graph(xaxis_valus):
#     print(xaxis_valus)
#     temp=test.melt(id_vars='statut',value_vars=[xaxis_valus],var_name=xaxis_valus,value_name='Count')
#     fig_test2=px.area(temp,x='statut',y='Count',color=xaxis_valus,height=400,title ='medailles par structure',color_discrete_sequence=[rec,dth,act])
#     fig_test.update_layout(xaxis_rangeslider_visible=True)
#     #fig.show()
#     return {'data':[  
#            px.area(temp,x='statut',y='Count',color=xaxis_valus,height=400,title ='medailles par structure',color_discrete_sequence=[rec,dth,act])
#             ]}
def getComponent(columns,df11,value ):
    card_content = [
        dbc.CardHeader(value),
        dbc.CardBody(
            [
                html.H5(columns, className="card-title"),
                html.P(
                    df11[columns].values[0],
                    className="card-text",
                ),
            ]
        ),
    ]


    return dbc.Row(
               [
                   dbc.Col(dbc.Card(card_content, color="info", outline=True)),
                   #dbc.Col(dbc.Card(card_content, color="secondary", outline=True)),
                   #dbc.Col(dbc.Card(card_content, color="info", outline=True)),
               ],
               className="mb-12",
           )
#     return   dbc.Card([
#
#             html.H6(columns,
#                     style={
#                         'textAlign': 'center',
#                         'color': 'orange',
#                         }
#                     ),
#
#             dbc.CardBody(f"{df11[columns].values[0]:}",
#                    style={
#                        'textAlign': 'center',
#                        'color': 'orange',
#                        'fontSize': 20}
#                    ),
#
#           ], className="card_container",
#         )

@app.callback(
      dash.dependencies.Output('dd-output-container', 'options'),
                                    [dash.dependencies.Input('demo-dropdown', 'value')])
def update_output(value):

     #print(value)
     ##nbr_enquete_par_jour=df5.groupby("Date").count()['Numero questionnaire :' ].reset_index()

     #fig8 = px.bar(nbr_enquete_par_jour, x='Date', y='Numero questionnaire :' ,color='Numero questionnaire :' ,title="Nombre d'enquetes par jour")
     df00=df1[['statut','Quel est le nom de votre structure']]
     df0=df00[df00['statut'] == value]
     df11=df0['Quel est le nom de votre structure']
     df_org=df11
     return  [{"label":i,"value":i} for i in df11]
     #return df_org
     


@app.callback(
     # dash.dependencies.Output('page-content1', 'children'),
      dash.dependencies.Output('col1', 'children'),

                                    [dash.dependencies.Input('dd-output-container', 'value')])
def update_output_1(value):

     #print(value)
     ##nbr_enquete_par_jour=df5.groupby("Date").count()['Numero questionnaire :' ].reset_index()

     #fig8 = px.bar(nbr_enquete_par_jour, x='Date', y='Numero questionnaire :' ,color='Numero questionnaire :' ,title="Nombre d'enquetes par jour")
    # df00=df1[['statut','Quel est le nom de votre structure']]
     #df0=df00[df00['statut'] == value]
     df11=df1[df1['Quel est le nom de votre structure']==value]
     #Sprint(df11)
     #return  df11.to_dict('records')
     print(df11['Quel est le nombre de membres dans le comité directeur ?'])
     nbre_comitte=df11["Quel est le nombre de membres dans le comité directeur ?"].values[0]
     print(nbre_comitte)
     print(df11.columns)
     return html.Div(
      children=[getComponent(column,df11,value) for column in df11.columns[7:]]

     )
#      return  dbc.Row(
#      [
#      dbc.Col(
#              html.Div( children=[getComponent(column,df11) for column in df11.columns[5:]
#
#              ]),   width={"size": 6, "offset": 3},
#
#
#
#
#
#          )
#          ]
#          )

    #  return    html.Div([
    #         html.H6(children='Quel est le nombre de membres dans le comité directeur ? :',

    #                 style={
    #                     'textAlign': 'center',
    #                     'color': 'white'}
    #                 ),
 
    #         html.P(f"{df11['Quel est le nombre de membres dans le comité directeur ?'].values[0]}",
    #                style={
    #                    'textAlign': 'center',
    #                    'color': 'orange',
    #                    'fontSize': 40}
    #                ),
    #  ], className="card_container",
    #     )
     return dbc.Col([
           html.H1("Identification de l organisation",
           style={
                        'textAlign': 'center',
                        'color': 'white'}),
           html.Br(),
    dbc.Col(
      
       html.Div([
           
            html.H6(children='Disciplines pratiquees',
                    style={
                        'textAlign': 'center',
                        'color': 'white',
                        }
                    ),
 
            html.P(f"{df11['Quelles disciplines pratiquez-vous '].values[0]:}",
                   style={
                       'textAlign': 'center',
                       'color': 'orange',
                       'fontSize': 20}
                   ),
 
          ], className="card_container",
        ),
        md=3 
    ),
     dbc.Col(
       html.Div([
            html.H6(children='Outils de travail:',
                    style={
                        'textAlign': 'center',
                        'color': 'white'}
                    ),
 
            html.P(f"{df11['Quel sont les outils de travail que vous utilisez  ?'].values[0]:}",
                   style={
                       'textAlign': 'center',
                       'color': 'orange',
                       'fontSize': 20}
                   ),
 
            # html.P(':  ' + f"{:,.0f} "
            #        + ' (' + str(round(56,344)) + '%)',
            #        style={
            #            'textAlign': 'center',
            #            'color': 'orange',
            #            'fontSize': 15,
            #            'margin-top': '-18px'}
            #        )
                   ], className="card_container",
        ),
        md=3 
    ),
     dbc.Col(
      html.Div([
            html.H6(children='Membres dans le comite directeur',
                    style={
                        'textAlign': 'center',
                        'color': 'white'}
                    ),
 
                html.P(' ' + f"{df11['Quel est le nombre de membres dans le comité directeur ?'].values[0]:} "
                   ,
                   style={
                       'textAlign': 'center',
                       'color': 'orange',
                       'fontSize': 20,
                       }
                   ),
 
            ], className="card_container",
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
 
            html.P(f"{NOMBRE_CNG:,.0f}",
                   style={
                       'textAlign': 'center',
                       'color': 'orange',
                       'fontSize': 40}
                   ),
 
            html.P(' ' + f"{(NOMBRE_CNG/len(df1.index)*100):,.0f} "
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

if __name__ == "__main__":
    app.run_server(debug=True,port=8040)