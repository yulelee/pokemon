import random
from random_board import Random_board



class Regional_board(Random_board):
    def __init__(self, board_size, spawn_frequency = 2, verbose = True, nearby_variance= 2):
        super(Regional_board, self).__init__(board_size, spawn_frequency, verbose, nearby_variance)

        # this is a dictionary which contains the center of all the pokemons spawns
        # use the pokemon id as th key, and the center is stored as a position tuple
        self.regional_center = {}

    def _init_position(self, pokemon_id):
        if pokemon_id not in self.regional_center:
            self.regional_center[pokemon_id] = super(Regional_board, self)._init_position(pokemon_id)
            if self.verbose:
                print 'set up center for', self.pokedex[pokemon_id], 'at', self.regional_center[pokemon_id]
        return super(Regional_board, self)._random_nearby_positions(self.regional_center[pokemon_id], 1)[0]

