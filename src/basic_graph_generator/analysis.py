import pandas as pd
import networkx as nx

actors_edges = pd.read_csv('actor_edge.csv')
# actors_nodes = pd.read_csv('actor_nodes.csv')

#init Graph
G = nx.Graph()
G = nx.from_pandas_edgelist(actors_edges,"Source","Target")

#betweenness centrality
bet_centrality = nx.betweenness_centrality(G, k = 1000)

#small-world
sigma = nx.sigma(G)

print("Small world sigma is " + sigma)