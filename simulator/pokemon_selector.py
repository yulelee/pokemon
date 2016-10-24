from scipy import stats
import json

class pokemon_selector():
    def __init__(self):
        with open('../preprocess/JSON/pokemon_freq.json') as freq_table_file:
            self.freq_table = json.load(freq_table_file)

        with open('../preprocess/JSON/pokemon_index.json') as pokedex_file:
            self.pokedex = json.load(pokedex_file)

        self.pokemon_id_list = [entry[0] for entry in self.freq_table]
        self.pokemon_frequency = [entry[3] for entry in self.freq_table]
        self.init_selector = stats.rv_discrete(values = (self.pokemon_id_list, self.pokemon_frequency))

    def get_init_pokemon(self):
        pokemon_id = self.init_selector.rvs()
        return (pokemon_id, self.pokedex[pokemon_id - 1])



