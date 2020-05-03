import networkx as nx
from parse import *
from utils import is_valid_network, average_pairwise_distance
import sys
import os
from networkx.algorithms import approximation
from networkx.algorithms.approximation import *

# Find the maximum length of edge in G
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

# Computes the length of a path
def path_length(G, path):
    weight = 0
    for i in range(len(path)-1):
        s = path[i]
        t = path[i+1]
        for (u, v, d) in G.edges(data=True):
            if (s==u and t==v) or (s==v and t==u):
                weight += d.get('weight')
    return weight

# Computes the total distance from a vertex to other vertex in G
def vertex_total_length(G, v):
    nodes = [n for n in G.nodes]
    weight = 0
    for i in nodes:
        path = nx.shortest_path(G, source=v, target=i)
        weight += path_length(G, path)
    return weight

# Return the median vertex
def median_vertex(G):
    nodes = [n for n in G.nodes]
    median = [vertex_total_length(G, n) for n in nodes]
    return nodes[median.index(min(median))]

# Add a path in T with weight in G
def add_path(T, path, G):
    for i in range(len(path)-1):
        s = path[i]
        t = path[i+1]
        for (u, v, d) in G.edges(data=True):
            if (s==u and t==v) or (s==v and t==u):
                w = d.get('weight')
                break
        T.add_edge(s, t, weight=w)

def BFS(G, s):
    # Mark all the vertices as not visited
    visited = [False] * (len(G.nodes))

    # Create a queue for BFS
    queue = []
    order = []
    # Mark the source node as
    # visited and enqueue it
    queue.append(s)
    visited[s] = True


    while queue:
        # Dequeue a vertex from
        # queue and print it
        s = queue.pop(0)
        start = s
        # Get all adjacent vertices of the
        # dequeued vertex s. If a adjacent
        # has not been visited, then mark it
        # visited and enqueue it
        for i in G.neighbors(s):
            if visited[i] == False:
                queue.append(i)
                visited[i] = True
                end = i
                order.append([start, end])
    return order

def update(T):
        # Update
        update = True
        while update == True:
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
                    continue      # do not start over
                    # break           # start over

            # Keep iterate
            update = updated


def solve(G):
    """
    Args:
        G: networkx.Graph

    Returns:
        T: networkx.Graph
    """

    # TODO: your code here!

    """


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
    T = all_mst[min_ind]
    update(T)

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

if __name__ == "__main__":
    output_dir = "outputs"
    input_dir = "inputs"
    for input_path in os.listdir(input_dir):
        graph_name = input_path.split(".")[0]
        G = read_input_file(f"{input_dir}/{input_path}")
        T = solve(G)
        write_output_file(T, f"{output_dir}/{graph_name}.out")
