import csv
import matplotlib.pyplot as plt


# visualizer for k-center solution on normalized bank-data

# import math
def get_data(filename, delimeter=","):
    with open(filename, "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=delimeter)
        next(csv_reader)
        data = [line for line in csv_reader]

    return data


def main():

    read_data = get_data('normalized_bank_data.txt',',')

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

    
    #OPT SOLUTION FOR FIRST 200 POINTS
    
    #rad = 0.06719536449573707
    #cents = [9,26,62,63,107,114,164,193,197,198]


    #OPTIMAL SOLUTION FOR FIRST 500 POINTS
    #rad = 0.0704399555878803
    #cents = [209,479,456,346,404,391,198,93,195,309]

    rad = 0
    cents = []

    fig = plt.figure()
    #fig.suptitle('K-Center Clustering on Bank Data', fontsize=14,fontweight='bold')
    ax = fig.add_subplot(111)
    fig.subplots_adjust(top=0.85)

    ax.set_title('Bank Data')
    ax.set_xlabel('Age (normalized)')
    ax.set_ylabel('Bank Balance (normalized)')


    for i in cents:
        point = better_data[i]

        circ = plt.Circle((point[0], point[1]), rad, ec='k',fc='none')
        ax.add_patch(circ)

   # plt.plot(range(1))
    plt.xlim(0, 1)
    plt.ylim(-0.1, .7)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.draw()
    plt.scatter(*zip(*better_data))

    plt.show()


if __name__ == '__main__':
        main()
