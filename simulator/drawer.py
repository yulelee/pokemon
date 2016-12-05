import sys
import base_line_simulator as bls
import oracle_simulator as os 
import matplotlib.pyplot as plt

import regional_board

sys.path.insert(0, './../agents')
import oracle_agent
import random_agent
import base_line_agent
import improved_agent
import reflect_agent
import taxis_agent

sys.path.insert(0, './../utils')
import configurations as cf

ITERATOIN_INTERVAL = cf.ITERATOIN_INTERVAL

print 'taxis agent'
ta_rates = bls.simulate(regional_board.Regional_board, taxis_agent.Taxis_agent())
plt.plot(range(len(ta_rates)), ta_rates, label = 'Taxis Agent')


print 'base line agent'
bs_rates = bls.simulate(regional_board.Regional_board, base_line_agent.Base_line_agent())
plt.plot(range(len(bs_rates)), bs_rates, label = 'Base Line Agent')


print 'improved agent'
ia_rates = bls.simulate(regional_board.Regional_board, improved_agent.Improved_agent())
plt.plot(range(len(ia_rates)), ia_rates, label = 'Improved Agent')


print 'reflect agent'
ra_rates = bls.simulate(regional_board.Regional_board, reflect_agent.Reflect_agent())
plt.plot(range(len(ra_rates)), ra_rates, label = 'Reflect Agent')


print 'oracle agent'
oa_rates = os.simulate(regional_board.Regional_board, oracle_agent.Oracle_agent)
plt.plot(range(len(oa_rates)), oa_rates, label = 'Oracle Agent')


print 'random agent'
ra_rates = os.simulate(regional_board.Regional_board, random_agent.Random_agent)
plt.plot(range(len(ra_rates)), ra_rates, label = 'Random Agent')


plt.title('All Agents Learning Curve - Ratio Of Pokemons')
plt.xlabel('Iterations (' + str(ITERATOIN_INTERVAL) + ')');
plt.ylabel('Ratio Of Pokemons Caught');
plt.legend()
plt.grid()
plt.show()

