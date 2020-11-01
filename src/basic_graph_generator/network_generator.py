import pandas as pd


raw_movie_data = pd.read_csv("../../Data_V1/movie_data.csv")
raw_actors_data = pd.read_csv("../../Data_V1/people_with_relation.csv")

#generate all nodes
nodes_movie = raw_movie_data.drop_duplicates(subset=['tconst'])
nodes_movie["Label"] = "movie"


nodes_movie = nodes_movie.rename({'tconst':'Id'},axis='columns')

nodes_movie = nodes_movie[["Id","Label"]]


nodes_actors = raw_actors_data.drop_duplicates(subset=['nconst'])
nodes_actors["Label"] = "actor"

nodes_actors.rename({'nconst':'Id'},axis='columns',inplace=True)
nodes_actors = nodes_actors[["Id","Label"]]
nodes =[nodes_movie,nodes_actors]
res = pd.concat(nodes)

res.to_csv('./graph_nodes.csv', index = False)

#generate edges

edges = raw_actors_data[["tconst","nconst"]]

edges.rename({'tconst':'Source', 'nconst':'Target'}, axis='columns',inplace=True)

edges.to_csv('./graph_edges.csv', index = False)
