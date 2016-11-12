import sys
sys.path.insert(0, './../agents')
import random_board
import regional_board
import base_line_agent
import improved_agent

# state for the problem is defined to be tuple (agent_position, radar)

def simulate(board, agent):
    bd = board(50, verbose = False)
    agent.legal_actions = bd.possible_moves
    total_rewards_received = 0
    total_pokemon_num_catched = 0

    old_state = (bd.agent_position, [])

    for _ in range(8000):
        action = agent.get_action(old_state)
        (reward, caught_num, radar) = bd.move_agent(action)
        agent.incorperate_feedback(old_state, action, 1, (bd.agent_position, radar))
        old_state = (bd.agent_position, radar)

        total_rewards_received += reward
        total_pokemon_num_catched += caught_num


    print bd.total_spawn_score, total_rewards_received, (total_rewards_received * 1.0 / bd.total_spawn_score)
    print bd.total_spawn_num, total_pokemon_num_catched, (total_pokemon_num_catched * 1.0 / bd.total_spawn_num)

simulate(random_board.Random_board, base_line_agent.Base_line_agent())
simulate(regional_board.Regional_board, base_line_agent.Base_line_agent())

simulate(random_board.Random_board, improved_agent.Improved_agent())
simulate(regional_board.Regional_board, improved_agent.Improved_agent())

#import cProfile
#import re
#cProfile.run('simulate(random_board.Random_board)')
