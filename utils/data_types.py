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
    def __init__(self, pokemon_id, pokemon_name):
        self.pokemon_id = pokemon_id
        self.pokemon_name = pokemon_name
        # maybe need to figure out a way to make this more scalable, the max and min time should
        # be relavent to the size of the board
        self.time_remains = random.randint(5, WORLD_SIZE)
