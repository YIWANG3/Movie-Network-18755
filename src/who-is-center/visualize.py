import pandas as pd
import networkx as nx
import community

mod = pd.read_csv("../../Data_V2/people_with_relation.csv")

df1 = pd.read_csv("cleanNetwork.csv")
df1 = df1[['source', 'target', 'freq']]
df1 = df1.dropna()

G = nx.from_pandas_edgelist(df1, 'source', 'target', edge_attr='freq')

H = list(nx.node_connected_component(G, "Nicolas Cage"))
df = df1.loc[(df1['source'].isin(H)) & (df1['target'].isin(H))]

partition = community.best_partition(G, weight='freq')

partition1 = pd.DataFrame([partition]).T
partition1 = partition1.reset_index()
partition1.columns = ['index', 'value']



# nx.write_gexf(G, "center.gexf")

# net1000 = df1.loc[(df1['source'].isin(H)) & (df1['target'].isin(H))]
# G_clean = nx.from_pandas_edgelist(net1000, 'source', 'target', edge_attr='freq')
#
# dc1000 = nx.degree_centrality(G_clean)
# dc1000 = pd.DataFrame([dc1000.keys(), dc1000.values()]).T
# dc1000.columns = ['names', 'values']
# dc1000 = dc1000.sort_values(by='values', ascending=False)
# dc1000 = pd.merge(dc1000, partition1, how='left', left_on="names", right_on="index")
