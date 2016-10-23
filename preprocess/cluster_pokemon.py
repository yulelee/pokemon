import json
import numpy as np
from sklearn import preprocessing
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN

np.set_printoptions(threshold = np.nan)


# there are 151 pokemon in total
dataset = np.zeros((151, 151))

# load the pokedex
pokedex_file = open('JSON/pokemon_index.json')
pokedex = json.load(pokedex_file)
pokedex_file.close()

with open('../data/pokemon_spawns_more.csv') as data_file:
    next(data_file)
    for line in data_file:
        example = line.split(',')
        pokemon_id = int(example[0])
        dataset[pokemon_id - 1][pokemon_id - 1] += 1
        neighbors = example[-152:-1]
        for (index, is_neighbor) in enumerate(neighbors):
            if is_neighbor == 'true':
                dataset[pokemon_id - 1][index] += 1

print dataset
dataset = preprocessing.scale(dataset)

# there are 18 types of pokemon, so try this number first
# for n_clusters in range(2, 20):
#     kmeans = KMeans(n_clusters = n_clusters).fit(dataset)
#     clusters = {index: [] for index in range(n_clusters)}
#     for (pokemon_id, label) in enumerate(kmeans.labels_):
#         clusters[label].append(pokedex[pokemon_id])
#     print n_clusters
#     print clusters

# try DBSCAN clustering, seems not require a predetermined number of clusters
dbscan = DBSCAN()
dbscan.fit(dataset)
clusters = {}
for (pokemon_id, label) in enumerate(dbscan.labels_):
    if label not in clusters:
        clusters[label] = []
    clusters[label].append(pokedex[pokemon_id])
print clusters

