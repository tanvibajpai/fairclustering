import csv
import networkx as nx
from itertools import combinations
import matplotlib.pyplot as plt
import scipy


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
    return nx.adjacency_matrix(G)

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

    normalizedcooldata = [(int(line[0])/max_age, int(line[5])/max_balance, int(line[11])/max_duration, colours[line[2]]) for line in data]
    G = make_graph(normalizedcooldata[0:100],euclidean_metric)
    draw_graph(G)
    adj = graph_to_matrix(G)
  print(adj.todense())
    print("number of nodes: " + str(G.number_of_nodes()))
    # print(G.nodes(data=True))
    # print(G.edges(data=True))



if __name__ == '__main__':
    main()
