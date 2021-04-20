import pandas as pd
import matplotlib.pyplot as plt
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

def weather_charts(df, team, metric):
    """Makes plots for weather tab of app"""
    
    # skeleton of graph
    fig, (ax1, ax2) = plt.subplots(2,1, figsize=(10,10))
    
     # redefine labelS
    if metric == 'attend':
        labeler = 'Attendance'
    if metric == 'viewers':
        labeler = 'Viewership'
    if metric == 'rating':
        labeler = 'Rating'
    
    ##################### Start Time Graph
    
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
        metrics.append(avg)
        
    # generate plot
    ax1.bar(times_sort, metrics, width = 0.35, color = teamColorsDict[team])
    ax1.set_title('Average '+labeler+' by Start Time')
    ax1.set_xticks(times_sort)
    ax1.set_ylabel(labeler)
    ax1.set_xlabel("Game Start Time")
    ax1.set_xticklabels(times_sort)
    
   ##################### Temperature Graph

    # get team of interest
    df_team = df[(df['hometeamid']==team) & (df['cleaned_temp']!=0)]
        
    # generate plot
    lineStart = df_team[metric].min()
    lineEnd = df_team[metric].max()
    lowtemp = df_team['cleaned_temp'].min()
    hitemp = df_team['cleaned_temp'].max()
    
    ax2.scatter(df_team['cleaned_temp'], df_team[metric], c=pd.to_datetime(df_team['DATE']))
    ax2.set_title('Average ' + labeler + ' by Temperature')
    ax2.set_ylabel(labeler)
    ax2.set_xlabel("Temperature (F)")
    ax2.plot([lowtemp, hitemp], [lineStart, lineEnd], 'k-', color = 'b')
    
    # return plot
    fig.tight_layout()
    return(fig)
    # plt.show()




    