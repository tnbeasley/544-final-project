# import relevant packages

import pandas as pd


# read in data

ratings = pd.read_csv("TV_Ratings_onesheet.csv")
games = pd.read_csv("games_flat_xml_2012-2018.csv")


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

games = games.drop(badcols, axis=1)

# join on ?
