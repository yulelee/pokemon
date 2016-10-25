import sys
sys.path.insert(0, './../agents')
import oracle_agent
import random_board
import random_agent

# oracle agent and random agent has the same interface, so we can use
# the same simualtor to simulate them

def simulate(agent):
    rb = random_board.random_board(50, verbose = False)
    total_rewards_received = 0
    total_pokemon_num_catched = 0

    for _ in range(3000):
        (rewards, catched_num, _) = rb.move_agent(agent.make_decision(rb))
        total_rewards_received += rewards
        total_pokemon_num_catched += catched_num

    print rb.total_spawn_score, total_rewards_received, (total_rewards_received * 1.0 / rb.total_spawn_score)
    print rb.total_spawn_num, total_pokemon_num_catched, (total_pokemon_num_catched * 1.0 / rb.total_spawn_num)

simulate(oracle_agent.oracle_agent)
simulate(random_agent.Random_agent)

