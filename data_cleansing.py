# import relevant packages

import pandas as pd
import numpy as np


# read in data

ratings = pd.read_csv("TV_Ratings_onesheet.csv")
ratings.columns = ratings.columns.str.replace(' ', '').str.lower()
ratings_key_cols = ['hometeamid', 'date']

games = pd.read_csv("games_flat_xml_2012-2018.csv")
games.columns = games.columns.str.replace(' ', '').str.lower()
game_key_cols = ['homeid', 'date']

# drop unecessary columns
badcols = []
for col in games.columns:
    if 'official' in col:
        badcols.append(col)
    elif 'rush' in col:
        badcols.append(col)
    elif 'pass' in col:
        badcols.append(col)
    elif 'penalties' in col:
        badcols.append(col)
    elif 'fumble' in col:
        badcols.append(col)
    elif 'matchupteam' in col:
        badcols.append(col)
        

dupcols = games.columns[[i in ratings.columns for i in games.columns]]
dupcols = dupcols[[i not in game_key_cols for i in dupcols]].values.tolist()

dropcols = badcols + dupcols

games = games.drop(dropcols, axis=1)

# join on home team id and date
df = pd.merge(
    left = ratings,
    right = games,
    left_on = ratings_key_cols,
    right_on = game_key_cols,
    how = 'outer',
    suffixes = ['_r','_g']
)

df = df.rename({'date':'DATE'}, axis='columns')

df['HOMEID'] = df[ratings_key_cols[0]].combine_first(df[game_key_cols[0]])

df.drop([ratings_key_cols[0]] + [game_key_cols[0]], axis = 1)
df = df.set_index(['DATE', 'HOMEID'])
df.to_csv('clean_data.csv')
