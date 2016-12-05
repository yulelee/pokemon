import sys
sys.path.insert(0, './../agents')
import oracle_agent
import random_board
import random_agent
import regional_board
sys.path.insert(0, './../utils')
import configurations as cf

# oracle agent and random agent has the same interface, so we can use
# the same simualtor to simulate them

ITERATOIN_INTERVAL = cf.ITERATOIN_INTERVAL

def simulate(board, agent):
    rb = board()

    total_rewards_received = 0
    total_pokemon_num_catched = 0

    interval_rewards_received_list = []
    interval_pokemon_num_catched_list = []
    interval_catching_rate_list = []
    cumulative_catching_rate_list = []

    total_rewards_received_commit = 0
    total_pokemon_num_catched_commit = 0
    total_spawn_num_commit = 0

    for i in range(cf.NUM_ITERATIONS):
        (rewards, pokemons_caught, catched_num, _) = rb.move_agent(agent.make_decision(rb))
        total_rewards_received += rewards
        total_pokemon_num_catched += catched_num


        if i % ITERATOIN_INTERVAL == 0:
            interval_rewards_received = total_rewards_received - total_rewards_received_commit
            interval_pokemon_num_catched = total_pokemon_num_catched - total_pokemon_num_catched_commit
            interval_total_spawn_num = rb.total_spawn_num - total_spawn_num_commit

            print 'At iteration', i, 'Scores:', interval_rewards_received, 'Pokemons:', interval_pokemon_num_catched
            print 'Cumulative Catching rate:', (total_pokemon_num_catched * 1.0 / rb.total_spawn_num)
            print 'Interval Catching rate:', (interval_pokemon_num_catched * 1.0 / (interval_total_spawn_num ))

            interval_rewards_received_list.append(interval_rewards_received)
            interval_pokemon_num_catched_list.append(interval_pokemon_num_catched)
            interval_catching_rate_list.append(interval_pokemon_num_catched * 1.0 / (interval_total_spawn_num))
            cumulative_catching_rate_list.append(total_pokemon_num_catched * 1.0 / rb.total_spawn_num)            

            total_rewards_received_commit = total_rewards_received
            total_pokemon_num_catched_commit = total_pokemon_num_catched
            total_spawn_num_commit = rb.total_spawn_num



    print rb.total_spawn_score, total_rewards_received, (total_rewards_received * 1.0 / rb.total_spawn_score)
    print rb.total_spawn_num, total_pokemon_num_catched, (total_pokemon_num_catched * 1.0 / rb.total_spawn_num)

    return cumulative_catching_rate_list

# simulate(random_board.Random_board, oracle_agent.Oracle_agent)
# simulate(random_board.Random_board, random_agent.Random_agent)

# simulate(regional_board.Regional_board, oracle_agent.Oracle_agent)
# simulate(regional_board.Regional_board, random_agent.Random_agent)

