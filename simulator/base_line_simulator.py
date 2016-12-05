import sys
sys.path.insert(0, './../agents')
import random_board
import regional_board
import base_line_agent
import improved_agent
import reflect_agent
import taxis_agent
sys.path.insert(0, './../utils')
import configurations as cf

import matplotlib.pyplot as plt

# state for the problem is defined to be tuple (agent_position, radar)

ITERATOIN_INTERVAL = cf.ITERATOIN_INTERVAL

def simulate(board, agent):
    bd = board()
    agent.legal_actions = bd.possible_moves
    total_rewards_received = 0
    total_pokemon_num_catched = 0

    interval_rewards_received_list = []
    interval_pokemon_num_catched_list = []
    interval_catching_rate_list = []
    cumulative_catching_rate_list = []

    total_rewards_received_commit = 0
    total_pokemon_num_catched_commit = 0
    total_spawn_num_commit = 0

    old_state = (bd.agent_position, [])

    for i in range(cf.NUM_ITERATIONS):

        action = agent.get_action(old_state)
        (reward, pokemon_caught, caught_num, radar) = bd.move_agent(action)
        agent.incorperate_feedback(old_state, action, reward, pokemon_caught, (bd.agent_position, radar))
        old_state = (bd.agent_position, radar)

        total_rewards_received += reward
        total_pokemon_num_catched += caught_num

        if i % ITERATOIN_INTERVAL == 0:
            interval_rewards_received = total_rewards_received - total_rewards_received_commit
            interval_pokemon_num_catched = total_pokemon_num_catched - total_pokemon_num_catched_commit
            interval_total_spawn_num = bd.total_spawn_num - total_spawn_num_commit

            print 'At iteration', i, 'Scores:', interval_rewards_received, 'Pokemons:', interval_pokemon_num_catched
            print 'Cumulative Catching rate:', (total_pokemon_num_catched * 1.0 / bd.total_spawn_num)
            print 'Interval Catching rate:', (interval_pokemon_num_catched * 1.0 / (interval_total_spawn_num ))

            interval_rewards_received_list.append(interval_rewards_received)
            interval_pokemon_num_catched_list.append(interval_pokemon_num_catched)
            interval_catching_rate_list.append(interval_pokemon_num_catched * 1.0 / (interval_total_spawn_num))
            cumulative_catching_rate_list.append(total_pokemon_num_catched * 1.0 / bd.total_spawn_num)            

            total_rewards_received_commit = total_rewards_received
            total_pokemon_num_catched_commit = total_pokemon_num_catched
            total_spawn_num_commit = bd.total_spawn_num


    print bd.total_spawn_score, total_rewards_received, (total_rewards_received * 1.0 / bd.total_spawn_score)
    print bd.total_spawn_num, total_pokemon_num_catched, (total_pokemon_num_catched * 1.0 / bd.total_spawn_num)

    # plt.plot(range(len(interval_pokemon_num_catched_list)), interval_pokemon_num_catched_list,);
    # plt.title('Taxis Agent Learning Curve - Number Of Pokemons')
    # plt.xlabel('Iterations (' + str(ITERATOIN_INTERVAL) + ')');
    # plt.ylabel('Number Of Pokemons Caught');
    # plt.grid()
    # plt.show()
    # plt.plot(range(len(interval_rewards_received_list)), interval_rewards_received_list);
    # plt.grid()
    # plt.show()
    # plt.plot(range(len(cumulative_catching_rate_list)), cumulative_catching_rate_list, label = 'Cumulative');
    # plt.plot(range(len(interval_catching_rate_list)), interval_catching_rate_list, label = 'Interval');
    # plt.title('Taxis Agent Learning Curve - Ratio Of Pokemons')
    # plt.xlabel('Iterations (' + str(ITERATOIN_INTERVAL) + ')');
    # plt.ylabel('Ratio Of Pokemons Caught');
    # plt.legend()
    # plt.grid()
    # plt.show()

    return cumulative_catching_rate_list

# print 'base line agent'
# simulate(random_board.Random_board, base_line_agent.Base_line_agent())
# simulate(regional_board.Regional_board, base_line_agent.Base_line_agent())

# print 'improved agent'
# simulate(random_board.Random_board, improved_agent.Improved_agent())
# simulate(regional_board.Regional_board, improved_agent.Improved_agent())

# print 'reflect agent'
# simulate(random_board.Random_board, reflect_agent.Reflect_agent())
# simulate(regional_board.Regional_board, reflect_agent.Reflect_agent())

# print 'taxis agent'
# simulate(random_board.Random_board, taxis_agent.Taxis_agent())
simulate(regional_board.Regional_board, taxis_agent.Taxis_agent())

#import cProfile
#import re
#cProfile.run('simulate(random_board.Random_board)')
