from scipy import stats
import random
import json

class pokemon_selector():
    def __init__(self, neighbor_rate = 0.3):
        with open('../preprocess/JSON/pokemon_freq.json') as freq_table_file:
            self.freq_table = json.load(freq_table_file)

        with open('../preprocess/JSON/pokemon_index.json') as pokedex_file:
            self.pokedex = json.load(pokedex_file)

        with open('../preprocess/JSON/pokemon_neighbors_stats.json') as neighbor_file:
            self.neighbors_stats = json.load(neighbor_file)

        # the probability that a neighbor appears along side with the initial spawn
        self.neighbor_rate = neighbor_rate

        # a list of all the pokemon ids, might not be start from 1
        self.pokemon_id_list = [entry[0] for entry in self.freq_table]

        # a list of all the frequencies, might not be start from pokemon_id 1,
        # but is consistent with the self.pokemon_id_list
        self.pokemon_frequency = [entry[3] for entry in self.freq_table]

        # a random selector, selector from a list of integers, with the coresponding probabilities
        # the pokemon_id stored in those selectors are the real ids, not the list index
        self.init_selector = stats.rv_discrete(values = (self.pokemon_id_list, self.pokemon_frequency))

        self.neighbor_selector = [stats.rv_discrete(values = (list(range(1, len(self.pokemon_id_list) + 1)), \
                [neighbor_count * 1.0 / sum(self.neighbors_stats[index]) for neighbor_count in self.neighbors_stats[index]])) \
                for index in range(len(self.pokemon_id_list))]

    # spawn the first pokemon, based on the overall probability of appearance of all the pokemons
    # and then choose to spawn neighbors alongs side the initial pokemon, with the probobilit of
    # self.neighbor_rate, for a neighbor, their might be a neighbor of neighbor, but the probability
    # would be self.neighbor_rate ** 2, so it's more rare
    # this function returns a list of spawned pokemons, contains at least one pokemon, each element
    # is a tuple (pokemon_id, pokemon_name)
    def get(self):
        pokemon_id = self.init_selector.rvs()
        result = []

        # current probability of spawning a neighbor
        curr_prob = self.neighbor_rate

        while True:
            result.append([pokemon_id, self.pokedex[pokemon_id - 1]])
            if random.random() > curr_prob: break
            pokemon_id = self.neighbor_selector[pokemon_id - 1].rvs()
            curr_prob *= self.neighbor_rate

        return result



