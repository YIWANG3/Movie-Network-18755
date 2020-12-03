import pandas as pd
import itertools
import csv


raw_movie_data = pd.read_csv("../../Data_V1/movie_data.csv")
raw_actors_data = pd.read_csv("../../Data_V1/people_with_relation.csv")

def edge_to_csv(filename,data):
    header = ["Source","Target"]

    with open(filename,'w') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter = ',')
        #write head 
        csvwriter.writerow(header)
        #write edges
        csvwriter.writerows(data)


#generate all nodes
nodes_movie = raw_movie_data.drop_duplicates(subset=['tconst'])

# nodes_directors = raw_movie_data['directors'].drop_duplicates()

nodes_movie = nodes_movie.rename({'tconst':'Id'},axis='columns')

edge_movies = []

#generate edges
edges_one = raw_actors_data[["tconst","nconst","averageRating"]]
edges_two = edges_one[edges_one.duplicated(subset = ['nconst'], keep = False)]
edges_sorting = edges_two.sort_values(by = 'nconst')
cur_actor = edges_two['nconst'][0]

tmp = []
for edge_idx in edges_sorting.index:
    if edges_sorting["nconst"][edge_idx] == cur_actor:
        tmp.append(edges_sorting["tconst"][edge_idx])
    else:
        if len(tmp) > 1:
            for edge in itertools.combinations(tmp,2):
                edge_movies.append(edge)
        tmp.clear()
        tmp.append(edges_sorting["tconst"][edge_idx])
        cur_actor = edges_sorting["nconst"][edge_idx]

# add time interval to create dynamic graph
nodes_movie["Time Interval"] = "?"

for node_idx in nodes_movie.index:
    range_key = (nodes_movie["startYear"][node_idx] - 1950) // 10
    nodes_movie["Time Interval"][node_idx] = "<[{},{})>".format(1950 + range_key * 10,1950+(range_key+1)*10)


edge_to_csv('movie_edges.csv',edge_movies)
nodes_movie.to_csv('./movie_nodes.csv',index = False)

