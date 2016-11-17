# test whether the selector works as desired
# print the results

import pokemon_selector

results = {}

s = pokemon_selector.Pokemon_selector()

for _ in range(30000):
	for (_, name) in s.get():
		if name not in results: results[name] = 0
		results[name] += 1

results = [(count, name) for (name, count) in results.items()]
results.sort()

for (count, name) in results:
	print name, count