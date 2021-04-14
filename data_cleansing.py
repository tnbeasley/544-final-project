# import relevant packages

import pandas as pd


# read in data

ratings = pd.read_csv("TV_Ratings_onesheet.csv")
ratings.columns = ratings.columns.str.replace(' ', '').str.lower()

games = pd.read_csv("games_flat_xml_2012-2018.csv")
games.columns = games.columns.str.replace(' ', '').str.lower()

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

games = games.drop(badcols, axis=1)

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


# join on home team id and date


