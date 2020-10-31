import pandas as pd
import itertools
import datetime

people_data = pd.read_csv("../../Data_V2/people_with_relation.csv")
data = pd.read_csv("../../Data_V2/movie_data.csv")

movies = data['tconst'].unique().tolist()

df = pd.DataFrame()
counter = 0
for x in movies:
    counter += 1
    movie = data.loc[data['tconst'] == x]
    print(movie)
