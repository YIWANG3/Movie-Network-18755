import pandas as pd
import itertools
import csv


def edge_to_csv(filename,data):
    header = ["Source","Target"]

    with open(filename,'w') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter = ',')
        #write head 
        csvwriter.writerow(header)
        #write edges
        csvwriter.writerows(data)


raw_movie_data = pd.read_csv("../../Data_V1/movie_data.csv")
raw_actors_data = pd.read_csv("../../Data_V1/people_with_relation.csv")

#generate all nodes
nodes_movie = raw_movie_data.drop_duplicates(subset=['tconst'])
nodes_movie["Label"] = "movie"
nodes_directors = raw_movie_data['directors'].drop_duplicates()

nodes_movie = nodes_movie.rename({'tconst':'Id'},axis='columns')

nodes_movie = nodes_movie[["Id","Label"]]


nodes_actors = raw_actors_data.drop_duplicates(subset=['nconst'])

nodes_actors.rename({'nconst':'Id','primaryName':'Label'},axis='columns',inplace=True)
nodes_actors = nodes_actors[["Id","Label"]]


#generate edges

edges = raw_actors_data[["tconst","nconst","averageRating"]]

#movie in order
cur_movie = raw_actors_data["tconst"][0]
edges_actors = []
edges_a = []

for idx in raw_actors_data.index:
    # if raw_actors_data['nconst'][idx] in nodes_directors.values:
    #     nodes_actors.loc[nodes_actors['Id'] == raw_actors_data['nconst'][idx],'Label'] = "director"
    if raw_actors_data["tconst"][idx] == cur_movie:
        edges_actors.append(raw_actors_data["nconst"][idx])
    else:
        if len(edges_actors) > 1:
            for edge in itertools.combinations(edges_actors,2):
                edges_a.append(edge)
        edges_actors.clear()
        edges_actors.append(raw_actors_data["nconst"][idx])
        cur_movie = raw_actors_data["tconst"][idx]

edges.rename({'tconst':'Source', 'nconst':'Target', 'averageRating' : 'Weight'}, axis='columns',inplace=True)
nodes =[nodes_movie,nodes_actors]
res = pd.concat(nodes)


edge_to_csv('actor_edge.csv',edges_a)
nodes_actors.to_csv('./actor_nodes.csv',index = False)
edges.to_csv('./graph_edges.csv', index = False)
res.to_csv('./graph_nodes.csv', index = False)
