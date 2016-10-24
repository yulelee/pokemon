import sys
sys.path.insert(0, './../agents')
import oracle_agent
import random_board

rb = random_board.random_board(20, verbose = False)
total_rewards_received = 0
total_pokemon_num_catched = 0

for _ in range(30000):
    (rewards, catched_num, _) = rb.move_agent(oracle_agent.oracle_agent.make_decision(rb))
    total_rewards_received += rewards
    total_pokemon_num_catched += catched_num

print rb.total_spawn_score, total_rewards_received, (total_rewards_received * 1.0 / rb.total_spawn_score)
print rb.total_spawn_num, total_pokemon_num_catched, (total_pokemon_num_catched * 1.0 / rb.total_spawn_num)



