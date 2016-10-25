# random agent calculate nothing, just return a random (but legal) move

import random

class Random_agent():
    @staticmethod
    def make_decision(board):
        return random.choice(board.possible_moves())


