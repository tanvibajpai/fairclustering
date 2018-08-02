import networkx as nx
import random
import matplotlib.pyplot as plt

# fairly ratchet graph generator


# builds graph with num_nodes vertices
# adds edges with probability 1/p
def build_graph(num_nodes, p):
    G = nx.Graph()

    # add num_nodes nodes to G
    nodes = []
    for i in range(num_nodes):
        nodes.append(i)

    G.add_nodes_from(nodes)

    # add edges with probability 1/p
    for i in range(num_nodes):
        for j in range(i,num_nodes):
            curr = random.randint(1,p+1)
            if curr == 1:
              G.add_edge(i,j)

    return G

# draw graph and show in console
def draw_graph(G):
    nx.draw(G, with_labels=True)
    plt.show()
    return

G = build_graph(15,3)
draw_graph(G)
