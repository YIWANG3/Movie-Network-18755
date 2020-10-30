import pandas as pd
import itertools
import datetime

data = pd.read_csv("../../Data_V2/people_with_relation.csv")

names = pd.DataFrame(data[['nconst', 'primaryName']].drop_duplicates())
movies = data['tconst'].unique().tolist()

df = pd.DataFrame()
counter = 0
for x in movies:
    counter = counter + 1
    movie = data.loc[data['tconst'] == x]
    temp = pd.DataFrame(list(itertools.combinations(movie['nconst'], 2)))
    if len(temp) == 0:
        continue
    temp.columns = ['source', 'target']
    df = pd.concat([df, temp])
    if counter % 1000 == 0:
        print(x + " " + str(counter) + " " + str(datetime.datetime.now()))
df = df.groupby(["source", "target"]).size().reset_index(name="freq")

df1 = pd.merge(df, names, how='left', left_on='source', right_on='nconst')
df1 = pd.merge(df1, names, how='left', left_on='target', right_on='nconst')
df1 = df1[['primaryName_x', 'primaryName_y', 'freq']]
df1.columns = ['source', 'target', 'freq']

df1.to_csv("cleanNetwork.csv")

