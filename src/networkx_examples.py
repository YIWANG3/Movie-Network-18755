import networkx as nx

G = nx.read_graphml("../Graphml/movies.graphml").to_undirected()
degree_sequence = sorted([d for n, d in G.degree()])
print(degree_sequence)
