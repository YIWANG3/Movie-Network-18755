import pandas as pd
import networkx as nx
import itertools
import csv


raw_movie_data = pd.read_csv("../../Data_V1/movie_data.csv")
raw_actors_data = pd.read_csv("../../Data_V1/people_with_relation.csv")

raw_movie_data = raw_movie_data.drop_duplicates(subset = "tconst")

def generate_edges(idx): 
    #generate edges
    edges_one = raw_actors_data[["tconst","nconst","averageRating"]]
    edges_two = edges_one[edges_one.duplicated(subset = ['nconst'], keep = False)]
    edges_sorting = edges_two.sort_values(by = 'nconst')
    cur_actor = edges_two['nconst'][0]
    edges = []
    tmp = []
    for edge_idx in edges_sorting.index:
        if edges_sorting["nconst"][edge_idx] == cur_actor:
            year = (raw_movie_data.loc[raw_movie_data["tconst"] == edges_sorting["tconst"][edge_idx]])["startYear"]
            if (year >= periods[idx][0]).all() and (year < periods[idx][1]).all():
                tmp.append(edges_sorting["tconst"][edge_idx])
        else:
            if len(tmp) >= 2:
                for edge in itertools.combinations(tmp,2):
                    edges.append(tuple(edge))
            tmp.clear()
            tmp.append(edges_sorting["tconst"][edge_idx])
            cur_actor = edges_sorting["nconst"][edge_idx]
    return edges


def list_to_csv(filename,data):
    with open(filename,'w') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter = ',')
        #write content
        csvwriter.writerows(data)

#generating period
startYear = 1950
periods = []
while startYear < 2012:
    periods.append([startYear,startYear+9])
    startYear += 10

#split datasets
dataframes = []
for interval in periods:
    dataframes.append(raw_movie_data[raw_movie_data["startYear"].isin(interval)])

#edges in periods and create graphs
edges_time = []
graphs = []
for idx in range(len(periods)):
    edges_time.append(generate_edges(idx))

#create graphs
graphs = []
for idx in range(len(edges_time)):
    G = nx.Graph()
    G.add_edges_from(edges_time[idx])
    graphs.append(G)
    print(G.number_of_nodes())

#Calculate all stuff
betweenness_centralitys = []
average_cc = []
degree_centrality = []
triangles = []
average_degree = []

for g in graphs:
    betweenness_centralitys.append(nx.betweenness_centrality(g))
    average_cc.append(nx.average_clustering(g))
    degree_centrality.append(nx.degree_centrality(g))
    triangles.append(nx.triangles(g))

    #average degree
    degrees = g.degree()
    sum_of_degree = 0
    for n,d in degrees:
        sum_of_degree += d
    average_degree.append(sum_of_degree/g.number_of_nodes())

def max_val(dict):
    val = list(dict.values())
    return max(val)

betweenness_centralitys_max = []
degree_centrality_max = []
#calc the highest betweenness and degree centrality from each period of time
for idx in range(len(edges_time)):
    betweenness_centralitys_max.append(max_val(betweenness_centralitys[idx]))
    degree_centrality_max.append(max_val(degree_centrality[idx]))

#export to csvs
result_dict = {'average_degrees': average_degree, 'max_betweeness_centrality': betweenness_centralitys_max,
                 'max_degree_centrality': degree_centrality_max, 'average_clustering_coefficient': average_cc}

ex_df = pd.DataFrame(result_dict)
ex_df.to_csv('./statics.csv')

# list_to_csv("average_degrees.csv",average_degree)
# list_to_csv("max_betweeness_centrality.csv", betweenness_centralitys_max)
# list_to_csv("max_degree_centrality.csv", degree_centrality_max)
# list_to_csv("average_clustering_coefficient.csv", average_cc)