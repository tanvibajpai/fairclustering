import csv
import matplotlib.pyplot as plt


# visualizer for k-center solution

# import math
def get_data(filename, delimeter=","):
    with open(filename, "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=delimeter)
        next(csv_reader)
        data = [line for line in csv_reader]

    return data


def main():

    read_data = get_data('norm_data.txt',',')

    use_data = [(float(line[0]), float(line[1]), int(line[2])) for line in read_data]

    better_data = []
    point_size = 2




    for point in use_data:
        if point[2] == 0:
            better_data.append((point[0],point[1],point_size,'r'))
        elif point[2] == 1:
            better_data.append((point[0], point[1], point_size, 'b'))
        elif point[2] == 2:
            better_data.append((point[0], point[1], point_size, 'g'))
        elif point[2] == 3:
            better_data.append((point[0], point[1], point_size, 'c'))

    #OPT 200
    #rad = 0.06719536449573707
    #cents = [9,26,62,63,107,114,164,193,197,198]


    #OPT 500
    #rad = 0.0704399555878803
    #cents = [209,479,456,346,404,391,198,93,195,309]
    rad = 0
    cents = []

    #plt.scatter(*zip(*better_data[:200]))
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)


    for i in cents:
        point = better_data[i]

        circ = plt.Circle((point[0], point[1]), rad, ec='k',fc='none')
        ax.add_patch(circ)



    plt.scatter(*zip(*better_data))
   # plt.scatter(0.5, 0.2, s=1000, facecolors='none', edgecolors='r')

    plt.show()


if __name__ == '__main__':
        main()
