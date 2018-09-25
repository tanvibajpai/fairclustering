from gurobipy import *
from networkx import *
import csv
from itertools import combinations
import matplotlib.pyplot as plt
import k_center_OPT2
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


# Takes in a coloured, unweighted graph and the ratio constraints
# lowerbounds is a list of tuples (p1i, q1i) and upperbounds is a list of tuples (p2i,q2i)
def fair_k_center(G,k,lowerbounds,upperbounds):
    model = k_center_OPT2.k_center(G,k)
    # HOW TO RENAME THE FUCKING MODEL

    x = model.__data[0]
    y = model.__data[1]
    g = len(lowerbounds) #Number of colours


    model.write("fairkcenter.lp")

    colourdict = nx.get_node_attributes(G,"colour")
    #print(colourdict)

    for i in range(1,g):

        p_1i, q_1i = lowerbounds[i]
        p_2i, q_2i = upperbounds[i]

        for u in G.nodes():
            # Constraint 4
            model.addConstr(p_1i*quicksum([x[u,v] for v in G.nodes() if colourdict[v] == 0]) <= q_1i*quicksum([x[u,v] for v in G.nodes() if colourdict[v] == i]),"C4")
            # model.write("fairkcenter.lp")

            # Constraint 5
            model.addConstr(p_2i*quicksum([x[u, v] for v in G.nodes() if colourdict[v] == 0]) >= q_2i * quicksum([x[u, v] for v in G.nodes() if colourdict[v] == i]),"C5")
            # model.write("fairkcenter.lp")

    model.update()
    model.__data = x,y
    return model

def draw_graph(G):
    nx.draw(G,with_labels=True)
    plt.show()

# Given a weighted undirected graph G and a radius r,
# Returns an unweighted undirected graph G' with only edges less than r
def threshhold_graph(G,r):
    G_r = nx.Graph()    
    G_r.add_nodes_from(G)
    #print('made threshold')
    gthing = nx.get_node_attributes(G,"colour")
    nx.set_node_attributes(G_r,gthing,"colour")
    grthing = nx.get_node_attributes(G_r,"colour")
    #print(gthing)
    #print(grthing)
    #G_r.set_node_attributes(G.get_node_attributes)
    G_r.add_edges_from((u,v) for (u,v,d) in G.edges(data = True) if d["weight"] <= r)
    return G_r

def main():
    
    read_data = get_data("normalized_bank_data.txt",',')
    use_data = [(float(line[0]),float(line[1]),line[2]) for line in read_data]
    n = 100
    test_data = use_data[:n]
    #599 have color 1, 132 have color 2, 269 have color 0 
    G = make_graph(test_data,euclidean_metric)

    
    for i in range(n):
        thing = G.nodes[i]['colour']
        if thing == ' 0':
            G.nodes[i]['colour'] = 1
        elif thing == ' 1':
            G.nodes[i]['colour'] = 0
        else:
            G.nodes[i]['colour'] = 2
    

    print('Made graph!!')

    # NOTE: Colour 0 must be the majority colour
    # switch married to 'majority color'
    #print('thing' + str(G.nodes[1]))


   # colours = {0:1, 1:0 , 2:2, 6:32} #,4:1,5:0}
  #  nx.set_node_attributes(G,colours,"colour")
    #colorthing = nx.get_node_attributes(G,"colour")
    #print('colorthing' + str(colorthing))
    
    lowerbounds = [(1,1),(28,100),(13,100)]
    upperbounds = [(1,1),(30,100),(15,100)]
    cents = 25

    edge_weights = list(set([tuple[2]['weight'] for tuple in G.edges(data = True)]))
    edge_weights.sort()

    lower = 0
    upper = len(edge_weights)

    final_answer = 0
    final_rad = 0

    while lower < upper:
        x = lower + (upper-lower)//2
        print('Trying radius: ' + str(edge_weights[x]) + '... at index ' + str(x))
        Gr = threshhold_graph(G,edge_weights[x])
        cM = fair_k_center(Gr,cents,lowerbounds,upperbounds)
        print('time to optimze!')
        cM.optimize()
       # print('will i ever get here..')
        pM = cM
        if x != 0 and cM.status == GRB.Status.OPTIMAL:
            print('Trying pradius: ' + str(edge_weights[x-1]))
            Gr2 = threshhold_graph(G,edge_weights[x-1])
            pM = fair_k_center(Gr2,cents,lowerbounds,upperbounds)
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

    file1 = open("big_fair_test.txt", "w")
    file1.write('RADIUS: ' + str(final_rad) + '\n')

    if final_answer == 0:
        file1.write('No answer found..')
    else:
        for a in final_answer.getVars():
            file1.write(a.varName + " = " + str(a.x) + '\n')   



if __name__ == '__main__':
        main()