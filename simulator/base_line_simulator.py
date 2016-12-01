import sys
sys.path.insert(0, './../agents')
import random_board
import regional_board
import base_line_agent
import improved_agent
import reflect_agent
sys.path.insert(0, './../utils')
import configurations as cf

# state for the problem is defined to be tuple (agent_position, radar)

def simulate(board, agent):
    bd = board()
    agent.legal_actions = bd.possible_moves
    total_rewards_received = 0
    total_pokemon_num_catched = 0

    old_state = (bd.agent_position, [])

    for _ in range(cf.NUM_ITERATIONS):
        action = agent.get_action(old_state)
        (reward, pokemon_caught, caught_num, radar) = bd.move_agent(action)
        agent.incorperate_feedback(old_state, action, reward, pokemon_caught, (bd.agent_position, radar))
        old_state = (bd.agent_position, radar)

        total_rewards_received += reward
        total_pokemon_num_catched += caught_num


    print bd.total_spawn_score, total_rewards_received, (total_rewards_received * 1.0 / bd.total_spawn_score)
    print bd.total_spawn_num, total_pokemon_num_catched, (total_pokemon_num_catched * 1.0 / bd.total_spawn_num)

# print 'base line agent'
# simulate(random_board.Random_board, base_line_agent.Base_line_agent())
# simulate(regional_board.Regional_board, base_line_agent.Base_line_agent())

# print 'improved agent'
# simulate(random_board.Random_board, improved_agent.Improved_agent())
# simulate(regional_board.Regional_board, improved_agent.Improved_agent())

print 'reflect agent'
simulate(random_board.Random_board, reflect_agent.Reflect_agent())
simulate(regional_board.Regional_board, reflect_agent.Reflect_agent())

#import cProfile
#import re
#cProfile.run('simulate(random_board.Random_board)')
