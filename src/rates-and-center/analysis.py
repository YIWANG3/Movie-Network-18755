import pandas as pd
import networkx as nx
import community
import matplotlib.pyplot as plt

people_data = pd.read_csv("../../Data_V2/people_with_relation.csv")
movie_data = pd.read_csv("../../Data_V2/movie_data.csv")

names = pd.DataFrame(people_data[['nconst', 'primaryName']].drop_duplicates())
movies = pd.DataFrame(movie_data[['tconst', 'primaryTitle', 'averageRating']].drop_duplicates())

G = nx.from_pandas_edgelist(people_data, 'nconst', 'tconst')

ec = nx.closeness_centrality(G)
ec = pd.DataFrame([ec.keys(), ec.values()]).T
ec.columns = ['id', 'values']  # call them whatever you like
ec = ec.sort_values(by='values', ascending=False)

df1 = ec.merge(movies, left_on="id", right_on="tconst")

centrality_values = df1["values"].to_list()
rates = df1["averageRating"].to_list()


def normalize(nums):
    return [float(i) / sum(nums) for i in nums]


def normalize2(nums, base):
    return [float(i) / base for i in nums]


def normalize3(nums, ratio):
    return [float(i) * ratio for i in nums]


x = [i for i in range(len(rates))]

fig, ax = plt.subplots()
temp, = plt.plot(x, normalize3(centrality_values, 1.0 / centrality_values[0]), "*", color="black")
temp.set_label("centrality_values")
temp2, = plt.plot(x, normalize2(rates, 10), "+", color="red")
temp2.set_label("rates")
ax.legend()
# ax.set_xticks([d + 0.4 for d in deg])
# ax.set_xticklabels(deg)
plt.show()
