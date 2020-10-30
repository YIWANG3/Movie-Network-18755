import pandas as pd

# filtered_data with votesNum > 500
data_ids = pd.read_csv('filtered_data_v2.csv')

'''
Data pack No.1 
Arguments:
titleId (string) - a tconst, an alphanumeric unique identifier of the title
ordering (integer) – a number to uniquely identify rows for a given titleId
title (string) – the localized title
region (string) - the region for this version of the title
language (string) - the language of the title
types (array) - Enumerated set of attributes for this alternative title. One or more of the following: "alternative", "dvd", "festival", "tv", "video", "working", "original", "imdbDisplay". New values may be added in the future without warning
attributes (array) - Additional terms to describe this alternative title, not enumerated
isOriginalTitle 
'''

data_title = pd.read_csv('title.akas.tsv', sep = '\t')
data_title.drop(columns = ['language'])
data_title = data_title.drop(data_title[data_title.region != 'US'].index)
data_title.rename(columns = {'titleId' : 'tconst'}, inplace = True)


'''
Data pack No.2
Arguments:
tconst (string) - alphanumeric unique identifier of the title
titleType (string) – the type/format of the title (e.g. movie, short, tvseries, tvepisode, video, etc)
primaryTitle (string) – the more popular title / the title used by the filmmakers on promotional materials at the point of release
originalTitle (string) - original title, in the original language
isAdult (boolean) - 0: non-adult title; 1: adult title
startYear (YYYY) – represents the release year of a title. In the case of TV Series, it is the series start year
endYear (YYYY) – TV Series end year. /N for all other title types
runtimeMinutes – primary runtime of the title, in minutes
genres (string array) – includes up to three genres associated with the title
'''

data_time = pd.read_csv('title.basics.tsv', sep = '\t')
data_time.drop(columns = ['primaryTitle','originalTitle','runtimeMinutes'])

'''
Data pack No.3
Arguments:
tconst (string) - alphanumeric unique identifier of the title
directors (array of nconsts) - director(s) of the given title
writers (array of nconsts) – writer(s) of the given title
'''
data_directors = pd.read_csv('title.crew.tsv', sep = '\t')

data_movie = pd.merge(data_ids,data_title, on = 'tconst', how = 'left')
data_movie = data_movie.merge(data_time, on = 'tconst', how = 'left')
data_movie = data_movie.merge(data_directors, on = 'tconst',how = 'left')


data_movie.to_csv('./movie_data.csv', index = False)