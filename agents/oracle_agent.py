# an oracle agent knows about everything on the board, it know the all the positions, types, rewards of pokemons,
# and their disappearing time, it make the optimal decision based on the current situation on the board.

import sys
sys.path.insert(0, './../utils')
sys.path.insert(0, './../simulator')
import heapq
import random
from data_types import pokemon_spawn

class Graph_node():
    def __init__(self, position, total_rewards, time_remains, parent = None):
        self.position = position
        self.total_rewards = total_rewards
        self.best_cumulative_rewards = total_rewards
        self.time_remains = time_remains

        # all the edges is stored here, this is a weighted graph, but do not the store the weights
        # explicitly, the total_rewards of the node at next_hop is the weight of this edge.
        # and we're actually computing the longest path here
        self.next_hop = []
        self.parent = parent

        # used by DFS visit
        self.DFS_visited = False

    def _manhattan_distance(self, p1, p2):
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

    def is_reachable(self, other_node):
        return self._manhattan_distance(self.position, other_node.position) < other_node.time_remains - self.time_remains

    def __str__(self):
        return str(self.position) + '; time:' + str(self.time_remains) + '; next_hop:' + str(self.next_hop)

    def __repr__(self):
        return self.__str__()

class Oracle_agent():

    @staticmethod
    def make_decision(board):
        # gather information from the board
        agent_position = board.agent_position
        board_information = board.board
        pokemon_scores = board.scores


        # if there is no pokemon, just return a random direction
        if len(board_information) == 0:
            return random.choice(board.possible_moves())

        agent_node = Graph_node(agent_position, 0, 0)
        all_nodes_reachable = []

        # construct the graph
        for (position, pokemon_list) in board_information.items():
            # sort the pokemons by the time_remaining, the most short living pokemon at the front
            time_sorted_pokemons = sorted(pokemon_list, key = lambda x: x.time_remains)
            total_rewards = 0
            for pokemon in time_sorted_pokemons:
                total_rewards += pokemon_scores[pokemon.pokemon_id - 1]
                node = Graph_node(position, total_rewards, pokemon.time_remains, agent_node)
                if agent_node.is_reachable(node): all_nodes_reachable.append(node)


        # if no node is reachable, equivalent to no pokemon
        if len(all_nodes_reachable) == 0:
            return random.choice(board.possible_moves())

        # only the nodes that are reachable from the agent is considered,
        # now construct all the edges
        for node in all_nodes_reachable:
            for other_node in all_nodes_reachable:
                if node.position != other_node.position and node.is_reachable(other_node):
                    node.next_hop.append(other_node)

        # topology sort on the nodes
        sorted_nodes = []

        def DFS_visit(node):
            if not node.DFS_visited:
                node.DFS_visited = True
                for next_hop in node.next_hop:
                    DFS_visit(node)
                sorted_nodes.append(node)

        for node in all_nodes_reachable:
            DFS_visit(node)

        sorted_nodes = list(reversed(sorted_nodes))

        # compute the longest path
        for node in sorted_nodes:
            for next_hop in node.next_hop:
                if node.best_cumulative_rewards + next_hop.total_rewards > next_hop.best_cumulative_rewards:
                    next_hop.parent = node
                    next_hop.best_cumulative_rewards = node.best_cumulative_rewards + next_hop.total_rewards

        # reverse engineer to find the origin of this path
        best_destination = max(sorted_nodes, key = lambda x: x.best_cumulative_rewards)
        while best_destination.parent != agent_node:
            best_destination = best_destination.parent

        if best_destination.position[0] < agent_position[0]: return 'Left'
        if best_destination.position[0] > agent_position[0]: return 'Right'
        if best_destination.position[1] < agent_position[1]: return 'Down'
        if best_destination.position[1] > agent_position[1]: return 'Up'

