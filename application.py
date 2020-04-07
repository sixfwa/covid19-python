from connection import collection
import utils
import mongodb
import os


def menu(feature):
    print("1. For daily {0}. Here you will be able to see groups of countries and their daily {0} together. For example you can compare the daily {0} of (China, Iran) with (France, Italy)".format(feature))
    print("2. For average daily {0}. Best used when grouping countries. Here you can see the average daily number of groups of countries. For example you can compare the average daily number of {0} for (India, Germany) and (France, Italy, Spain)\n".format(feature))


def analysis_menu(feature):
    print("\nPress 1 for daily {}".format(feature))
    print("Press 2 for average daily {}".format(feature))
    print("Press 3 for {} within a population".format(feature))


if __name__ == "__main__":
    os.system("clear")
    command = int(input("Press 1 for cases or 2 for deaths:\t"))
    if command == 1 or command == 2:
        feature = ""
        if command == 1:
            feature = "cases"
        elif command == 2:
            feature = "deaths"
        menu(feature)
        analysis_menu(feature)
        command = int(input())
        if command == 1:
            mongodb.display_countries()
            a = mongodb.dates_cases_totals(utils.create_groups(), feature)
            utils.plot_graphs("Number of Daily {}".format(feature), a)
        elif command == 2:
            mongodb.display_countries()
            a = mongodb.dates_cases_averages(utils.create_groups(), feature)
            utils.plot_graphs("Number of Average Daily {}".format(feature), a)
        elif command == 3:
            greater_than = int(input("You want a population greater than:\t"))
            less_than = int(input("You want a population less than:\t"))
            countries = mongodb.aggregate_population_countries(
                greater_than, less_than, feature)
            utils.plot_graphs("Population", countries)
