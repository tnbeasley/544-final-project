import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import dash_daq as daq

import pandas as pd
import numpy as np

import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.express as px





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
    'MIZZU':'#F1B82D', 
    'SCAR':'#73000A',
    'TAMU':'#500000',
    'TENN':'#f77f00',
    'VANDY':'#A8996E'
}

df = pd.read_csv('544-final-project-main/clean_data.csv')
teams = np.unique(df[['visteamid', 'hometeamid']].dropna().values.ravel())
sec_teams = ['UA', 'AR', 'AU', 'UF', 'UGA', 'UK', 'LSU', 
             'MIZZU', 'MS', 'OM', 'SCAR','TAMU',
             'TENN', 'VANDY']
#########Carly #################
selectyear = df['year'].unique()
selectyeareDict = [{'label' : x, 'value': x} for x in selectyear ]
###########################
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

sec_season_stats = []
for team in sec_teams:
    team_viewers = df_viewers.loc[((df_viewers.hometeamid==team) |\
                                  (df_viewers.visteamid==team))]\
        .groupby('season')['viewers'].agg(['mean', 'median'])\
        .rename({'mean':'AvgViewers', 'median':'MedViewers'}, axis = 'columns')\
        .reset_index()
    
    team_attend = df_attend.loc[((df_attend.hometeamid==team) |\
                                  (df_attend.visteamid==team))]\
        .groupby('season')['attend'].agg(['mean', 'median'])\
        .rename({'mean':'AvgAttend', 'median':'MedAttend'}, axis = 'columns')\
        .reset_index()
    
    team_ratings = df_rating.loc[((df_rating.hometeamid==team) |\
                                  (df_rating.visteamid==team))]\
        .groupby('season')['rating'].agg(['mean', 'median'])\
        .rename({'mean':'AvgRating', 'median':'MedRating'}, axis = 'columns')\
        .reset_index()
    
    team_stats = team_viewers\
        .merge(team_attend, on = 'season')\
        .merge(team_ratings, on = 'season')
    
    team_stats['team'] = team
    
    sec_season_stats.append(team_stats)
    
sec_season_stats = pd.concat(sec_season_stats).set_index('team').reset_index()





app = dash.Dash(name = __name__, external_stylesheets=[dbc.themes.SLATE])


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
                    html.H5('Choose a team:')
                ], width = 4, style = {'text-align':'right'}),
                dbc.Col(children = [
                    dbc.Select(
                        id = 'selectedTeam',
                        options = [{'label':df_viewers.hometeam[df_viewers.HOMEID == team]\
                                        .unique()[0], 
                                    'value':team} for team in sec_teams],
                        value = 'TENN',
                        style = {'font-size':20}
                    )
                ], width = 8)
            ])
        ], width = 4),
        dbc.Col(children = [
            html.Br(),
            dbc.Button("Help", id="openHelpModal",
                       className="ml-auto", color = 'info')
        ], width = 3, style = {'text-align':'right'}),
        dbc.Col(children = [
            html.Img(src = 'https://upload.wikimedia.org/wikipedia/commons/b/b2/Southeastern_Conference_logo.svg', style = {
                'height' : '75%',
                'width' : '75%',
                'vertical-align': 'top',
                'float' : 'right',
                'position' : 'relative',
                'padding-top' : 10,
                'padding-right' : 0,
                'padding-left':0,
                'padding-bottom':0
            })
        ], width = 1, style = {'text-align':'right'})
    ]),
    
    html.Hr(style = {'background-color':'white'}),

    dbc.Row(children = [
        dbc.Col(children = [
            html.Div(children = [
                dbc.Tabs(children = [
                    dbc.Tab(label = 'Rank', tab_id = 'rank-tab', children = [
                        dbc.Col(children = [ 
############################### Carly #######################################                            
                            dcc.Graph(id = 'rankmetrics', style = {'height':500}),
                            html.H6('Rank Different =  Visit Weighted rank - Home Weighted Rank'),
                            dcc.Dropdown(
                                    id = 'selectedyear',
                                    options = selectyeareDict)
                        ], width = 10)
                    ]),
###################################################################### 
                    dbc.Tab(label = "Weather", tab_id = "weather-tab", children = [
                        dbc.Col(children = [ 

                        ], width = 12)
                    ]), # weather, temperature, time of day
                    dbc.Tab(label = "Network", tab_id = "network-tab", children = [
                        dbc.Col(children = [
                            dcc.Graph(id = 'networkMetrics', style = {'height':550})
                        ], width = 12)
                    ]),
                    dbc.Tab(label = "Matchup", tab_id = "matchup-tab", children = [
                        dbc.Col(children = [

                        ], width = 12)
                    ])
                ], id = 'tabs', active_tab = 'network-tab')      
            ], style = {'height':600}),
            dbc.RadioItems(
                id = 'selectedMetric',
                options = [
                    {'label':'Viewers', 'value':'viewers'},
                    {'label':'Attendance', 'value':'attend'},
                    {'label':'Ratings', 'value':'rating'}
                ],
                value = 'viewers',
                inline = True
            )
        ], width = 7),
        
        dbc.Col(children = [
            dbc.Card(children = [
                dbc.CardHeader(children = [
                    dbc.RadioItems(
                        id = 'statsChoice',
                        options=[
                            {'label': 'Averages', 'value': 'avg'},
                            {'label': 'Medians', 'value': 'med'}
                        ],
                        value='avg',
                        inputStyle={"margin-right": "10px"},
                        inline = True
                    )  
                ]),
                dbc.CardBody(children = [
                    dbc.Row(children = [
                        dbc.Col(children = [
                            html.H5('Viewers'),
                            daq.Gauge(
                                id='viewersGauge',
                                size=125,
                                style = {'color':'black'},
                                color = {'default':'white'}),
                            html.H5('Attendance'),
                            daq.Gauge(
                                id='attendanceGauge',
                                size=125,
                                style = {'color':'black'}),
                            html.H5('Ratings'),
                            daq.Gauge(
                                id='ratingsGauge',
                                size=125,
                                style = {'color':'black'})
                        ], width = 3),
                        dbc.Col(children = [
                            dcc.Graph(id = 'teamStatsPlots',
                                      style = {'height':550})
                        ], width = 9)
                    ]),
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
    [Output('teamStatsPlots', 'figure'),
     Output('viewersGauge', 'value'),
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
def create_right_plots(selectedTeam, statsChoice):
    #### Columns ####
    viewer_col = np.where(statsChoice == 'avg', 'AvgViewers', 'MedViewers').tolist()
    attend_col = np.where(statsChoice == 'avg', 'AvgAttend', 'MedAttend').tolist()
    rating_col = np.where(statsChoice == 'avg', 'AvgRating', 'MedRating').tolist()
    teamColor = teamColorsDict[selectedTeam]
    
    #### Time Series Plots ####
    team_season_stats = sec_season_stats[sec_season_stats.team == selectedTeam]\
        .sort_values('season')
    ts_fig = make_subplots(rows = 3, cols = 1,
                           shared_xaxes=True,
                           vertical_spacing=0.1
#                            subplot_titles=("Viewership", "Attendance", "Ratings")
                          )
    
    ts_fig.add_trace(
        go.Scatter(x=team_season_stats.season, y=team_season_stats[viewer_col],
                   mode = 'lines+markers',
                   marker = {'size':10},
                   line = {'width':5, 'color':teamColor}, name = 'Viewers'), 
        row=1, col=1)

    ts_fig.add_trace(
        go.Scatter(x=team_season_stats.season, y=team_season_stats[attend_col],
                   mode = 'lines+markers',
                   marker = {'size':10},
                   line = {'width':5, 'color':teamColor}, name = 'Attendance'), 
        row=2, col=1)
    
    ts_fig.add_trace(
        go.Scatter(x=team_season_stats.season, y=team_season_stats[rating_col],
                   mode = 'lines+markers',
                   marker = {'size':10},
                   line = {'width':5, 'color':teamColor}, name = 'Ratings'), 
        row=3, col=1)
    
    ts_fig.update_layout(
        showlegend=False,
        margin = {'l':0, 'r':0, 't':20, 'b':0},
        paper_bgcolor = 'rgba(0,0,0,0)',
        plot_bgcolor = 'rgba(0,0,0,0)',
        xaxis1 = {'showgrid': False},
        xaxis2 = {'showgrid': False},
        xaxis3 = {'showgrid': False, 'color':'gray'},
        yaxis1 = {'gridcolor':'gray', 'color':'gray'},
        yaxis2 = {'gridcolor':'gray', 'color':'gray'},
        yaxis3 = {'gridcolor':'gray', 'color':'gray'}
    )
    
    
    #### Gauges ####
    viewer_stats = sec_sum_stats.loc[:,['Team', viewer_col]]
    team_viewer_stats = viewer_stats[viewer_stats.Team == selectedTeam]
    min_views = viewer_stats[viewer_col].min()
    max_views = viewer_stats[viewer_col].max()
    
    attend_stats = sec_sum_stats.loc[:,['Team', attend_col]]
    team_attend_stats = attend_stats[attend_stats.Team == selectedTeam]
    min_attend = attend_stats[attend_col].min()
    max_attend = attend_stats[attend_col].max()
    
    rating_stats = sec_sum_stats.loc[:,['Team', rating_col]]
    team_rating_stats = rating_stats[rating_stats.Team == selectedTeam]
    min_rating = rating_stats[rating_col].min()
    max_rating = rating_stats[rating_col].max()
    
    return(ts_fig,
           team_viewer_stats[viewer_col].values[0], min_views, max_views, teamColor,
           team_attend_stats[attend_col].values[0], min_attend, max_attend, teamColor,
           team_rating_stats[rating_col].values[0], min_rating, max_rating, teamColor)


@app.callback(
    Output('networkMetrics', 'figure'),
    [Input('selectedTeam', 'value'),
     Input('selectedMetric', 'value')]
)
def create_network_plots(selectedTeam, selectedMetric):
    team_df = df.loc[(df.HOMEID == selectedTeam) | (df.visid == selectedTeam)]
    team_df = team_df[(team_df[selectedMetric].isna() == False) & 
                      (team_df.network.isna() == False)]
    avgMetric = team_df.groupby('network')[selectedMetric]\
        .mean().to_frame().reset_index()\
        .sort_values(selectedMetric, ascending = False)
    
    bar = go.Bar(x = avgMetric.network, y = avgMetric[selectedMetric])
    fig = go.Figure(data = bar)
    fig.update_traces(marker = {'color':teamColorsDict[selectedTeam]})
    fig.update_layout(
        margin = {'l':10, 'r':10, 't':40, 'b':5},
        title = {
            'text':f'Avg. {selectedMetric.title()} for {selectedTeam} by Network',
            'font':{'color':'white'}
        },
        xaxis = {'color':'white'},
        yaxis = {'color':'white'},
        paper_bgcolor = 'rgba(0,0,0,0)',
        plot_bgcolor = 'lightgray'
    )
    
    return fig
############################   Carly ########################################## 
@app.callback(
    Output('rankmetrics','figure'),
    [Input('selectedTeam','value'),
     Input('selectedyear','value')]
    
)

### rank
def create_rank_plot (selectedTeam, selectedyear):

    
    team_df = df.loc[df.HOMEID == selectedTeam]
    team_df = team_df[(team_df.homeweightedrank.isna() == False) & (team_df.visitorweightedrank.isna() == False)]
    
    team_df['rank_diff'] = team_df['visitorweightedrank'] - team_df['homeweightedrank'] 
    if selectedyear is None:
        team_df = df.loc[df.HOMEID == selectedTeam]
        team_df = team_df[(team_df.homeweightedrank.isna() == False) & (team_df.visitorweightedrank.isna() == False)]
    
        team_df['rank_diff'] = team_df['visitorweightedrank'] - team_df['homeweightedrank'] 
        
        
    else: 
        team_df = df.loc[df.HOMEID == selectedTeam]
        team_df = team_df[(team_df.homeweightedrank.isna() == False) & (team_df.visitorweightedrank.isna() == False)]
    
        team_df['rank_diff'] = team_df['visitorweightedrank'] - team_df['homeweightedrank']   
        team_df = team_df[team_df.year == selectedyear]
    
    
    hist = px.histogram(team_df,y= 'matchup_full_teamnames',x='rank_diff')

   
    fig = go.Figure(data = hist)
    fig.update_traces(marker = {'color':teamColorsDict[selectedTeam]})
    fig.update_traces(hovertemplate='Home Weighted Rank: %{text}'+
                      '<br> Rank Different: %{x}'
                      '<br> Team: %{y}', 
                      text= [i for i in team_df.homeweightedrank],
    #                  visit = [i for i in team_df.visitorweightedrank],
                      showlegend = False
                      )
    fig.update_traces(hovertemplate=None, selector={'name':'Europe'})
    fig.update_layout(
        margin = {'l':10, 'r':10, 't':40, 'b':5},
        title = {
           'text':f'Hometeam: {selectedTeam}',
            'font':{'color':'white'}
        },
        xaxis = {'color':'white'},
        yaxis = {'color':'white'},
        paper_bgcolor = 'rgba(0,0,0,0)',
        plot_bgcolor = 'lightgray'
    )
    
    fig.update_layout(
    yaxis={
        'title':'full name for hometeam and visit team'},
    xaxis={'title':'Rank Difference'})
    
    fig.update_layout(
    hoverlabel=dict(
        bgcolor="white",
        font_size=16,
        font_family="Rockwell"
    )
)
    return fig
###################################################################### 
if __name__ == '__main__':
    app.run_server(debug = True)
    
    
    