import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import csv
import json
import community

G = nx.empty_graph(0)  # Empty graph
List_of_movie_cast = []  # list of movie cast
edges = []  # list of edges

with open('TMDB/tmdb_5000_credits.csv') as csvDataFile:  # Open cvs file with credits
    csvReader = csv.reader(csvDataFile)  # read file
    for row in csvReader:  # loop file lines
        try:
            newdict = {}
            list1 = []
            list1.append(row[1])
            names = []
            for val in json.loads(row[2]):  # loop all cast list
                names.append(val['name'])  # add cast names to list
            list1.append(names)
            List_of_movie_cast.append(list1)  # add cast list to list of movie cast
        except ValueError:
            continue

for idx, cast in enumerate(List_of_movie_cast):  # loop through list of movie cast
    for cast2 in List_of_movie_cast[idx:]:  #
        if cast[0] != cast2[0]:  # if not same movie
            if len(list(set(cast[1]) & set(cast2[1]))) > 2:  # if movies have same actors
                edges.append((cast[0], cast2[0]))  # append edges

G.add_edges_from(edges)  # add edges to graf

BC = nx.betweenness_centrality(G)  # calculate betweeness centrality
btc_s = sorted(BC, key=BC.get, reverse=True)  # Sort values
print(btc_s)
