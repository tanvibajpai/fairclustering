import numpy
import networkx as nx
import matplotlib.pyplot as plt
import itertools

# Returns the lists: (redpoints, bluepoints)
def generate_data(n,mu_r,sigma_r,mu_b,sigma_b,pi):

    data = []
    random_numbers = numpy.random.random(n)
    n_red = 0
    n_blue = 0

    # Get number of red and blue points
    for num in random_numbers:
        if num > pi:
            n_red = n_red + 1
        else:
            n_blue = n_blue + 1

    red_points = numpy.random.normal(mu_r,sigma_r,n_red)
    blue_points = numpy.random.normal(mu_b,sigma_b,n_blue)

    return  red_points,blue_points

def main():
    red_points, blue_points = generate_data(5,0,1,0,1,0.5)

    print(red_points,blue_points)

    G = lists_to_graph(red_points,blue_points)


    print(G.edges(data=True))

    # print("hi")
    # pos = nx.spring_layout(G)
    #
    # nx.draw_networkx_nodes(G, pos, nodelist=G.nodes()[0:len(red_points)], node_color='r', node_size=500)
    # nx.draw_networkx_nodes(G, pos, nodelist=G.nodes()[len(red_points):], node_color='b', node_size=500)
    # nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5)
    #
    #
    # plt.show()

# Takes in the lists redpoints and bluepoints and constructs a weighted, coloured graph G out of them
def lists_to_graph(red_points,blue_points):
    G = nx.Graph()

    for i,pt in enumerate(red_points):
        G.add_node(i,value = red_points[i],colour = "red")

    for i, pt in enumerate(blue_points):
        G.add_node(i+len(red_points), value=blue_points[i], colour="blue")

    n = len(red_points) + len(blue_points)
    for (u,v) in itertools.combinations(range(n),2):
        myvalues = nx.get_node_attributes(G,"value")
        myweight = abs(myvalues[u] - myvalues[v])
        G.add_edge(u,v,weight = myweight)

    return G

if __name__ == "__main__":
    main()