import matplotlib.pyplot as plt
import numpy as np


def create_groups():
    groups = {}
    number_of_groups = int(input("Number of Groups: "))
    for i in range(number_of_groups):
        group_length = int(
            input("Number of Countries in Group {}: ".format(i + 1)))
        group = []
        for j in range(group_length):
            country = str(input("Enter a Country: "))
            group.append(country)
        group = tuple(group)
        groups[group] = {}

    return groups


def plot_graphs(title, groups):
    for group in groups:
        x = list(groups[group].keys())
        y = list(groups[group].values())
        plt.plot(x, y, label=group)
        # plt.xticks(np.arange(0, len(x), step=5))
        # plt.yticks(np.arange(0, max(y), step=1000))

    plt.legend()
    plt.title(title)
    plt.show()
