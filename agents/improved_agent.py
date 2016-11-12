# base line agent use the basic Q-learning algorithm to decide which

import random
import math

# a semi-general q-learning algorithm for the pokemon go game,
# the state is represented by the current position, and the radar information
# the legal_action is defined by the board

class Improved_agent():
    def __init__(self, legal_actions = None, exploration_prob = 0.2):
        self.exploration_prob = exploration_prob
        self.weights = {}
        self.num_iters = 0
        self.last_radar = None

        # used to generalize my own model of pokemon preference
        self.pokemon_count = {}
        # kind of Laplace smoothing...
        self.pokemon_count[0] = 1

    def feature_extractor(self, state, action):
        (agent_position, radar) = state
        result = {key: 1 for key in enumerate(radar)}
        result[action] = 1
        #result['agent_position_x'] = agent_position[0]
        #result['agent_position_y'] = agent_position[1]
        return result


    def get_Q(self, state, action):
        return sum(self.weights.get(key, 0) * v for (key, v) in self.feature_extractor(state, action).items())

    # the legal_actions function is provided by the board, no input is needed, the board
    # knows where the agent is now
    def get_action(self, state):
        self.num_iters += 1
        legal_actions = self.legal_actions()
        if random.random() > self.exploration_prob:
            return max((self.get_Q(state, action), action) for action in legal_actions)[1]
        return random.choice(legal_actions)

    def get_stepsize(self):
        return 1.0 / math.sqrt(self.num_iters)

    def incorperate_feedback(self, state, action, reward, new_state):
        # the game could last forever, so there is no end state defined

        # add the current pokemons into the count, this is not the count being spawned,
        # just our own observation of what pokemon is everywhere and what is rare
        for pokemon_id in state[1]:
            if pokemon_id not in self.pokemon_count: self.pokemon_count[pokemon_id] = 0
            self.pokemon_count[pokemon_id] += 1

        if self.last_radar is not None:
            for pokemon_id in self.last_radar:
                if pokemon_id in state[1]: reward += 1.0 / self.pokemon_count[pokemon_id]


        best_Q_after_new_state = max(self.get_Q(new_state, new_action) for new_action in self.legal_actions())
        half_gradient = self.get_Q(state, action) - (reward + best_Q_after_new_state)

        for (key, v) in self.feature_extractor(state, action).items():
            self.weights[key] = self.weights.get(key, 0) - (self.get_stepsize() * half_gradient * v)

        last_radar = state[1]

