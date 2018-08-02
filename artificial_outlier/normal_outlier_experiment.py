import networkx as nx
import numpy as np
import itertools



def graph_to_matrix(G):
    return (nx.adjacency_matrix(G)).todense()

# Greedy 3-approx implementation ------------

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
        print('Failure! ' + str(covered) + ' points covered')
        return (r, cen, cov, 0)
    else:
        print('Success! ' + str(covered) + ' points covered')
        return (r, cen, cov, 1)


def solver(G, k, p):
    n = G.number_of_nodes()
    edge_weights = list(set([tuple[2]['weight'] for tuple in G.edges(data=True)]))
    # print(edge_weights[0])
    edge_weights.sort()

    adj = graph_to_matrix(G)

    lower = 0
    upper = len(edge_weights)

    while lower < upper:
        x = lower + (upper - lower) // 2
        print('Trying radius: ' + str(edge_weights[x]) + '... at index: ' + str(x))
        (cr, ccen, ccov, cans) = r_solver(n, p, adj, k, edge_weights[x])
        (pr, pcen, pcov, pans) = (3, [], [], 0)
        if x != 0 and cans == 1:
            print('Trying previous radius ' + str(edge_weights[x - 1]) + '... at index: ' + str(x - 1))
            (pr, pcen, pcov, pans) = r_solver(n, p, adj, k, edge_weights[x - 1])

        if cans == 1 and pans == 0:
            return (cr, ccen, ccov, cans)
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
    return (pr, pcen, pcov, pans)


# Data Generation ---------------------------

# Returns the lists: (redpoints, bluepoints)
def generate_data(n,mu_r,sigma_r,mu_b,sigma_b,pi):

    data = []
    random_numbers = np.random.random(n)
    n_red = 0
    n_blue = 0

    # Get number of red and blue points
    for num in random_numbers:
        if num > pi:
            n_red = n_red + 1
        else:
            n_blue = n_blue + 1

    red_points = np.random.normal(mu_r,sigma_r,n_red)
    blue_points = np.random.normal(mu_b,sigma_b,n_blue)

    return  red_points,blue_points


# Takes in the lists redpoints and bluepoints and constructs a weighted, coloured graph G out of them
def lists_to_graph(red_points,blue_points):
    G = nx.Graph()

    for i,pt in enumerate(red_points):
        G.add_node(i,value = red_points[i],color = "red")

    for i, pt in enumerate(blue_points):
        G.add_node(i+len(red_points), value=blue_points[i], color="blue")

    n = len(red_points) + len(blue_points)
    for (u,v) in itertools.combinations(range(n),2):
        myvalues = nx.get_node_attributes(G,"value")
        myweight = abs(myvalues[u] - myvalues[v])
        G.add_edge(u,v,weight = myweight)

    return G

def main():
    n = 1000
    mu_r = 0
    sig_r = 1
    mu_b = 0
    sig_b = 2
    pi = 0.5

    red_points, blue_points = generate_data(n,mu_r,sig_r,mu_b,sig_b,pi)

    print('Got points!')
    # print(red_points,blue_points)

    G = lists_to_graph(red_points,blue_points)

    print('Made graph!')

   # G_matrix = graph_to_matrix(G)

    k = 50
    p = 850

    num_red = 0
    num_blue = 0

    rad,centers,covered,correct = solver(G,k,p)
    colors = nx.get_node_attributes(G,'color')

    for i in range(n):
        if covered[i] == 0:
            if colors[i] == 'red':
                num_red = num_red + 1
            else:
                num_blue = num_blue + 1

    nmp = n - p
    per_red = (float(num_red)/nmp) * 100
    per_blue = (float(num_blue)/nmp) * 100

    file = open('norm_outlier_' + str(k) + '_' + str(n) + '_' + str(p) +'_3.txt',"w")
    file.write('NODES: ' + str(n) + '\n')
    file.write('MU_RED: ' + str(mu_r) + '\n')
    file.write('SIGMA_RED: ' + str(sig_r) + '\n')
    file.write('MU_BLUE: ' + str(mu_b) + '\n')
    file.write('SIGMA_BLUE: ' + str(sig_b) + '\n')
    file.write('PI: ' + str(pi) + '\n')
    file.write("RADIUS " + str(rad))
    file.write('\nOUTLIER COLORS\n')

    file.write('# RED - ' + str(num_red) + '\n')
    file.write('# BLUE - ' + str(num_blue) + '\n')

    file.write('% RED - ' + str(per_red) + '\n')
    file.write('% BLUE - ' + str(per_blue) + '\n')







if __name__ == "__main__":
    main()
