import pandas as pd
import networkx as nx
import community

mod = pd.read_csv("../../Data_V2/people_with_relation.csv")

df1 = pd.read_csv("cleanNetwork.csv")
df1 = df1[['source', 'target', 'freq']]
df1 = df1.dropna()

G = nx.from_pandas_edgelist(df1, 'source', 'target', edge_attr='freq')
GU = nx.from_pandas_edgelist(df1, 'source', 'target')

G_sorted = pd.DataFrame(sorted(G.degree, key=lambda x: x[1], reverse=True))
G_sorted.columns = ['nconst', 'degree']
# G_sorted = pd.merge(G_sorted,names,how='left',left_on='nconst',right_on='nconst')
print("Top 10 Degree")
print(G_sorted.head(10), "\n")

# -----------------------------------------
dc = nx.degree_centrality(G)
dc = pd.DataFrame([dc.keys(), dc.values()]).T
dc.columns = ['names', 'values']  # call them whatever you like
dc = dc.sort_values(by='values', ascending=False)
print("Top 10 Degree Centrality")
print(dc.head(10), "\n")

# -----------------------------------------
ec = nx.eigenvector_centrality(G, weight='freq')
ec = pd.DataFrame([ec.keys(), ec.values()]).T
ec.columns = ['names', 'values']  # call them whatever you like
ec = ec.sort_values(by='values', ascending=False)
print("Top 10 Eigenvector centrality")
print(ec.head(10), "\n")

# -----------------------------------------
bc = nx.betweenness_centrality(G, k=10000, weight='freq')
bc = pd.DataFrame([bc.keys(), bc.values()]).T
bc.columns = ['names', 'values']  # call them whatever you like
bc = bc.sort_values(by='values', ascending=False)
print("Top 10 Betweenness centrality")
print(bc.head(10), "\n")
