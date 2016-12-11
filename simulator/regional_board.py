import random
from random_board import Random_board
import sys
sys.path.insert(0, './../utils')
import configurations as cf


class Regional_board(Random_board):
    def __init__(self, board_size = cf.WORLD_SIZE, spawn_frequency = cf.SPAWN_FREQUENCY, verbose = cf.BOARD_VERBOSE, nearby_variance = cf.NEARBY_VARIANCE, radar_radius = cf.MINIMUM_RADAR_SIZE):
        super(Regional_board, self).__init__(board_size, spawn_frequency, verbose, nearby_variance, radar_radius)

        # this is a dictionary which contains the center of all the pokemons spawns
        # use the pokemon id as th key, and the center is stored as a position tuple
        self.regional_center = {}

    def _init_position(self, pokemon_id):
        if pokemon_id not in self.regional_center:
            position = super(Regional_board, self)._init_position(pokemon_id)

            # give a breath region on the borders
            position = (min(self.board_size - 2, max(1, position[0])), min(self.board_size - 2, max(1, position[1])))

            self.regional_center[pokemon_id] = position

            # if pokemon_id == 19 or pokemon_id == 16:
            #     print 'set up center for', self.pokedex[pokemon_id - 1], 'at', self.regional_center[pokemon_id]
            
        return super(Regional_board, self)._random_nearby_positions(self.regional_center[pokemon_id], 1)[0]

