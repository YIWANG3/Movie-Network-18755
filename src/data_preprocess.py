import pandas as pd


data_pri = pd.read_csv('title.principals.tsv', sep = '\t')
data_crew = pd.read_csv('title.crew.tsv', sep = '\t')


new_data = pd.merge(data_pri,data_crew, on = 'tconst')

new_data.to_csv('./processed_data.csv', index = False)