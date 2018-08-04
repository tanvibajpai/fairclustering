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


def get_data(filename, delimeter=","):
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
    G.add_nodes_from([(i, dict(colour=data[i][m - 1])) for i in range(n)])  # There's got to be a better way to do this
    G.add_weighted_edges_from([(i, j, metric(data[i][0:m], data[j][0:m])) for (i, j) in combinations(range(n), 2)])
    return G


def euclidean_metric(point1, point2):
    if not len(point1) == len(point2):
        raise ValueError("The tuples arent the same length")

    return (sum([(point1[i] - point2[i]) ** 2 for i in range(len(point1))])) ** (1 / 2)


def draw_graph(G):
    nx.draw(G, with_labels=True)
    plt.show()


# Takes in a weighted graph, gives the weight adjacency matrix
def graph_to_matrix(G):
    return (nx.adjacency_matrix(G)).todense()


# returns array of cardinalities of disks of radius r around every vertex
# will only count uncovered points
def disk_count(n, cov, adj, r):
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
def max_disk(n, D):
    max = 0

    for i in range(n):
        if D[max] < D[i]:
            max = i
    return max


# marks newly covered vertices in cov array
def cov_disk(n, cov, adj, i, r):
    temp = adj
    tar = np.array(temp[i]).tolist()
    for j in range(n):
        if tar[0][j] <= r:
            cov[j] = 1
    return cov


# counts the number of points covered overall
def count_cov(n, cov):
    count = 0
    for i in range(n):
        if cov[i] == 1:
            count = count + 1
    return count


# solver for specific r; returns tuple (cen,cov,0/1) to denote the centers chosen,
# vertices covered, and whether or not at least p points were covered after placing
# k centers according the Charikar Khuller algorithm
def r_solver(n, p, adj, k, r):
    # initialize cov and cen to reflect that no points are centers or are covered.
    cov = []
    cen = []

    for i in range(n):
        cov.append(0)
        cen.append(0)

    # initialize D to have disk counts for all vertices
    D = disk_count(n, cov, adj, r)

    # Repeat the following k times
    for i in range(k):
        # let max be the heaviest disk
        max = max_disk(n, D)

        # pick max as a center
        cen[max] = 1

        # mark as covered all points in the extended disk
        cov = cov_disk(n, cov, adj, max, (3 * r))

        # update all disk cardinalities
        D = disk_count(n, cov, adj, r)

    # count number of points covered
    covered = count_cov(n, cov)

    # if at least p points are covered then answer is YES, otherwise, NO
    if (covered < p):
        return (r, cen, cov, 0)
    else:
        return (r, cen, cov, 1)


def solver(G, k, p):
    n = G.number_of_nodes()
    edge_weights = [tuple[2]['weight'] for tuple in G.edges(data=True)]
    # print(edge_weights[0])
    edge_weights.sort()

    ans = []

    adj = graph_to_matrix(G)

    for r in edge_weights:
        ans.append(r_solver(n, p, adj, k, r))

    return ans


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
            max_age = int(line[5])
        if int(line[11]) > max_duration:
            max_age = int(line[11])

    # for (age, balance, duration) in (data[0],data[5],data[11]):
    #     if age > max_age:
    #         max_age = age
    #     if balance > max_balance:
    #         max_age = balance
    #     if duration > max_duration:
    #             max_age = duration

    normalizedcooldata = [
        (int(line[0]) / max_age, int(line[5]) / max_balance, int(line[11]) / max_duration, colours[line[2]]) for line in
        data]
    n = 1000
    G = make_graph(normalizedcooldata[0:n], euclidean_metric)
    draw_graph(G)

    ans = solver(G, 100, 900)
    print("radius, centers, covered, passed")

    b = ans[0]

    for a in ans:
        r = a[0]
        if r < b[0] and a[3]:
            b = a

    outliers = [i for i in range(n) if b[2][i] == 0]

    print(outliers)
    nodelist = nx.nodes(G)
    outliervertices = [nodelist[v] for v in outliers]
    for a in outliervertices:
        print(a)
    for v in outliers:
        print(data[v])
   # print(outliervertices)

    # for a in ans:
    #     print(a)
    #     print()

    # print(adj.todense())
    # print("number of nodes: " + str(G.number_of_nodes()))
    # print(G.nodes(data=True))
    # print(G.edges(data=True))


if __name__ == '__main__':
    main()