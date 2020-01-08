""" author:     Pascal Schlaak
    title:      main.py
    content:    Functionality to discover NYPD crime data
    data:       https://catalog.data.gov/dataset/nypd-shooting-incident-data-historic
    python:     3.6.9
"""

import json
import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from collections import OrderedDict


PATH_TO_DATA = r"../data/NYPD_Shooting_Incident_Data__Historic_.csv"


def get_min_max_position(data: pd.DataFrame) -> list:
    
    """ Get min, max longitude, latitude for plot

    :param      data    pandas dataframe containing all informations
    :return     list    min, max of longitude and latitude
    """
        
    return data["Longitude"].min(), data["Longitude"].max(), data["Latitude"].min(), data["Latitude"].min()


def plot_crime_locations(data: pd.DataFrame):

    """ Plot crime locations by longitude and latitude
    
    :param      data    pandas dataframe containing all informations
    """

    # Define min and max longitude, latitude
    bounding_box = [-74.24930372699998, -73.70308204399998, 40.51158633800003, 40.910818945000074]
    # Get background image
    image_map = plt.imread(r"../data/map.png")
    
    # Plot data
    plt.scatter(data["Longitude"], data["Latitude"], c="r", alpha=0.2, zorder=1)
    
    # Set legend
    plt.title("NYPD crimes in 2018")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    
    # Show plot on background
    plt.imshow(image_map, zorder=0, extent=[bounding_box[0], bounding_box[1], bounding_box[2], bounding_box[3]])
    plt.show()


def get_murder_rate(data: pd.DataFrame) -> float:

    """ Calculate murder rate by number of incidents
    
    :param      data    pandas dataframe containing all informations
    :return     float   percentile of murder
    """

    murder_counter = 0

    # Check if murder flaf is true
    for entry in data:
        if entry:
            murder_counter += 1

    # Calculate and return percentile of murder by incidents
    return round((murder_counter / len(data)) * 100, 3)


def get_age_perpetrator_and_victim(data: pd.DataFrame) -> list:
    
    """ Get age group of perpetator and victim
    
    :param      data    pandas dataframe containing all informations
    :return     list    age of perpetator and victim
    """

    pass


def get_likelyhood_by_daytime(data: pd.DataFrame) -> str:

    """ Calculate average time of shooting
    
    :param      data    containing all occur timestamps of shootings
    :return     str     most likely time of day for shooting incident
    """

    hour_counters = {}
    
    # Count shootings per hour of day
    for entry in data:
        hour, _, _ = entry.split(":")
        if int(hour) not in hour_counters:
            hour_counters[int(hour)] = 0
        else:
            hour_counters[int(hour)] += 1
    
    # Sort dict by hours
    sorted_hour_counters = OrderedDict(sorted(hour_counters.items()))
    
    # Plot shootings by month
    plt.plot(sorted_hour_counters.keys(), sorted_hour_counters.values())
    plt.fill_between(sorted_hour_counters.keys(), sorted_hour_counters.values())

    # Add metadata
    plt.title("New York shooting incidents by hour of day")
    plt.xlabel("Hour [h]")
    plt.ylabel("Incidents")
    plt.xticks(np.arange(len(sorted_hour_counters.keys())), sorted_hour_counters.keys(), rotation=0)
    
    # Show plot
    plt.show()


def get_most_likely_month(data: pd.DataFrame, year: int):

    """ Find month with highest shooting rate

    :param      data    pandas dataframe containing all informations
    :param      year    Year of data entries
    """
    
    # Init months
    month_counters = {"01": 0, "02": 0, "03": 0, "04": 0, "05": 0, "06": 0, "07": 0, "08": 0, "09": 0, "10": 0, "11": 0, "12": 0}
    
    # Count incidents by month
    for entry in data:
        month = str(entry)[0:2]
        month_counters[month] += 1
    
    # Plot shootings by month
    plt.bar(month_counters.keys(), month_counters.values())
    
    # Add metadata
    plt.title("NY shooting incidents in {}".format(year))
    plt.xlabel("Month")
    plt.ylabel("Incidents")
    
    # Show plot
    plt.show()


def get_sex_rate_perpetrator(data: pd.DataFrame) -> list:

    """ Get male/female ration of perpetrator

    :param      data... pandas dataframes containing sex of perpetrators and victims
    :return     float   ratio of perpetrators sex
    """

    # Possible values: Male, female, unknown
    sex_perpetrators = {"M": 0, "F": 0, "U": 0}
    sex_victims = {"M": 0, "F": 0, "U": 0}

    data["PERP_SEX"] = data["PERP_SEX"].fillna("U")
    data["VIC_SEX"] = data["VIC_SEX"].fillna("U")
    
    # Count sex of perpetrators and victims
    for entry in data["PERP_SEX"]:
        sex_perpetrators[entry] += 1

    for entry in data["VIC_SEX"]:
        sex_victims[entry] += 1

    return sex_perpetrators, sex_victims


def count_race_perpetrator(data: pd.DataFrame) -> list:

    """ Get distribution of perpetrators race

    :param      data    pandas dataframe containing all informations
    :return     list    counters of perpetrator by race
    """

    pass


def shootings_per_year(data: pd.DataFrame):

    """ Plot shooting incidents per year from 2006 until 2018

    :param      data    pandas dataframe containing all column of all occur dates
    """

    year_counters = {}
    
    # Count shooting incidents per year
    for entry in data:
        if entry[6:] not in year_counters:
            year_counters[entry[6:]] = 0
        else:
            year_counters[entry[6:]] += 1
    
    # Sort dict entries by key
    sorted_year_counters = OrderedDict(sorted(year_counters.items()))

    # Plot shootings by month
    plt.bar(sorted_year_counters.keys(), sorted_year_counters.values())
    
    # Add metadata
    plt.title("Number of New York shooting incidents by year")
    plt.xlabel("Year")
    plt.ylabel("Incidents")
    
    # Show plot
    plt.show()


def main():
    
    """ Main to run functionality
    """
    
    altered_data = pd.DataFrame({})
    year = 2018
    
    # Read data from csv
    data = pd.read_csv(PATH_TO_DATA)

    # Filter data by year
    for index, row in data.iterrows():
        if ("/" + str(year)) in str(row["OCCUR_DATE"]):
            altered_data = altered_data.append(row, ignore_index = True)
    
    # Print murder rate
    #murder_rate = get_murder_rate(altered_data["STATISTICAL_MURDER_FLAG"])
    #print("Murder rate in {year}:\t{rate} %".format(year=year, rate=murder_rate))
    
    # Visualize crime locations on map
    #plot_crime_locations(altered_data)

    # Show shootings by month and year
    #get_most_likely_month_and_season(altered_data["OCCUR_DATE"], year)
    
    # Get male/female ratio
    #sex_perpetrators, sex_victims = get_sex_rate_perpetrator(altered_data)
    #print("Sex perpetrators:\n{perp}\n\nSex victims:\n{vict}".format( \
            #perp=json.dumps(sex_perpetrators, indent=1), vict=json.dumps(sex_victims, indent=1)))
    
    # Plot shooting incidents per year
    #shootings_per_year(data["OCCUR_DATE"])
    
    # Get most likely time of incident
    time = get_likelyhood_by_daytime(data["OCCUR_TIME"])
    print("Most likely time: {}".format(time))


if __name__ == "__main__":
    main()

