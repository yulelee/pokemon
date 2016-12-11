# Taxis agent construct a probability distribution for the best spot on the board
# each spot on the board has some values associated with it

import random
import math
import sys
sys.path.insert(0, './../utils')
import configurations as cf
import utilities as ut
from scipy import stats


import matplotlib.pyplot as plt
import numpy as np


class Taxis_agent_two():
    def __init__(self, legal_actions = None, exploration_prob = cf.EXPLORATION_RATE, verbose = cf.AGENT_VERBOSE):
        # still explore

        self.num_iters = 0
        self.exploration_prob = exploration_prob
        self.verbose = verbose

        # the agent has the right to know the size of the board and the radius of the radar
        self.radar_radius = cf.MINIMUM_RADAR_SIZE
        self.board_size = cf.WORLD_SIZE

        # a dictionary, using the pokemon_id as the key, maps to the probability grid 
        # of this type of pokemon, each prob is also a dictionary, with the coordinates 
        # of all of the positions on the board as the key, and the probability of 
        # that pokemon appears on that position as the value
        self.probs = {}

        # used to generalize my own model of pokemon preference
        self.pokemon_count = {}
        self.total_pokemon_count = 0


        # propose a new counter, just count when the pokemon is caught at a place
        self.mixed_probs = ut._new_prob


        # initialize the weights
        self.weights = {}
        for p_id in range(152):
            self.weights[p_id] = {'x': 0, 'y': 0, 'x_sqr': 0, 'y_sqr': 0, 'xy': 0, '1': 0}


    def _sigmoid(self, x):
        return 1.0 / (1 + math.exp(- x))


    def _normalize_prob(self, prob):
        total = sum(prob.values())
        for position in prob:
            prob[position] /=  total


    def _exp_prob(self, prob):
        for position in prob:
            prob[position] = math.exp(prob[position])


    def _max_in_prob(self, prob):
        max_prob = -1
        best_position = None
        for position in prob:
            if prob[position] < max_prob:
                max_prob = prob[position]
                best_position = position

        return position


    def _feature_extract(self, x, y):
        x = (x - 0.5 * self.board_size) / self.board_size
        y = (y - 0.5 * self.board_size) / self.board_size
        return {'x': x, 'y': y, 'x_sqr': x ** 2, 'y_sqr': y ** 2, 'xy': x * y, '1': 1}

    def _get_prob(self, features, pokemon_id):
        # print features
        # print self.weights[pokemon_id]
        # print sum(self.weights[pokemon_id][key] * features[key] for key in features)
        return self._sigmoid(sum(self.weights[pokemon_id][key] * features[key] for key in features))

    # knowing the source and destination of the agent, what is the action to take?
    def _get_direction(self, source, destination):
        if source == destination: return random.choice(self.legal_actions())
        actions = []
        if destination[0] > source[0]: actions.append('Right')
        if destination[0] < source[0]: actions.append('Left')
        if destination[1] > source[1]: actions.append('Up')
        if destination[1] < source[1]: actions.append('Down')
        return random.choice(actions)


    def _normalize_weights(self):
        for (key, weights) in self.weights.items():
            norm = math.sqrt(sum(weight ** 2 for weight in weights.values()))
            if norm > 0:
                self.weights[key] = {feature_name: weight / norm for (feature_name, weight) in weights.items()}

    # the legal_actions function is provided by the board, no input is needed, the board
    # knows where the agent is now
    def get_action(self, state):
        self.num_iters += 1

        if self.num_iters % 100 == 0: self._normalize_weights()

        # HEATMAP
        if self.num_iters % cf.ITERATOIN_INTERVAL == 0:

            print self.pokemon_count
            image = [[0 for _ in range(self.board_size)] for _ in range(self.board_size)]
            for x in range(self.board_size):
                for y in range(self.board_size):
                    image[x][y] = self._get_prob(self._feature_extract(x, y), 16)
            print self.weights[16]
            plt.imshow(image, cmap='hot', interpolation='nearest')
            plt.show()

        # if self.num_iters % 10 == 0: print state[0]

        # explore
        if random.random() < self.exploration_prob or len(self.probs) == 0: 
            return random.choice(self.legal_actions())
        
        (agent_position, radar) = state

        # get the best action 
        # right now, just consider only the pokemons in radar
        # later, 2 things could be added, 
        # (1) weight the pokemons in radar, instead of just adding them
        # (2) also consider the other pokemons not in the radar, 
        voting_prob = ut._new_prob(zero_out = True)
        for pokemon_id in radar:
            if pokemon_id in self.probs:
                (start_x, start_y, end_x, end_y) = ut.get_radar_region(agent_position, self.radar_radius, self.board_size)
                for x in range(start_x, end_x):
                    for y in range(start_y, end_y):
                        voting_prob[(x, y)] += self._get_prob(self._feature_extract(x, y), pokemon_id)

        if sum(voting_prob.values()) == 0: return random.choice(self.legal_actions())

        # self._exp_prob(voting_prob)
        self._normalize_prob(voting_prob)

        destination_selector = stats.rv_discrete(values = (range(self.board_size * self.board_size), voting_prob.values()))
        return self._get_direction(agent_position, voting_prob.keys()[destination_selector.rvs()])


    def incorperate_feedback(self, state, action, reward, pokemons_caught, new_state):
        # the game could last forever, so there is no end state defined
        (agent_position, radar) = new_state
        (start_x, start_y, end_x, end_y) = ut.get_radar_region(agent_position, self.radar_radius, self.board_size)
        radar = set(radar)
        pokemons_caught = set(pokemons_caught)


        for pokemon_id in radar:
            # increment count for this pokemon
            if pokemon_id not in self.pokemon_count: self.pokemon_count[pokemon_id] = 0
            self.pokemon_count[pokemon_id] += 1
            self.total_pokemon_count += 1
            for x in range(start_x, end_x):
                for y in range(start_y, end_y):
                    phi = self._feature_extract(x, y)
                    # update weights
                    for key in phi:
                        self.weights[pokemon_id][key] += 0.00001 * phi[key]


        agent_phi = self._feature_extract(agent_position[0], agent_position[1])

        # for pokemon_id in range(151):
        #     if pokemon_id not in radar:
        #         for key in phi:
        #             self.weights[pokemon_id][key] -= 0.00001 * phi[key]
        #     if pokemon_id


        for pokemon_id in range(151):
            if pokemon_id in pokemons_caught:
                for x in range(start_x, end_x):
                    for y in range(start_y, end_y):
                        mht_dis = abs(agent_position[0] - x) + abs(agent_position[1] - y)
                        phi = self._feature_extract(x, y)
                        for key in phi:
                            self.weights[pokemon_id][key] += 0.001 * math.exp(- mht_dis) * phi[key]
            elif pokemon_id not in radar:
                if random.random() < self.pokemon_count.get(pokemon_id, 0) / (self.total_pokemon_count + 1.0) * 1.4:
                    for x in range(start_x, end_x):
                        for y in range(start_y, end_y):
                            phi = self._feature_extract(x, y)
                            # mht_dis = abs(agent_position[0] - x) + abs(agent_position[1] - y)
                            for key in phi:
                                self.weights[pokemon_id][key] -= 0.00001 * phi[key]

