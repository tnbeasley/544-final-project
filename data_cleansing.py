# import relevant packages

import pandas as pd
import numpy as np


# read in data
ratings = pd.read_csv("TV_Ratings_onesheet.csv")
ratings.columns = ratings.columns.str.replace(' ', '').str.lower()
ratings_key_cols = ['hometeamid', 'date']
ratings['date'] = pd.to_datetime(ratings.date)

games = pd.read_csv("games_flat_xml_2012-2018.csv")
games.columns = games.columns.str.replace(' ', '').str.lower()
game_key_cols = ['homeid', 'date']
games['date'] = pd.to_datetime(games.date)


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


# add season variable


# clean weather column

cleaned_weather = []
weather = list(games['weather'].fillna(""))
weather = [day.lower() for day in weather]

for row in weather:
    if 'sun' in row:
        cleaned_weather.append('sunny')
    elif 'rain' in row or 'showers' in row or 'drizz' in row:
        cleaned_weather.append('rain')
    elif 'cloud' in row or 'cldy' in row or 'scatt' in row or 'cloduy' in row:
        cleaned_weather.append('cloudy')
    elif 'clear' in row:
        cleaned_weather.append('clear')
    elif 'indoor' in row or 'roof' in row or 'dome' in row:
        cleaned_weather.append('indoor')
    elif 'overcast' in row:
        cleaned_weather.append('overcast')
    elif 'fair' in row or 'mild' in row or 'calm' in row:
        cleaned_weather.append('fair')
    elif 'perfect' in row or 'beautiful' in row or 'like' in row:
        cleaned_weather.append('perfect')
    elif 'humid' in row or 'muggy' in row or 'warm' in row:
        cleaned_weather.append('humid')
    elif 'haz' in row or 'fog' in row:
        cleaned_weather.append('hazy/foggy')
    elif 'storm' in row or 'lightning' in row or 'flood' in row:
        cleaned_weather.append('severe weather')
    elif 'evening' in row or 'dark' in row or 'night' in row:
        cleaned_weather.append('night')
    elif 'cold' in row or 'chill' in row or 'cool' in row:
        cleaned_weather.append('cold')
    elif '' == row:
        cleaned_weather.append('unknown')

games['weather_clean'] = cleaned_weather

sec_east = ['Vanderbilt', 'Tennessee', 'South Carolina', 
            'Missouri', 'Kentucky', 'Georgia', 'Florida']
sec_west = ['Alabama', 'Arkansas', 'Auburn', 'LSU', 
            'Mississippi (Ole Miss)', 'Mississippi State', 'Texas A&M']
home = list(games['homename'])
league = []
for i in range(0, len(home)):
    if home[i] in sec_east:
        league.append('SEC_EAST')
    elif home[i] in sec_west:
        league.append('SEC_WEST')
    else:
        league.append('INTERDIVISIONAL')
        
games['league'] = league

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
