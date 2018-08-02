import csv
import networkx as nx
from itertools import combinations
import matplotlib.pyplot as plt
import scipy
import numpy as np


# with open("bank.csv", "r") as csv_file:
#     csv_reader = csv.DictReader(csv_file, delimiter = ";")
#     for line in csv_reader:
#         print(line["age"])


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

    return (sum([(point1[i] - point2[i])**2 for i in range(len(point1))]))**(1/2)

def draw_graph(G):
    nx.draw(G,with_labels=True)
    plt.show()

# Takes in a weighted graph, gives the weight adjacency matrix
def graph_to_matrix(G):
    return (nx.adjacency_matrix(G)).todense()

# returns array of cardinalities of disks of radius r around every vertex
# will only count uncovered points
def disk_count(n,cov,adj,r):
    D = []
   # print(adj)
    for i in range(n):
        D.append(0)
        temp = adj
        tar = np.array(temp[i]).tolist()
        for j in range(n):
            # only count if within radius and uncovered
            if (cov[j] == 0) and (tar[0][j] <= r):
                D[i] = D[i] + 1

    return D


# returns index of heaviest disk
def max_disk(n,D):
    max = 0


    for i in range(n):
        if D[max] < D[i]:
            max = i
    return max

# marks newly covered vertices in cov array
def cov_disk(n,cov,adj,i,r):
    temp = adj
    tar = np.array(temp[i]).tolist()
    for j in range(n):
        if tar[0][j] <= r:
            cov[j] = 1
    return cov

# counts the number of points covered overall
def count_cov(n,cov):
    count = 0
    for i in range(n):
        if cov[i] == 1:
            count = count + 1
    return count


# solver for specific r; returns tuple (cen,cov,0/1) to denote the centers chosen,
# vertices covered, and whether or not at least p points were covered after placing
# k centers according the Charikar Khuller algorithm
def r_solver(n,p,adj,k,r):


    # initialize cov and cen to reflect that no points are centers or are covered.
    cov = []
    cen = []

    for i in range(n):
        cov.append(0)
        cen.append(0)

    # initialize D to have disk counts for all vertices
    D = disk_count(n,cov,adj,r)

    # Repeat the following k times
    for i in range(k):
        # let max be the heaviest disk
        max = max_disk(n,D)

        # pick max as a center
        cen[max] = 1

        # mark as covered all points in the extended disk
        cov = cov_disk(n,cov,adj,max,(3*r))

        # update all disk cardinalities
        D = disk_count(n,cov,adj,r)
 

    # count number of points covered
    covered = count_cov(n,cov)

    # if at least p points are covered then answer is YES, otherwise, NO
    if(covered < p):
        print('Failure! ' + str(covered) + ' points covered')
        return (r,cen,cov,0)
    else:
        print('Success! ' + str(covered) + ' points covered')
        return (r,cen,cov,1)



def solver(G, k, p):
    n = G.number_of_nodes()
    edge_weights = list(set([tuple[2]['weight'] for tuple in G.edges(data=True)]))
    #print(edge_weights[0])
    edge_weights.sort()



    adj = graph_to_matrix(G)
    
    lower = 0
    upper = len(edge_weights)

    while lower < upper:
        x = lower + (upper-lower)//2
        print('Trying radius: ' + str(edge_weights[x])+ '... at index: ' + str(x))
        (cr,ccen,ccov,cans) = r_solver(n,p,adj,k,edge_weights[x])
        (pr,pcen,pcov,pans) = (3,[],[],0)
        if x != 0 and cans == 1:
            print('Trying previous radius ' + str(edge_weights[x-1]) + '... at index: ' + str(x-1))
            (pr,pcen,pcov,pans) = r_solver(n,p,adj,k,edge_weights[x-1])


        if cans == 1 and pans == 0:
            return (cr,ccen,ccov,cans)
        elif cans == 1 and pans == 1:
            upper = x
        else:
            if lower == x:
                break
            lower = x

   # for r in edge_weights:
     #   (r,cen,cov,ans) = r_solver(n,p,adj,k,r)

       # if ans == 1:
       #     return (r,cen,cov,ans)

    print("NO ANSWER FOUND")
    return (pr,pcen,pcov,pans)






# The data we have is of the form: (age, balance, duration, marital-status)
def main():
    data = get_data("bank.csv", ";")

    colours = {"single": 0, "married": 1, "divorced": 2, "unknown": 3}
    max_age = -1
    max_balance = -1
    max_duration = -1

    for line in data:
        if int(line[0]) > max_age:
            max_age = int(line[0])
        if int(line[5]) > max_balance:
            max_balance = int(line[5])
        if int(line[11]) > max_duration:
                max_duration = int(line[11])

    # for (age, balance, duration) in (data[0],data[5],data[11]):
    #     if age > max_age:
    #         max_age = age
    #     if balance > max_balance:
    #         max_age = balance
    #     if duration > max_duration:
    #             max_age = duration

    normalizedcooldata = [(int(line[0])/max_age, int(line[5])/max_balance, int(line[11])/max_duration, colours[line[2]]) for line in data]
    num_nodes = 1000
    G = make_graph(normalizedcooldata[0:num_nodes],euclidean_metric)
    #draw_graph(G)
    cents = 75
    covs = 900
    nodes = nx.nodes(G)
    (r,cen,cov,ans) = solver(G,cents,covs)
    print("radius, centers, covered, passed")
    print('RADIUS: ' + str(r))
    print('CENTERS' + str(cen))
    print('COVERED' + str(cov))

    file = open("results(1000,75,900).txt","w")
    file.write("RADIUS: " + str(r))
    file.write("\nOUTLIER COLORS\n")

    count = 0
    ones = 0
    twos = 0
    zeros = 0
    threes = 0
    for i in range(num_nodes):
        if cov[i] == 0:
            curr = nodes[i]
            #print("vertex " + str(i) + ": " + str(curr))
            file.write("vertex " + str(i) + ": " + str(curr) + " + " + str(data[i]) + "\n")
            count = count + 1

            if curr['colour'] == 0:
                zeros = zeros + 1
            elif curr['colour'] == 1:
                ones = ones + 1
            elif curr['colour'] == 2:
                twos = twos + 1
            else:
                threes = threes + 1

    new_count = count

    if count == 0:
        new_count = 1

    per_z = (float(zeros)/new_count)*100
    per_o = (float(ones)/new_count)*100
    per_t = (float(twos)/new_count)*100
    per_th = (float(threes)/new_count)*100



    file.write("\nNUMBER OF OUTLIERS: " + str(count) + "\n\n")
    file.write("SINGLE:\n COUNT: " + str(zeros) + "\tPERCENTAGE: " + str(per_z) + "\n")
    file.write("MARRIED:\n COUNT: " + str(ones) + "\tPERCENTAGE: " + str(per_o) + "\n")
    file.write("DIVORCED:\n COUNT: " + str(twos) + "\tPERCENTAGE: " + str(per_t) + "\n")
    file.write("UNKNOWN:\n COUNT: " + str(threes) + "\tPERCENTAGE: " + str(per_th) + "\n")
    file.close()



    # print(adj.todense())
    # print("number of nodes: " + str(G.number_of_nodes()))
    # print(G.nodes(data=True))
    # print(G.edges(data=True))



if __name__ == '__main__':
    main()
