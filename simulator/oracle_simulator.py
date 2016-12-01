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

def simulate(board, agent):
    rb = board()
    total_rewards_received = 0
    total_pokemon_num_catched = 0

    for _ in range(cf.NUM_ITERATIONS):
        (rewards, pokemons_caught, catched_num, _) = rb.move_agent(agent.make_decision(rb))
        total_rewards_received += rewards
        total_pokemon_num_catched += catched_num

    print rb.total_spawn_score, total_rewards_received, (total_rewards_received * 1.0 / rb.total_spawn_score)
    print rb.total_spawn_num, total_pokemon_num_catched, (total_pokemon_num_catched * 1.0 / rb.total_spawn_num)

simulate(random_board.Random_board, oracle_agent.Oracle_agent)
simulate(random_board.Random_board, random_agent.Random_agent)

simulate(regional_board.Regional_board, oracle_agent.Oracle_agent)
simulate(regional_board.Regional_board, random_agent.Random_agent)

