from gurobipy import *
from networkx import *
# import math

def k_center(G,k):
    model = Model("k_center_OPT")
    x = {}
    y = {}
    n = G.number_of_nodes()

    for v in G.nodes(): #should this be replaced by range(n)?
        y[v] = model.addVar(vtype=GRB.BINARY, name = "y_%s" % v)
        model.addConstr(quicksum(x[u,v] for u in G[v]) == 1)     #Constraint 2
        for u in G.nodes():
            x[u,v] = model.addVar(vtype = GRB.BINARY, name = "x_%s,%s" % (u,v))
            model.addConstr(x[u,v] <= y[u])                      #Constraint 3
            if not (u,v) in G.edges():
                model.addConstr(x[u,v] == 0)                     #Constraint 6

    model.addConstr(quicksum(y) == k)                            #Constraint 1
    model.update()
    model.__data = x,y
    return model

# Given a weighted undirected graph G and a radius r,
# Returns an unweighted undirected graph G' with only
def threshhold_graph(G,r):
    G_r = nx.Graph()
    G_r.add_nodes_from(G.nodes)
    G_r.add_edges_from((u,v) for (u,v,d) in G.edges(data = True) if d["weight"] <= r)
    return G_r


if __name__ == '__main__':

    G = networkx.Graph()
    G.add_nodes_from([1,2,3,4,5])
    G.add_weighted_edges_from([(1,2,1),(2,3,2),(3,4,3),(4,5,4),(5,1,5)])

    r = 3
    G_r = threshhold_graph(G,r)

    k = 2
    k_center(G,k)