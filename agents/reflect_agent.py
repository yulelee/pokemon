# Reflect agent construct a probability distribution of where the pokemons might be,
# looking at the radar information, it goes to the direction it think is best

import random
import math


class Reflect_agent():
    def __init__(self, legal_actions = None, exploration_prob = 0.2, verbose = False):
        # still explore
        self.exploration_prob = exploration_prob
        self.verbose = verbose
        self.weights = {}
        self.num_iters = 0

        # used to generalize my own model of pokemon preference
        self.pokemon_count = {}
        # kind of Laplace smoothing...
        self.pokemon_count[0] = 1

        # probabilities
        self.centers = {}


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
        if random.random() < self.exploration_prob: return random.choice(self.legal_actions())
        (agent_position, radar) = state
        direction_vote = {}
        for pokemon in radar:
            if pokemon in self.centers:
                action = self._get_direction(agent_position, self.centers[pokemon])
                if action not in direction_vote: direction_vote[action] = 0
                direction_vote[action] += 1

        if len(direction_vote) > 0: 
            directions = [(votes, direction) for (direction, votes) in direction_vote.items()]
            directions.sort()
            directions.reverse()
            return directions[0][1]
        return random.choice(self.legal_actions())
        

    def incorperate_feedback(self, state, action, reward, pokemons_caught, new_state):
        # the game could last forever, so there is no end state defined
        (agent_position, radar) = state

        for pokemon_id in radar:
            if pokemon_id not in self.pokemon_count: self.pokemon_count[pokemon_id] = 0
            self.pokemon_count[pokemon_id] += 1

        for pokemon_caught in pokemons_caught:
            # firstly added
            if pokemon_caught not in self.centers: self.centers[pokemon_caught] = agent_position
            else:
                # change the new center to the middle point
                old_position = self.centers[pokemon_caught]
                self.centers[pokemon_caught] = (int(0.5 * (old_position[0] + agent_position[0])), \
                                                int(0.5 * (old_position[1] + agent_position[1])))
            if self.verbose:
                print 'pokemon', pokemons_caught, 'caught, now the center at:', self.centers[pokemon_caught]




