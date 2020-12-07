import pandas as pd
import re
import csv

movie_data = pd.read_csv("../../Data_V1/movie_data.csv")

movie_data = movie_data[["genres", "startYear", "title"]]

#Collecting all genre types
genres_dict = {}
counts_via_years = [0 for i in range(0,71)] #from 1950 to 2020

for idx in movie_data.index:
    #break genres
    key_arr = re.split(",", movie_data["genres"][idx])
    for key in key_arr:
        if genres_dict.get(key) == None:
            genres_dict[key] = [0 for i in range(0,71)]
        genres_dict[key][movie_data["startYear"][idx] - 1950] += 1


header_year = [str(i) for i in range(1950,2021)]
header = ["Categories"] + header_year 
with open("genre.csv",'w') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter = ',')
    #write head 
    csvwriter.writerow(header)
    #write contents
    for key, value in genres_dict.items():
        data = [key] + value
        csvwriter.writerow(data)

