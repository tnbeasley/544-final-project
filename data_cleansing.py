import pandas as pd
import numpy as np
import datetime

games = pd.read_csv('games_flat_xml_2012-2018.csv')
tv = pd.read_csv('TV_Ratings_onesheet.csv')

games['Date'] = games['gameid&date'].str.slice(0, 10)
games['gamesid'] = games['gameid&date'].str.slice(10,)

tv = tv.rename(columns = {"VisTeamID":"visid",'HomeTeamID':"homeid"})
pd.merge(left=tv,right=games,how='outer',on=['Date','visid','homeid'])