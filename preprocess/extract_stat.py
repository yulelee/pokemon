import json

pokedex = []

with open('../data/pokemon_index.csv') as data_file:
    next(data_file)
    for line in data_file:
        name = line.split(',')[1]
        pokedex.append(name)

counts = {id: 0 for id in range(1, len(pokedex) + 1)}

with open('../data/pokemon_spawns.csv') as data_file:
    next(data_file)
    for line in data_file:
        pokemon_id = int(line.split(',')[2])
        counts[pokemon_id] += 1


with open('../data/pokemon_spawns_more.csv') as data_file:
    next(data_file)
    for line in data_file:
       pokemon_id = int(line.split(',')[0])
       counts[pokemon_id] += 1



# there are several pokemons that never appeared, laplace smoothing is used
counts = {key: count + 1 for (key, count) in counts.items()}

total_count = sum(counts.values())
freqs = sorted([(name, count * 1.0 / total_count) for (name, count) in counts.items()], \
        cmp = lambda a, b: 1 if a[1] - b[1] < 0 else -1)

# construct the table of pokemon counts and frequencies
# format (tuple in list): pokemon_id, pokemon_name, pokemon_counts, appearance_frequency
table = [(pokemon_id, pokedex[pokemon_id - 1], counts[pokemon_id], freq) for (pokemon_id, freq) in freqs]

with open('JSON/pokemon_freq.json', 'w') as output_file:
    json.dump(table, output_file)

with open('JSON/pokemon_index.json', 'w') as output_file:
    json.dump(pokedex, output_file)

# proposed score system
# first extract the pokemon_id and score from the table
scores = [(pokemon_id, total_count / count) for (pokemon_id, _, count, _) in table]
scores = map(lambda x: x[1], sorted(scores))

with open('JSON/pokemon_score.json', 'w') as output_file:
    json.dump(scores, output_file)
