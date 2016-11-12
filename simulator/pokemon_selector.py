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

        # a dict of pokemon frequencies
        self.pokemon_frequency = {entry[0]: entry[3] for entry in self.freq_table}

        # a random selector, selector from a list of integers, with the coresponding probabilities
        # the pokemon_id stored in those selectors are the real ids, not the list index
        self.init_selector = stats.rv_discrete(values = (self.pokemon_frequency.keys(), self.pokemon_frequency.values()))
        
        self.neighbor_selector = {}
        for pokemon_id in self.pokemon_frequency.keys():
            neighbor_prob = {}
            for neighbor_id in range(1, len(self.pokemon_frequency) + 1):
                if self.neighbors_stats[pokemon_id - 1][neighbor_id - 1] > 0:
                    neighbor_prob[neighbor_id] = self.neighbors_stats[pokemon_id - 1][neighbor_id - 1] * self.pokemon_frequency[neighbor_id]
            
            sum_p = sum(neighbor_prob.values())
            for id in neighbor_prob.keys():
                neighbor_prob[id] /= sum_p

            self.neighbor_selector[pokemon_id] = stats.rv_discrete(values = (neighbor_prob.keys(), neighbor_prob.values()))


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
            pokemon_id = self.neighbor_selector[pokemon_id].rvs()
            curr_prob *= self.neighbor_rate

        #print result

        return result



