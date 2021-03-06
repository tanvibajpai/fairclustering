from gurobipy import *
from networkx import *
import matplotlib.pyplot as plt
# import math


# Takes in unweighted graph and k
def dominating_set(G,k):
    model = Model("Dominating_Set")

    y = {}
    # n = G.number_of_nodes()

    # Variables
    for u in G.nodes():
        y[u] = model.addVar(vtype = GRB.BINARY, name = "y_%s" % u)

    # Constraints
    model.addConstr(quicksum(y[u] for u in G.nodes) <= k)

    for v in G.nodes():
        model.addConstr(quicksum(y[u] for u in G.neighbors(v)) + y[v] >= 1, "C_%s" % v)

    model.write("dominating_set.lp")

    model.update()
    model.__data = y
    return model

# Takes in unweighted graph and k
def dominating_set_dominated_by_our_centers(G,S,k):
    model = dominating_set(G,k)

    y = model.__data
    # n = G.number_of_nodes()

    # # Variables
    # for u in G.nodes():
    #     y[u] = model.addVar(vtype = GRB.BINARY, name = "y_%s" % u)
    #
    # # Constraints
    # model.addConstr(quicksum(y[u] for u in G.nodes) <= k)
    #
    # for v in G.nodes():
    #     model.addConstr(quicksum(y[u] for u in G.neighbors(v)) + y[v] >= 1, "C_%s" % v)

    # Constraint encoding the fact that the dominating set has to be dominated by our centers:
    # nodes not dominated by our centers cannot be selected:
    S = set(S)
    for u in set(G.nodes()).difference(S):
        if not S.intersection(G.neighbors(u)):
            model.addConstr(y[u] == 0)

    model.write("dominating_set_dominated_by_our_centers.lp")

    model.update()
    model.__data = y
    return model


def draw_graph(G):
    nx.draw(G,with_labels=True)
    plt.show()

# Given a weighted undirected graph G and a radius r,
# Returns an unweighted undirected graph G' with only edges less than r
def threshhold_graph(G,r):
    G_r = nx.Graph()
    G_r.add_nodes_from(G.nodes)
    G_r.add_edges_from((u,v) for (u,v,d) in G.edges(data = True) if d["weight"] <= r)
    return G_r

def main():
    # G = networkx.Graph()
    # G.add_nodes_from([1,2,3,4,5])
    # G.add_weighted_edges_from([(1,2,1),(2,3,2),(3,4,3),(4,5,4),(5,1,5)])
    #
    # r = 5


    # G_r = threshhold_graph(G,r)
    # G_r = complete_graph(8)
    G_r = nx.cycle_graph(5)
    k = 2
    S = set([1])
    draw_graph(G_r)

    model = dominating_set_dominated_by_our_centers(G_r,S,k)
    model.optimize()
    # model.printAttr("X")
    for v in model.getVars():
        print(str(v.varName) + " \t| " + str(v.x))

if __name__ == '__main__':
        main()
