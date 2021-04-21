import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
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
    'TAMU':'#500000',
    'TENN':'#f77f00',
    'VANDY':'#A8996E'
}


def start_time_chart(df, team, metric):
    teamColor = teamColorsDict[team]

     # redefine labels
    if metric == 'attend':
        labeler = 'Attendance'
    if metric == 'viewers':
        labeler = 'Viewership'
    if metric == 'rating':
        labeler = 'Rating'

     # get team of interest
    df_team = df[(df['hometeamid']==team) & (df['clean_start']!='Unknown')]

    # custom sort generate list of times
    def sortfunc(s):
        return s[0]

    times_sort = sorted(list(df_team['clean_start'].unique()), key=sortfunc)

    # get avg metric per time
    metrics = []
    for time in times_sort:
        games = df_team[df_team['clean_start']==time]
        avg = np.mean(games[metric])
        metrics.append(
            dict(
                times_sort=time,
                metrics=avg,
                color=teamColor
                )
        )

    df_time = pd.DataFrame.from_dict(metrics)

    fig = px.bar(
        df_time,
        x='times_sort',
        y='metrics',
        # color='color',
        #title="Average " + labeler + " by Start Time",
        labels={
            'times_sort': 'Game Start Time',
            'metrics': labeler
        }
    )

    fig.update_traces(marker=dict(color=teamColor))
    fig.update_layout(
        margin = {'l':10, 'r':10, 't':40, 'b':5},
        title = {
            'text':"Average " + labeler + " by Start Time",
            'font':{'color':'white'}
        },
        xaxis = {'color':'white'},
        yaxis = {'color':'white'},
        paper_bgcolor = 'rgba(0,0,0,0)',
        plot_bgcolor = 'lightgray',
        height = 275)


    return(fig)


def temp_chart(df, team, metric):
    teamColor = teamColorsDict[team]

    # redefine labels
    if metric == 'attend':
        labeler = 'Attendance'
    if metric == 'viewers':
        labeler = 'Viewership'
    if metric == 'rating':
        labeler = 'Rating'

     # get team of interest
    df_team = df[(df['hometeamid']==team) & (df['cleaned_temp']!=0)]

    # generate plots
    fig = px.scatter(
            df_team,
            x='cleaned_temp',
            y=metric,
            # title=labeler + " by Temperature",
            labels={
                'cleaned_temp': 'Temperature (F)',
                metric: labeler
            }
    )

    fig.update_traces(marker=dict(color=teamColor))
    fig.update_layout(
        margin = {'l':10, 'r':10, 't':40, 'b':5},
        title = {
            'text':labeler + " by Temperature",
            'font':{'color':'white'}
        },
        xaxis = {'color':'white'},
        yaxis = {'color':'white'},
        paper_bgcolor = 'rgba(0,0,0,0)',
        plot_bgcolor = 'lightgray',
        height = 275)

    return(fig)
