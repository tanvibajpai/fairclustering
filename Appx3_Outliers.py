import networkx as nx
import scipy

def threshold_graph(G,r):
    G_r = nx.Graph()
    G_r.add_nodes_from(G.nodes)
    G_r.add_edges_from((u,v) for (u,v,d) in G.edges(data = True) if d["weight"] <= r)
    return G_r

# G is a weighted graph
# Place k centers, cover at least p points
# Returns (R,centers)???????????????????????
def k_center_outliers(G,k,p):
    n = G.number_of_nodes()

    edge_weights = [tuple[2]["weight"] for tuple in G.edges(data=True)]
    edge_weights.sort()

    for r in edge_weights:
        G_r = threshold_graph(G,r)
        boolean,centers = k_center_outliers_unweighted(G_r,k,p)
        if boolean:
            return r,centers

# G is now the unweighted threshold graph
# Returns a tuple (true,centers) if at least p points are covered
def k_center_outliers_unweighted(G,k,p):
    pass

def main():
    G = nx.Graph()
    G = nx.complete_graph(4)
    A = nx.adjacency_matrix(G)
    print(A)


if __name__ == '__main__':
    main()