import csv
from gurobipy import *
import networkx as nx
from itertools import combinations
import matplotlib.pyplot as plt
import random
import scipy
import numpy as np


# import math
def get_data(filename,delimeter = ","):
    with open(filename, "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=delimeter)
        next(csv_reader)
        data = [line for line in csv_reader]

    return data

# Takes in a list of tuples with the first entries being non-protected and the last entry being protected
def make_graph(data, metric):
    G = nx.Graph()
    n = len(data)
    m = len(data[0])
    G.add_nodes_from([(i,dict(colour=data[i][m-1])) for i in range(n)]) #There's got to be a better way to do this
    G.add_weighted_edges_from([(i,j,metric(data[i][0:m],data[j][0:m])) for (i,j) in combinations(range(n),2)])
    return G

def euclidean_metric(point1, point2):

    if not len(point1) == len(point2):
        raise ValueError("The tuples arent the same length")

    return (sum([(point1[i] - point2[i])**2 for i in range(len(point1)-1)]))**(1/2)


def k_center(G,k):
    print("LP bulding")
    model = Model("k_center_OPT")
    x = {}
    y = {}
    # n = G.number_of_nodes()

    # print(G.edges)

    # Variables
    for v in G.nodes():
        y[v] = model.addVar(vtype=GRB.BINARY, name = "y_%s" % v)
        for u in G.nodes():
            x[u,v] = model.addVar(vtype = GRB.BINARY, name = "x_%s,%s" % (u,v))

    model.write("mymodel.lp")

    print("LP vars done")

    # Constraints
    for u in G.nodes():
        model.addConstr(quicksum(y[u] for u in G.nodes()) == k)
        for v in G.nodes():
            #print(str(v))
            model.addConstr(quicksum(x[u,v] for u in G[v]) + x[v,v] == 1)
            model.addConstr(x[u, v] <= y[u])
            if not (u, v) in G.edges and not u == v:
                model.addConstr(x[u, v] == 0)


    model.write("mymodel.lp")


    model.update()
    model.__data = x,y
    print("LP built")
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

   # data = get_data("bank.csv", ";")
    read_data = get_data("norm_data.txt",',')





    use_data = [(float(line[0]), float(line[1]), line[2]) for line in read_data]
    
    first_1000_data_points = use_data[:1000]

    try_data = use_data[:500]

    cents = 10

    print('Got everthing ready...')

    G = make_graph(use_data,euclidean_metric)

    print('Made graph...')

    edge_weights = list(set([tuple[2]['weight'] for tuple in G.edges(data = True)]))

    edge_weights.sort()

    print('Here we go!')

    lower = 0
    upper = len(edge_weights)

    final_answer = 0
    final_rad = 0

    while lower < upper:
        x = lower + (upper-lower)//2
        print('Trying radius: ' + str(edge_weights[x]) + '... at index ' + str(x))
        Gr = threshhold_graph(G,edge_weights[x])
        cM = k_center(Gr,cents)
        print('time to optimze!')
        cM.optimize()
        print('will i ever get here..')
        pM = cM
        if x != 0 and cM.status == GRB.Status.OPTIMAL:
            print('Trying pradius: ' + str(edge_weights[x-1]))
            Gr2 = threshhold_graph(G,edge_weights[x-1])
            pM = k_center(Gr2,cents)
            pM.optimize()

        if cM.status == GRB.Status.OPTIMAL and  pM.status != GRB.Status.OPTIMAL:
            final_answer = cM
            final_rad = edge_weights[x]
            lower = upper + 1
        elif cM.status == GRB.Status.OPTIMAL and pM.status == GRB.Status.OPTIMAL:
            upper = x
        else:
            if lower == x:
                break
            lower = x

    file1 = open("big_test.txt", "w")
    file1.write('RADIUS: ' + str(final_rad))

    if final_answer == 0:
        file1.write('No answer found..')
    else:
        for a in final_answer.getVars():
            file1.write(a.varName + " = " + str(a.x))





    # for v in model.getVars():
    #     print(v.varName)

if __name__ == '__main__':
        main()
