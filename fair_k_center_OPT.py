from gurobipy import *
from networkx import *
import matplotlib.pyplot as plt

# import math


# Takes in a coloured, unweighted graph and the ratio constraints
# lowerbounds is a list of tuples (p1i, q1i) and upperbounds is a list of tuples (p2i,q2i)
def fair_k_center(G,k,lowerbounds,upperbounds):
    model = Model("k_center_OPT")
    x = {}
    y = {}
    # n = G.number_of_nodes()
    g = len(lowerbounds) #Number of colours

    # Variables
    for v in G.nodes():
        y[v] = model.addVar(vtype=GRB.BINARY, name = "y_%s" % v)
        for u in G.nodes():
            x[u,v] = model.addVar(vtype = GRB.BINARY, name = "x_%s,%s" % (u,v))

    # Constraints
    model.addConstr(quicksum(y[u] for u in G.nodes()) == k,"C1")
    for u in G.nodes():
        model.addConstr(quicksum(x[v, u] for v in G[u]) + x[u, u] == 1, "C2")
        for v in G.nodes():
            model.addConstr(x[u, v] <= y[u],"C3")
            if not (u, v) in G.edges and not u == v:
                model.addConstr(x[u, v] == 0,"C6")

    # model.write("mymodel.lp")

    colourdict = nx.get_node_attributes(G,"colour")
    print(colourdict)

    for i in range(1,g):

        p_1i, q_1i = lowerbounds[i]
        p_2i, q_2i = upperbounds[i]

        for u in G.nodes():
            # Constraint 4
            model.addConstr(p_1i*quicksum([x[u,v] for v in G.nodes() if colourdict[v] == 0]) <= q_1i*quicksum([x[u,v] for v in G.nodes() if colourdict[v] == i]),"C4")
            # model.write("mymodel.lp")

            # Constraint 5
            model.addConstr(p_2i*quicksum([x[u, v] for v in G.nodes() if colourdict[v] == 0]) >= q_2i * quicksum([x[u, v] for v in G.nodes() if colourdict[v] == i]),"C5")
            # model.write("mymodel.lp")

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
    G_r = complete_graph(3)
    # G_r = nx.path_graph(2)

    # NOTE: Colour 0 must be the majority colour
    colours = {0:0, 1:0, 2:1} #,3:0} #,4:1,5:0}
    lowerbounds = [(1,1),(1,1)]
    upperbounds = [(1,1),(1,1)]

    nx.set_node_attributes(G_r,colours,"colour")

    nx.draw(G_r)
    plt.show()

    k = 1
    model = fair_k_center(G_r,k,lowerbounds,upperbounds)
    model.write("mymodel.lp")
    model.optimize()
    # model.printAttr("X")
    for v in model.getVars():
        print(str(v.varName) + " \t| " + str(v.x))

if __name__ == '__main__':
        main()