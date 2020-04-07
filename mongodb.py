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
        # .strftime("%d/%m/%y")
        dates.append(item["_id"].date())
        features.append(item["average_{}".format(feature)])

    return dates, features


def aggregate_population_countries(greater_than, less_than, feature):
    """
    Compares the daily number of cases or deaths of countries within an population range
    """
    countries = {}
    agg = collection.aggregate([
        {
            "$match": {
                "$and": [{"popData2018": {"$lt": less_than, "$gt": greater_than}}]
                # "popData2018": {"$and": [{"$lt": less_than}, {"$gt": greater_than}]}
            }
        },
        {
            "$project": {
                "dateRep": {"$toDate": {"$concat": ["$year", "-", "$month", "-", "$day"]}},
                "{}".format(feature): "${}".format(feature),
                "countriesAndTerritories": "$countriesAndTerritories"
            }
        },
        {
            "$sort": {"dateRep": 1}
        }
    ])

    for item in agg:
        date = item["dateRep"].date()
        country_name = item["countriesAndTerritories"]
        # print("{} --> {}".format(date, country_name))
        if country_name not in countries:
            countries[country_name] = {}
            countries[item["countriesAndTerritories"]][date] = item[feature]
        else:
            countries[item["countriesAndTerritories"]][date] = item[feature]

    return countries


def dates_cases_totals(groups, feature):
    for group in groups:
        dates, cases = aggregate_countries(group, feature)
        for date, case in zip(dates, cases):
            groups[group][date] = case
    return groups


def dates_cases_averages(groups, feature):
    for group in groups:
        dates, cases = aggregate_average_countries(group, feature)
        for date, case in zip(dates, cases):
            groups[group][date] = case
    return groups
