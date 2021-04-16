import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import dash_daq as daq

import pandas as pd
import numpy as np

teamColorsDict = {
    'UA':'#A60C31', 
    'AR':'#9D2235', 
    'AU':'#0C2340',
    'UF':'#003087', 
    'UGA':'#BA0C2F', 
    'UK':'#0033A0',
    'LSU':'#461D7C',
    'OM':'#CE1126', 
    'MS':'#660000',
    'MIZZU':'#2C2A29', 
    'SCAR':'#73000A',
    'TENN':'#f77f00',
    'VANDY':'#A8996E'
}

df = pd.read_csv('clean_data.csv')
teams = np.unique(df[['visteamid', 'hometeamid']].dropna().values.ravel())
sec_teams = ['UA', 'AR', 'AU', 'UF', 'UGA', 'UK', 'LSU', 
             'MIZZU', 'MS', 'OM', 'SCAR','TAMU',
             'TENN', 'VANDY']

df_viewers = df[df.viewers.isna() == False]
df_attend = df[df.attend.isna() == False]
df_rating = df[df.rating.isna() == False]

team_sum_stats = [{
    'Team':team, 
    'AvgViewers':df_viewers.loc[(df_viewers.hometeamid==team) |\
                                (df_viewers.visteamid==team)].viewers.mean(),
    'MedViewers':df_viewers.loc[(df_viewers.hometeamid==team) |\
                                (df_viewers.visteamid==team)].viewers.median(),
    'AvgAttend':df_attend.loc[(df_attend.hometeamid==team) |\
                              (df_attend.visteamid==team)]\
        .attend.mean(),
    'MedAttend':df_attend.loc[(df_attend.hometeamid==team) |\
                              (df_attend.visteamid==team)]\
        .attend.median(),
    'AvgRating':df_rating.loc[(df_rating.hometeamid==team) |\
                              (df_rating.visteamid==team)].rating.mean(),
    'MedRating':df_rating.loc[(df_rating.hometeamid==team) |\
                              (df_rating.visteamid==team)].rating.median()
} for team in teams]
team_sum_stats = pd.DataFrame(team_sum_stats)
sec_sum_stats = team_sum_stats[team_sum_stats.Team.isin(sec_teams)]






app = dash.Dash(name = __name__, external_stylesheets=[dbc.themes.SUPERHERO])


helpModal = dbc.Modal([
    dbc.ModalHeader("Help"),
    dbc.ModalBody(children = [
        html.H5('Purpose of the app'),
        html.H5('How to use the app')
    ]),
    dbc.ModalFooter(
        dbc.Button("Close", id="closeHelpModel", className="ml-auto")
    ),
], id="helpModal", size="lg")

app.layout = dbc.Container(children = [
    helpModal,
    dbc.Row(children = [
        dbc.Col(children = [
            html.Br(),
            html.H4('COLLEGE FOOTBALL'),
            html.H6('How does your team\'s brand stack up against the competition?')
        ], width = 4, style = {'text-align':'left'}),
        dbc.Col(children = [
            html.Br(),
            dbc.Row(children = [
                dbc.Col(children = [
                    html.Label('Choose a team:')
                ], width = 4, style = {'text-align':'right'}),
                dbc.Col(children = [
                    dcc.Dropdown(
                        id = 'selectedTeam',
                        options = [{'label':df_viewers.hometeam[df_viewers.HOMEID == team]\
                                        .unique()[0], 
                                    'value':team} for team in sec_teams],
                        value = 'TENN',
                        style = {'color':'black'}
                    )
                ], width = 8)
            ])
            
        ], width = 4),
        dbc.Col(children = [
            html.Br(),
            dbc.Button("Help", id="openHelpModal", outline = True, 
                       className="ml-auto", color = 'info')
        ], width = 3, style = {'text-align':'right'}),
        dbc.Col(children = [
            html.Img(src = 'https://upload.wikimedia.org/wikipedia/commons/b/b2/Southeastern_Conference_logo.svg', 
                     style = {
                         'height' : '75%',
                         'width' : '75%',
                         'vertical-align': 'top',
                         'float' : 'right',
                         'position' : 'relative',
                         'padding-top' : 5,
                         'padding-right' : 0,
                         'padding-left':0,
                         'padding-bottom':0
                     })
        ], width = 1, style = {'text-align':'right'})
    ]),
    html.Hr(style = {'background-color':'white'}),
    dbc.Row(children = [
        dbc.Col(children = [
            
        ], width = 7),
        dbc.Col(children = [
            dbc.Card(children = [
                dbc.CardHeader(children = [
                    dcc.RadioItems(
                        id = 'statsChoice',
                        options=[
                            {'label': 'Averages', 'value': 'avg'},
                            {'label': 'Medians', 'value': 'med'}
                        ],
                        value='avg',
                        inputStyle={"margin-right": "10px"},
                        labelStyle = {'display': 'inline-block', 'margin-left':'10px'}
                    )  
                ]),
                dbc.CardBody(children = [
                    dbc.Row(children = [
                        dbc.Col(children = [
                            daq.Gauge(
                                id='viewersGauge',
                                label = 'Viewers',
                                size=150
                            )
                        ], width = 4),
                        dbc.Col(children = [
                            daq.Gauge(
                                id='attendanceGauge',
                                label = 'Attendance',
                                size=150
                            )
                        ], width = 4),
                        dbc.Col(children = [
                            daq.Gauge(
                                id='ratingsGauge',
                                label = 'Ratings',
                                size=150
                            )
                        ], width = 4)
                    ])
                ])
                
            ], color = 'light')
        ], width = 5)
    ])
], fluid = True)


@app.callback(
    Output("helpModal", "is_open"),
    [Input("openHelpModal", "n_clicks"), Input("closeHelpModel", "n_clicks")],
    [State("helpModal", "is_open")],
)
def toggle_help_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

@app.callback(
    [Output('viewersGauge', 'value'),
     Output('viewersGauge', 'min'),
     Output('viewersGauge', 'max'),
     Output('viewersGauge', 'color'),
     Output('attendanceGauge', 'value'),
     Output('attendanceGauge', 'min'),
     Output('attendanceGauge', 'max'),
     Output('attendanceGauge', 'color'),
     Output('ratingsGauge', 'value'),
     Output('ratingsGauge', 'min'),
     Output('ratingsGauge', 'max'),
     Output('ratingsGauge', 'color')],
    [Input('selectedTeam', 'value'),
     Input('statsChoice', 'value')]
)
def create_gauges(selectedTeam, statsChoice):
    
    viewer_col = np.where(statsChoice == 'avg', 'AvgViewers', 'MedViewers').tolist()
    viewer_stats = sec_sum_stats.loc[:,['Team', viewer_col]]
    team_viewer_stats = viewer_stats[viewer_stats.Team == selectedTeam]
    min_views = viewer_stats[viewer_col].min()
    max_views = viewer_stats[viewer_col].max()
    
    attend_col = np.where(statsChoice == 'avg', 'AvgAttend', 'MedAttend').tolist()
    attend_stats = sec_sum_stats.loc[:,['Team', attend_col]]
    team_attend_stats = attend_stats[attend_stats.Team == selectedTeam]
    min_attend = attend_stats[attend_col].min()
    max_attend = attend_stats[attend_col].max()
    
    rating_col = np.where(statsChoice == 'avg', 'AvgRating', 'MedRating').tolist()
    rating_stats = sec_sum_stats.loc[:,['Team', rating_col]]
    team_rating_stats = rating_stats[rating_stats.Team == selectedTeam]
    min_rating = rating_stats[rating_col].min()
    max_rating = rating_stats[rating_col].max()
    
    teamColor = teamColorsDict[selectedTeam]
    
    return(team_viewer_stats[viewer_col].values[0], min_views, max_views, teamColor,
           team_attend_stats[attend_col].values[0], min_attend, max_attend, teamColor,
           team_rating_stats[rating_col].values[0], min_rating, max_rating, teamColor)


if __name__ == '__main__':
    app.run_server(debug = True)