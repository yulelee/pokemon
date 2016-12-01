# This file defines the constants used in the whole project.
# All of the constants and other pre-deterministic values should be defined in this file.


######################### board

# The size of the board, height and width are the same
WORLD_SIZE = 50

# The interval of iterations between consecutive spawns
SPAWN_FREQUENCY = 2

# For the nearby pokemons, the variance of the guassian distribution 
# the distance from the initial spawn 
NEARBY_VARIANCE = 2

MINIMUM_RADAR_SIZE = 5
BOARD_TO_RADAR_RATIO = 2

BOARD_VERBOSE = False


######################### pokemon_selector

# The probability of any spawned pokemon to have a neighbor
NEIGHBOR_RATE = 0.02


######################### simulators

NUM_ITERATIONS = 10000


######################### agents

# the probability of taking a random move (action)
EXPLORATION_RATE = 0.4

AGENT_VERBOSE = False