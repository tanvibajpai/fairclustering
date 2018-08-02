from gurobipy import *
import networkx as nx
import random
import matplotlib.pyplot as plt

def solver(num_nodes,p, k):
    M = Model()

    x = {}
    y = {}

    # y variable for each vertex
    for i in range(num_nodes):
        y[i] = M.addVar(vtype=GRB.BINARY, name="y(%d)" % i)

    # x variable for each possible edge
    for i in range(num_nodes):
        for j in range(num_nodes):
            x[(i,j)] = M.addVar(vtype=GRB.BINARY, name="x(%d,%d)" % (i,j))

    # x_ij <= y_i (3)
    for i in range(num_nodes):
        for j in range(num_nodes):
            M.addConstr(x[(i,j)] <= y[i])



    # every vertex must be serviced by at least one center (2)
    for i in range(num_nodes):
        M.addConstr((quicksum((x[(i,j)] + x[(j,i)]) for j in range(num_nodes))) == 1)

    # only k centers (1)
    M.addConstr((quicksum(y[i] for i in range(num_nodes))) == k)

    G = build_graph_model(num_nodes,p,M,x)



    M.optimize()

    if M.status == GRB.Status.OPTIMAL:
        ys = M.getAttr('x', y)

        for i in range(num_nodes):
             print("y" + str(i) + " = " + str(ys[i]))

        draw_centered_graph(G,ys,num_nodes)
    else:
        draw_graph(G)
    return M





def build_graph_model(num_nodes,p,M,x):
    G = nx.Graph()

    # add num_nodes nodes to G
    nodes = []
    for i in range(num_nodes):
        nodes.append(i)

    G.add_nodes_from(nodes)

    # add edges with probability 1/p (6)
    for i in range(num_nodes):
        for j in range(i, num_nodes):
            curr = random.randint(1, p)
            if i != j and curr == 1:
                G.add_edge(i, j)
            elif i != j:
                M.addConstr(x[(i,j)] == 0)
                M.addConstr(x[(j,i)] == 0)

    return G

def draw_graph(G):
    nx.draw(G, with_labels=True)
    plt.show()
    return

def draw_centered_graph(G,ys,num_nodes):
    blue = []
    red = []
    labels = {}
    for i in range(num_nodes):
        if ys[i] == 1.0:
            blue.append(i)
        else:
            red.append(i)
        labels[i] = i

   # print(str(nodes))

  #  nx.draw(G, with_labels = True)
    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, nodelist = blue, node_color = 'b',node_size=500)
    nx.draw_networkx_nodes(G, pos, nodelist = red, node_color = 'r',node_size=500)
    nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5)
    nx.draw_networkx_labels(G, pos, labels =labels, font_color= 'w', font_size=12,font_weight=4)
    plt.axis('off')
    plt.show()


M = solver(5,1,2)
M.write("test.lp")



