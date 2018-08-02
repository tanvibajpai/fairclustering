import csv
import matplotlib.pyplot as plt

# Code to plot bank.csv data as colored points on a pyplot

# import math
def get_data(filename, delimeter=","):
    with open(filename, "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=delimeter)
        next(csv_reader)
        data = [line for line in csv_reader]

    return data

def main():
    
    read_data = get_data('bank.csv',';')

    colours = {"single": 0, "married": 1, "divorced": 2, "unknown": 3}

    use_data = [(float(line[0]), float(line[5]), colours[line[2]]) for line in read_data]

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
            better_data.append((point[0], point[1], point_size, 'y'))

    print(str(better_data))
    plt.scatter(*zip(*better_data))
    plt.show()


if __name__ == '__main__':
        main()
