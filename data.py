def import_data():
    import pandas as pd
    
    df = pd.read_csv('clean_data.csv')
    return df

def remove_null_columns(df):
    import pandas as pd
    
    df_viewers = df[df.viewers.isna() == False]
    df_attend = df[df.attend.isna() == False]
    df_rating = df[df.rating.isna() == False]
    
    return df_viewers, df_attend, df_rating

def calc_team_sum_stats(df, df_viewers, df_attend, df_rating, sec_teams):
    import numpy as np
    import pandas as pd
    
    teams = np.unique(df[['visteamid', 'hometeamid']].dropna().values.ravel())
    
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
    
    return team_sum_stats, sec_sum_stats
    
def calc_sec_season_stats(df_viewers, df_attend, df_rating, team_sum_stats, sec_teams):
    import pandas as pd
    
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
    
    return sec_season_stats