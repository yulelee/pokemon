import json

# there are 151 pokemon in total
# all the elements are initialzed to 1, similar to laplace smoothing, give the
# unseen situations a little bit of chance to happen
dataset = [[1 for _ in range(151)] for _ in range(151)]

# load the pokedex
with open('JSON/pokemon_index.json') as pokedex_file:
    pokedex = json.load(pokedex_file)

with open('../data/pokemon_spawns_more.csv') as data_file:
    next(data_file)
    for line in data_file:
        example = line.split(',')
        pokemon_id = int(example[0])
        neighbors = example[-152:-1]
        for (index, is_neighbor) in enumerate(neighbors):
            if is_neighbor == 'true':
                dataset[pokemon_id - 1][index] += 1

# for each dataset[index][index], it represent the times a pokemon appears with itself
# which is not contained in the dataset, and is arbitrarily set to the max of all of
# its neighbors, plus one, so a pokemon appears with itself is of the same probability of
# most probable neighbor, with a slightly advantage
for index in range(len(dataset)):
    dataset[index][index] += max(dataset[index])

with open('JSON/pokemon_neighbors_stats.json', 'w') as output_file:
    json.dump(dataset, output_file)
