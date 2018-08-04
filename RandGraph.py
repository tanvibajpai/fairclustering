import networkx as nx
import random
from itertools import combinations
import matplotlib.pyplot as plt


def generate_complete_graph(n):
    return generate_random_graph(n,1)

def generate_random_graph(n,p):
    G = nx.Graph()
    G.add_nodes_from(range(n))
    for edge in combinations(range(n),2):
        if random.random() <= p:
            G.add_edge(*edge)
    return G

def draw_graph(G):
    nx.draw(G,with_labels=True)
    plt.show()

def main():
    G = generate_random_graph(40,0.1)
    draw_graph(G)

if __name__ == "__main__":
    main()
