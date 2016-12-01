import random
import sys
sys.path.insert(0, './../utils')
from data_types import pokemon_spawn
import configurations as cf
import pokemon_selector as ps
import json

class Random_board(object):

    def __init__(self, board_size = cf.WORLD_SIZE, spawn_frequency = cf.SPAWN_FREQUENCY, verbose = cf.BOARD_VERBOSE, nearby_variance = cf.NEARBY_VARIANCE):
        self.verbose = verbose
        self.board_size = board_size
        self.spawn_frequency = spawn_frequency
        self.radar_radius = max(board_size // 4, 10)
        self.agent_position = (board_size // 2, board_size // 2)
        self.pokemon_selector = ps.Pokemon_selector()
        self.pokedex = self.pokemon_selector.pokedex
        self.nearby_variance = nearby_variance

        # board is defined by a dictionary, tuple (x, y)=> a list of pokemons within this position
        # a pokemon is represented by the data_type pokemon_spawn
        self.board = {}
        self.time = 0

        # statistics about spawning
        self.total_spawn_num = 0
        self.total_spawn_score = 0

        # load in the score (reward) system
        with open('../preprocess/JSON/pokemon_score.json') as score_file:
            self.scores = json.load(score_file)

    def possible_moves(self):
        result = []
        if self.agent_position[0] > 0: result.append('Left')
        if self.agent_position[0] < self.board_size: result.append('Right')
        if self.agent_position[1] > 0: result.append('Down')
        if self.agent_position[1] < self.board_size: result.append('Up')
        return result


    # get a random position within the board
    def _init_position(self, pokemon_id):
        return (random.randint(0, self.board_size), random.randint(0, self.board_size))

    # return a list of nearby positions, how many? num_nearby
    def _random_nearby_positions(self, current_position, num_nearby):

        # produce a one-dimensional number, near the current, generated by gaussian distribution
        def _axis_within_board(current):
            return int(max(min(random.gauss(current, self.nearby_variance), self.board_size), 0))

        def _nearby_position():
            return (_axis_within_board(current_position[0]), _axis_within_board(current_position[1]))

        return [_nearby_position() for _ in range(num_nearby)]


    # put a pokemon at a specific position of the board
    def _spawn(self, position, pokemon):
        if position not in self.board:
            self.board[position] = []
        self.board[position].append(pokemon_spawn(pokemon[0], pokemon[1], self.board_size))
        if self.verbose: print pokemon[1] + ' spawned at ' + str(position)
        self.total_spawn_num += 1
        self.total_spawn_score += self.scores[pokemon[0] - 1]

    # the rader, detect the nearby pokemons
    def _nearby_pokemons(self):
        start_x = max(0, self.agent_position[0] - self.radar_radius)
        start_y = max(0, self.agent_position[1] - self.radar_radius)
        end_x = min(self.board_size, self.agent_position[0] + self.radar_radius)
        end_y = min(self.board_size, self.agent_position[1] + self.radar_radius)

        result = []
        for x in range(start_x, end_x + 1):
            for y in range(start_y, end_y + 1):
                if (x, y) in self.board:
                    manhattan_dis = abs(x - self.agent_position[0]) + abs(y - self.agent_position[1])
                    result.extend([(manhattan_dis, pokemon) for pokemon in self.board[(x, y)]])

        # manhattan distence is the first element within each tuple, therefore is used to sort
        result.sort()

        # remove the distences, and just return a list of pokemons ids
        return map(lambda x: x[1].pokemon_id, result)

    def spend_time(self):

        # if are at the frequency point, we need to spawn some new pokemons!
        if self.time % self.spawn_frequency == 0:
            new_pokemons = self.pokemon_selector.get()
            spawn_center = self._init_position(new_pokemons[0][0])
            self._spawn(spawn_center, new_pokemons[0])
            nearby_positions = self._random_nearby_positions(spawn_center, len(new_pokemons) - 1) # could be empty
            for (index, position) in enumerate(nearby_positions):
                self._spawn(position, new_pokemons[index + 1])

        # every time we also need to scan over all the pokemons, if their time is up, just clean them
        for position in self.board.keys():
            for pokemon in self.board[position]:
                pokemon.time_remains -= 1
            self.board[position] = filter(lambda x: x.time_remains > 0, self.board[position])

        self.time += 1

    # assume the action is aquired by the board, therefore cannot be illegal
    # this is the main function for the simulator to call, the argument is the direction to move the
    # agent, and the return values is the tuple (reward get by this move, radar information)

    # return value: (rewards, pokemons_caught, num_pokemon_caught, radar)
    # pokemons_caught and radar are both a list of pokemon_ids, could be empty list
    def move_agent(self, action):
        if action == 'Left': self.agent_position = (self.agent_position[0] - 1, self.agent_position[1])
        if action == 'Right': self.agent_position = (self.agent_position[0] + 1, self.agent_position[1])
        if action == 'Down': self.agent_position = (self.agent_position[0], self.agent_position[1] - 1)
        if action == 'Up': self.agent_position = (self.agent_position[0], self.agent_position[1] + 1)

        if self.verbose: print 'agent move', action, 'to', str(self.agent_position)

        # catch and receive rewards
        if self.agent_position in self.board and len(self.board[self.agent_position]) > 0:
            total_rewards = sum(self.scores[pokemon.pokemon_id - 1] for pokemon in self.board[self.agent_position])
            if self.verbose:
                for pokemon in self.board[self.agent_position]:
                    print pokemon.pokemon_name + ' caught at ' + str(self.agent_position)
            num_pokemon_catched = len(self.board[self.agent_position])
            pokemons_caught = [pokemon.pokemon_id for pokemon in self.board[self.agent_position]]
            del self.board[self.agent_position]
        else:
            pokemons_caught = []
            total_rewards = 0
            num_pokemon_catched = 0
        self.spend_time()
        radar = self._nearby_pokemons()
        if self.verbose: print 'radar:', radar
        return (total_rewards, pokemons_caught, num_pokemon_catched, radar)

    # used to debug
    def toString(self):
        print 'board_size:', self.board_size
        print 'spawn_frequency', self.spawn_frequency
        print 'radar_radius', self.radar_radius
        print 'agent_position', self.agent_position
        print 'time', self.time

    def print_board(self):
        for (position, pokemons) in self.board.items():
            print position, pokemons


