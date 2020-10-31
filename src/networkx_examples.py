import networkx as nx

G = nx.read_graphml("../Graphml/movies_no_collaborate.graphml").to_undirected()
degree_sequence = sorted([d for n, d in G.degree()])



# print(G.nodes.data())
# print(G.edges.data())