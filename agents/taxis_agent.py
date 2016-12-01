# Taxis agent construct a probability distribution for the best spot on the board
# each spot on the board has some values associated with it

import random
import math
import sys
sys.path.insert(0, './../utils')
import configurations as cf
import utilities as ut
from scipy import stats


class Taxis_agent():
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


    def _sigmoid(self, x):
        return 1.0 / (1 + math.exp(x))


    def _sigmoid_gradient(self, sig):
        return sig * (1.0 - sig)


    def _new_prob(self, zero_out = False):
        new_prob = {}
        for x in range(self.board_size):
            for y in range(self.board_size):
                if zero_out:
                    new_prob[(x, y)] = 0
                else:
                    new_prob[(x, y)] = 1.0 / (self.board_size * self.board_size)
        return new_prob


    def _normalize_prob(self, prob):
        total = sum(prob.values())
        for x in range(self.board_size):
            for y in range(self.board_size):
                prob[(x, y)] /=  total


    # borders mark out the four values of the region border
    # only used to increase the probabilities
    def _increment_probs(self, borders, pokemon_id, learning_rate):
        # lazy construction
        if pokemon_id not in self.probs:
            self.probs[pokemon_id] = self._new_prob()

        (start_x, start_y, end_x, end_y) = borders
        learning_rate /= ((end_y - start_y) + (end_x - start_x))

        prob = self.probs[pokemon_id]
        for x in range(start_x, end_x):
            for y in range(start_y, end_y):
                prob[(x, y)] += learning_rate * self._sigmoid_gradient(prob[(x, y)])

        self._normalize_prob(prob)


    # position is only one position
    # could also be used to decrement the probability of that position
    # need to check the probability is still larger than 0
    def _increment_prob(self, position, pokemon_id, learning_rate):
        # lazy construction
        if pokemon_id not in self.probs:
            self.probs[pokemon_id] = self._new_prob()
        prob = self.probs[pokemon_id]
        prob[position] += learning_rate * self._sigmoid_gradient(prob[position])
        prob[position] = max(prob[position], 0)
        self._normalize_prob(prob)


    # knowing the source and destination of the agent, what is the action to take?
    def _get_direction(self, source, destination):
        if source == destination: return random.choice(self.legal_actions())
        actions = []
        if destination[0] > source[0]: actions.append('Right')
        if destination[0] < source[0]: actions.append('Left')
        if destination[1] > source[1]: actions.append('Up')
        if destination[1] < source[1]: actions.append('Down')
        return random.choice(actions)


    # the legal_actions function is provided by the board, no input is needed, the board
    # knows where the agent is now
    def get_action(self, state):
        self.num_iters += 1

        # explore
        if random.random() < self.exploration_prob or len(self.probs) == 0: 
            return random.choice(self.legal_actions())
        (agent_position, radar) = state

        # get the best action 
        # right now, just consider only the pokemons in radar
        # later, 2 things could be added, 
        # (1) weight the pokemons in radar, instead of just adding them
        # (2) also consider the other pokemons not in the radar, 
        voting_prob = self._new_prob(zero_out = True)
        for pokemon_id in radar:
            if pokemon_id in self.probs:
                for position in self.probs[pokemon_id].keys():
                    voting_prob[position] += self.probs[pokemon_id][position]

        if sum(voting_prob.values()) == 0: return random.choice(self.legal_actions())

        self._normalize_prob(voting_prob) 
        
        destination_selector = stats.rv_discrete(values = (range(self.board_size * self.board_size), voting_prob.values()))
        return self._get_direction(agent_position, voting_prob.keys()[destination_selector.rvs()])


    def incorperate_feedback(self, state, action, reward, pokemons_caught, new_state):
        # the game could last forever, so there is no end state defined
        (agent_position, radar) = state

        if len(radar) > 0:
            borders = ut.get_radar_region(agent_position, self.radar_radius, self.board_size)
            learning_rate = 1.0 / math.sqrt(self.num_iters)
            for pokemon_id in radar:
                # increment count for this pokemon
                if pokemon_id not in self.pokemon_count: self.pokemon_count[pokemon_id] = 0
                self.pokemon_count[pokemon_id] += 1

                # increase the probability of this pokemon for nearby regions
                self._increment_probs(borders, pokemon_id, 1)

                # decrease the probability of finding the pokemon in the radar but not here
                self._increment_prob(agent_position, pokemon_id, -1)

        for pokemon_id in pokemons_caught:
            self._increment_prob(agent_position, pokemon_id, 1)


