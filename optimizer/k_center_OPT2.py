from gurobipy import *
from networkx import *
import matplotlib.pyplot as plt

# import math

def k_center(G,k):
    model = Model("k_center_OPT")
    x = {}
    y = {}
    # n = G.number_of_nodes()

    # Variables
    for v in G.nodes():
        y[v] = model.addVar(vtype=GRB.BINARY, name = "y_%s" % v)
        for u in G.nodes():
            x[u,v] = model.addVar(vtype = GRB.BINARY, name = "x_%s,%s" % (u,v))

    # Constraints
    for u in G.nodes():
        model.addConstr(quicksum(y[u] for u in G.nodes()) == k)
        for v in G.nodes():
            model.addConstr(quicksum(x[u,v] for u in G[v]) + x[v,v] == 1)
            model.addConstr(x[u, v] <= y[u])
            if not (u, v) in G.edges and not u == v:
                model.addConstr(x[u, v] == 0)


    # model.addConstr(quicksum(y[u] for u in G.nodes()) == k) #Constraint 1
    #
    # for v in G.nodes():
    #     mylist = [x[u, v] for u in G[v]]
    #     sumlist = quicksum([x[u, v] for u in G[v]])
    #     nbrs = G[v]
    #     model.addConstr(quicksum([x[u,v] for u in G[v]]) + x[v,v] == 1) #Constraint 2
    #
    # for u in G.nodes():
    #     for v in G.nodes():
    #         model.addConstr(x[u, v] <= y[u]) # Constraint 3
    #
    # for u in G.nodes():
    #     for v in G.nodes():
    #         if not (u,v) in G.edges and not u == v:
    #             model.addConstr(x[u, v] == 0) # Constraint 6

    model.update()
    model.__data = x,y


    return model

def draw_graph(G):
    nx.draw(G,with_labels=True)
    plt.show()

# Given a weighted undirected graph G and a radius r,
# Returns an unweighted undirected graph G' with only
def threshhold_graph(G,r):
    G_r = nx.Graph()
    G_r.add_nodes_from(G.nodes)
    G_r.add_edges_from((u,v) for (u,v,d) in G.edges(data = True) if d["weight"] <= r)
    return G_r

def main():
    G = networkx.Graph()
    G.add_nodes_from([1,2,3,4,5])
    G.add_weighted_edges_from([(1,2,1),(2,3,2),(3,4,3),(4,5,4),(5,1,5)])

    r = 5
    # G_r = threshhold_graph(G,r)
    # G_r = complete_graph(6)
    G_r = cycle_graph(5)

    nx.draw(G_r)
    plt.show()

    k = 1
    model = k_center(G_r,k)
    model.write("kcenter.lp")
    model.optimize()

    # for v in model.getVars():
    #     print(str(v.varName) + " \t| " + str(v.x))

if __name__ == '__main__':
        main()