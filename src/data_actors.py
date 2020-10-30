import pandas as pd

# filtered_data with votesNum > 500
data_ids = pd.read_csv('filtered_data_v2.csv')

'''
Data pack No.1 Principals edges at the same time
Arguments:
tconst (string) - alphanumeric unique identifier of the title
ordering (integer) – a number to uniquely identify rows for a given titleId
nconst (string) - alphanumeric unique identifier of the name/person
category (string) - the category of job that person was in
job (string) - the specific job title if applicable, else /N
characters (string) - the name of the character played if applicable, else /N
'''

data_pri = pd.read_csv('title.principals.tsv', sep = '\t')
data_pri.drop(columns = ['characters'])


'''
Data pack No.2 name basics only people's names
Arguments:
nconst (string) - alphanumeric unique identifier of the name/person
primaryName (string)– name by which the person is most often credited
birthYear – in YYYY format
deathYear – in YYYY format if applicable, else /N
primaryProfession (array of strings)– the top-3 professions of the person
knownForTitles (array of tconsts) – titles the person is known for
'''

data_name = pd.read_csv('name.basics.tsv', sep = '\t')
data_name.drop(columns = ['knownForTitles'])

data_actors = pd.merge(data_name,data_pri, on = 'nconst', how = 'left')
data_people = data_ids.merge(data_actors, on = 'tconst', how = 'left')


data_people.to_csv('./people_data.csv', index = False)