import random

######################### Constants

# The size of the board:
WORLD_SIZE = 30


######################### Pokemon_spawn
# Represent the information about a spawn of a certian pokemon.
# General information should include the id and name of the pokemon,
# and other additional information for the game: currently the time before
# the pokemon to disappear

class pokemon_spawn():
    def __init__(self, pokemon_id, pokemon_name, board_size):
        self.pokemon_id = pokemon_id
        self.pokemon_name = pokemon_name
        # maybe need to figure out a way to make this more scalable, the max and min time should
        # be relavent to the size of the board
        self.time_remains = random.randint(board_size // 2, int(board_size * 1.1))

    def __str__(self):
        return 'id: ' + str(self.pokemon_id) + '; name:' + self.pokemon_name + '; time_remain:' + str(self.time_remains)

    def __repr__(self):
        return self.__str__()
