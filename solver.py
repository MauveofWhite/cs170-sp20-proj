import networkx as nx
from parse import *
from utils import is_valid_network, average_pairwise_distance
import sys
import os

def max_edge(G):
    weights = [d for (u, v, d) in G.edges(data=True)]
    max_w = max([i.get('weight') for i in weights])     # eg, 1.5 in test.in
    return [[u, v] for (u, v, d) in G.edges(data=True) if d.get('weight') == max_w][0]      # return [2, 3] for test.in

def solve(G):
    """
    Args:
        G: networkx.Graph

    Returns:
        T: networkx.Graph
    """

    # TODO: your code here!

    """
    First Algorithm
    1. MST
    2. update = True
    while (updated == True):
        for loop iterate |E| times:
            update = False
            e = max(edge)
            if (remove(e) disconnect or invalidate(G)):
                exclude(e)
                continue
            if (cost(remove(e)) <= cost(g)):
                remove(e)
                update = True
    return G

    def disconnect():
    def invalidate(): is_valid_network(G, T)
    def cost(): average_pairwise_distance(T)

    """

    # MST
    T = nx.minimum_spanning_tree(G)

    # Update
    update = True
    # count = 0
    while update == True:
        # count += 1
        avaliable_edge = T.copy()
        update = False
        updated = False     # as long as current tree is modified, this is set to be True
        for i in range(T.number_of_edges()):
            # First compute the max edge avaliable
            e = max_edge(avaliable_edge)
            # Try remove the edge
            node_to_remove = None
            test = T.copy()
            test.remove_edge(e[0], e[1])
            if (test.degree[e[0]] == 0):
                test.remove_node(e[0])
                node_to_remove = e[0]
            else:
                test.remove_node(e[1])
                node_to_remove = e[1]

            # print(i, "-th iteration, try remove ", e[0], " and ", e[1])
            # Check if remove is valid and helpful
            if not is_valid_network(G, test):
                avaliable_edge.remove_edge(e[0], e[1])
                # print(i, "               can't remove ", e[0], " and ", e[1])
                # print()
                continue
            if average_pairwise_distance(test) < average_pairwise_distance(T):
                # print("                 previous cost: ", average_pairwise_distance(T))
                # print("                 After removing cost: ", average_pairwise_distance(test))
                T.remove_node(node_to_remove)
                avaliable_edge.remove_edge(e[0], e[1])
                updated = True
                # print(i, "               can remove ", e[0], " and ", e[1])
                # print()
                # continue      # do not start over
                break           # start over

        # Keep iterate
        update = updated
        # print(count, "-th iteration")

    # T.remove_edge(0, 1) # leave node 0 alone with degree 0
    # T.remove_node(0) # remove e(0, 1) automatically
    # T.remove_node(0)

    return T

# Here's an example of how to run your solver.

# Usage: python3 solver.py test.in

# if __name__ == '__main__':
#     assert len(sys.argv) == 2
#     path = sys.argv[1]
#     G = read_input_file(path)
#     T = solve(G)
#     assert is_valid_network(G, T)
#     print("Average  pairwise distance: {}".format(average_pairwise_distance(T)))
#     write_output_file(T, 'out/test.out')
#     # print(T)
#
if __name__ == "__main__":
    output_dir = "outputs"
    input_dir = "inputs"
    for input_path in os.listdir(input_dir):
        graph_name = input_path.split(".")[0]
        G = read_input_file(f"{input_dir}/{input_path}")
        T = solve(G)
        write_output_file(T, f"{output_dir}/{graph_name}.out")
