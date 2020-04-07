from connection import collection


def display_countries():
    print("\nHere is a list of countries:\n")
    countries = collection.distinct("countriesAndTerritories")
    print(countries)


def aggregate_countries(countries, feature):
    """
    Groups a list of countries together based on the number of daily cases or deaths.
    countries: list()
    cases: String ("cases", "deaths")
    return: list(), list()
    """
    agg = collection.aggregate([
        {
            "$match": {"countriesAndTerritories": {"$in": countries}}
        },
        {
            "$group": {
                "_id": {
                    "$toDate": {"$concat": ["$year", "-", "$month", "-", "$day"]}
                },
                "{}".format(feature): {"$sum": "${}".format(feature)}
            }
        },
        {"$sort": {"_id": 1}}
    ])

    dates = []
    features = []

    for item in agg:
        dates.append(item["_id"].date())
        features.append(item["{}".format(feature)])

    return dates, features


def aggregate_average_countries(countries, feature):
    """
    Groups a list of countries together, however calculates the daily average of the countries.
    countries: list()
    feature: String ("cases", "deaths")
    return: list(), list()
    """
    agg = collection.aggregate([
        {
            "$match": {"countriesAndTerritories": {"$in": countries}}
        },
        {
            "$group": {
                "_id": {
                    "$toDate": {"$concat": ["$year", "-", "$month", "-", "$day"]}
                },
                "{}".format(feature): {"$sum": "${}".format(feature)}
            }
        },
        {
            "$project": {"average_{}".format(feature): {"$divide": [{"$sum": "${}".format(feature)}, len(countries)]}}
        },
        {"$sort": {"_id": 1}}
    ])

    dates = []
    features = []
    for item in agg:
        dates.append(item["_id"].date())
        features.append(item["average_{}".format(feature)])

    return dates, features
