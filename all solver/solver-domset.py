import networkx as nx
from parse import *
from utils import is_valid_network, average_pairwise_distance
import sys
import os

def max_edge(G):
    weights = [d for (u, v, d) in G.edges(data=True)]
    max_w = max([i.get('weight') for i in weights])     # eg, 1.5 in test.in
    return [[u, v] for (u, v, d) in G.edges(data=True) if d.get('weight') == max_w][0]      # return [2, 3] for test.in

def set_mst(G, V):
    # Construct the tree with shortest path
    # (Minimum spanning tree within selected nodes)
    update = True
    mst = nx.minimum_spanning_tree(G)
    nodes = [n for n in mst.nodes]

    while update:
        updated = False
        for n in nodes:
            # if the node is a leaf and not in dominating set, remove it
            if mst.degree[n] == 1 and n not in V:
                mst.remove_node(n)
                nodes = [n for n in mst.nodes]
                updated = True
        update = updated
    # return an MST of dominating set
    return mst

def solve(G):
    """
    Args:
        G: networkx.Graph

    Returns:
        T: networkx.Graph
    """

    # TODO: your code here!

    """
    Second Algorithm
    1. Find all dominating set
        1.1 Find all paths between any 2 nodes in the dominating set
        1.2 Find shortest path
    # 2. Filter out non-tree set
    3. Select the minimum cost set
    """

    # Try every possible dominating set
    all_set = [] # 2-d list
    for n in G.nodes:
        dom_set = nx.dominating_set(G, n)
        # dominating set nodes
        temp = []
        for e in dom_set:
            temp.append(e)
        # Only add unique set
        if temp not in all_set:
            all_set.append(temp)


    # Compare all sets' cost
    all_mst = [set_mst(G, set) for set in all_set]
    cost = [average_pairwise_distance(mst) for mst in all_mst]
    min_ind = cost.index(min(cost))

    return all_mst[min_ind]


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

if __name__ == "__main__":
    output_dir = "outputs"
    input_dir = "inputs"
    for input_path in os.listdir(input_dir):
        graph_name = input_path.split(".")[0]
        G = read_input_file(f"{input_dir}/{input_path}")
        T = solve(G)
        write_output_file(T, f"{output_dir}/{graph_name}.out")
