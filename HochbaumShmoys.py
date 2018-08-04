import networkx as nx
import matplotlib.pyplot as plt
import heapq

# What you were doing last time
# modifying HS select to use egograph
# finish slowselect


# Hochbaum-Shmoys. Takes in a weighted graph. Returns list of centers, and radius
def k_centers_hochbaumshmoys(G, k):

    def HS_select_with_k(G):
        HS_select(G,k)

    r = binsearch_thresholds(G, HS_select_with_k)
    G_r = threshhold_graph(G,r)
    S,passed = HS_select(G_r,k) #S is the set of centers

    if passed:
        return S,r
    else:
        return None

# Takes an unweighted threshold graph
# Returns (list_of_centers, passed)
def HS_select(Gr,k):
    uncovered_nodes = set(Gr.nodes)
    centers = []
    counter = 0
    while counter < k and len(uncovered_nodes) != 0:
        new_center = uncovered_nodes.pop()  #Get an arbitrary uncovered node
        centers.append(new_center)

        uncovered_nodes = uncovered_nodes - set(nx.ego_graph(Gr,new_center,radius=2))

        # for v in Gr.neighbors(new_center):
        #     uncovered_nodes.remove(Gr.neighbors(v))  #Throws an exception when removing something not in there

        # uncovered_nodes.remove(set(nx.ego_graph(Gr,new_center,radius=2))) #Remove all things within 2 of the node

        counter = counter + 1

    return centers, not uncovered_nodes

# Takes in an unweighted graph and an integer k. Returns (centers, booleanfor whether it placed at most k)
# Same as normal HS_select except instead of arbitrarily picking uncovered nodes, it picks the one that covers the least amount of points
def slow_select(G,k):
    # create a priority queue of nodes. The priority is how many nodes they would cover if selected.
    mylist = []
    for u in G.nodes():
        would_cover = len(set(nx.ego_graph(G, u, radius=2))) #What if I remove set?
        mylist.append((would_cover,u))

    h = heapq.heapify(mylist)
    print(type(h))

    count = 0
    centers = []
    while count < k:
        selected_node = heapq.heappop(h)
        centers.append(selected_node)

        set(nx.ego_graph(G, selected_node, radius=2))

        count = count + 1

    pass


# Takes in a weighted graph G and a test function.
# Returns the minimum value which passes the test using binary search
def binsearch_thresholds(G,test):
    radii = [data["weight"] for (u,v,data) in G.edges(data = True)]
    radii.sort()

    lower = 0
    upper = len(radii)

    while lower < upper:
        index = lower + (upper - lower) // 2
        G_r = threshhold_graph(G, radii[index])

        curr_passed = test(G_r)

        if not curr_passed:
            lower = index #Go up
            break

        elif curr_passed:
            upper = index
            # if index != 0:
            #     prev_Passed = test(threshhold_graph(G, radii[index - 1]))
            #     if prev_Passed:
            #         upper = index #Go down, both curr and prev passed the test
            #     else:
            #         return radii[index] #Getting here means curr_Passed but !prev_Passed, so this the answer
            # elif index == 0:
            #     return radii[index]

    #Getting here means lower=upper
    return radii[lower]

# Gonzalez. Takes in a weighted graph. Returns list of centers
def k_centers_gonzalez(G, k):
    mycenters = []
    cities = G.nodes()
    # add an arbitrary node, here, the first node,to the mycenters list
    mycenters.append(cities.popitem())
    k = k - 1  # since we have already added one center
    # choose k-1
    while k != 0:
        city_dict = {}
        for cty in cities:
            min_dist = float("inf")
            for c in mycenters:
                min_dist = min(min_dist, G[cty][c]['length'])
            city_dict[cty] = min_dist
        # print city_dict
        new_center = max(city_dict, key=lambda i: city_dict[i])
        # print new_center
        mycenters.append(new_center)
        cities.remove(new_center)
        k = k - 1
    # print mycenters
    return mycenters


# takes input from the file and creates a weighted undirected graph
def CreateGraph():
    G = nx.Graph()
    f = open('input.txt')
    n = int(f.readline())  # n denotes the number of cities
    wtMatrix = []
    for i in range(n):
        list1 = map(int, (f.readline()).split())
        wtMatrix.append(list1)
    # Adds egdes along with their weights to the graph
    for i in range(n):
        for j in range(n)[i:]:
            G.add_edge(i, j, length=wtMatrix[i][j])
    noc = int(f.readline())  # noc,here,denotes the number of centers
    return G, noc


# draws the graph and displays the weights on the edges
def DrawGraph(G, centers):
    pos = nx.spring_layout(G)
    color_map = ['blue'] * len(G.nodes())
    # all the center nodes are marked with 'red'
    for c in centers:
        color_map[c] = 'red'
    nx.draw(G, pos, node_color=color_map,
            with_labels=True)  # with_labels=true is to show the node number in the output graph
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=11)  # prints weight on all the edges



def main():
    G = nx.Graph()
    G.add_nodes_from(range(6))

    G.add_edge(0, 1, weight=0.6)
    G.add_edge(0, 2, weight=0.2)
    G.add_edge(2, 3, weight=0.1)
    G.add_edge(2, 4, weight=0.7)
    G.add_edge(2, 5, weight=0.9)
    G.add_edge(0, 3, weight=0.3)


    S,r = k_centers_hochbaumshmoys(G,2)
    print(S)
    print(r)
    DrawGraph(G,S)
    plt.show()


# Given a weighted undirected graph G and a radius r,
# Returns an unweighted undirected graph G' with only edges less than r
def threshhold_graph(G,r):
    G_r = nx.Graph()
    G_r.add_nodes_from(G.nodes)
    G_r.add_edges_from((u,v) for (u,v,d) in G.edges(data = True) if d["weight"] <= r)
    return G_r

if __name__ == "__main__":
    main()