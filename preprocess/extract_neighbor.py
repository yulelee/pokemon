import json

# there are 151 pokemon in total
dataset = [[0 for _ in range(151)] for _ in range(151)]

# load the pokedex
with open('JSON/pokemon_index.json') as pokedex_file:
    pokedex = json.load(pokedex_file)

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

with open('JSON/pokemon_neighbors_stats.json', 'w') as output_file:
    json.dump(dataset, output_file)
