import json
import math
import os
from operator import itemgetter


def distance(latitude1, latitude2, longitude1, longitude2):
    """
    The distance is calculated by the Havershine formula.
    :param latitude1: the latitude of location1
    :param latitude2: the latitude of location2
    :param longitude1: the longitude of location1
    :param longitude2: the longitude of location2
    :return: the distance in km
    """
    earth_radius = 6371

    latitude1 = math.radians(latitude1)
    latitude2 = math.radians(latitude2)
    delta_latitude = math.radians(latitude2 - latitude1)
    delta_longitude = math.radians(longitude2 - longitude1)

    a = math.sin(delta_latitude / 2) ** 2 + math.cos(latitude1) * math.cos(latitude2) * (
        math.sin(delta_longitude / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return earth_radius * c


def load_json(json_path):
    if not os.path.exists(json_path):
        return None
    with open(json_path) as data_file:
        return json.load(data_file)


def get_biggest_bar(json_bars):
    bars = {(json_bar['Cells']['SeatsCount'], json_bar['Cells']['Name']) for json_bar in json_bars}
    biggest_bar = max(bars, itemgetter(0))
    return biggest_bar[1]


def get_smallest_bar(json_bars):
    bars = {(json_bar['Cells']['SeatsCount'], json_bar['Cells']['Name']) for json_bar in json_bars}
    smallest_bar = min(bars, itemgetter(0))
    return smallest_bar[1]


def get_closest_bar(json_bars, user_longitude, user_latitude):
    bars = {(distance(
        user_latitude,
        float(json_bar['Cells']['geoData']['coordinates'][1]),
        user_longitude,
        float(json_bar['Cells']['geoData']['coordinates'][0]),
    ),
             json_bar['Cells']['Name']) for json_bar in json_bars
            }
    closest_bar = min(bars, itemgetter(0))
    return closest_bar[1]


if __name__ == '__main__':
    json_path = input('Enter the path to the file:\n=> ')
    json_bars = load_json(json_path)

    while json_bars is None:
        json_path = input('Sorry, but it looks like there is a mistake in the path to the file.'
                          '\nPlease, enter the valid path:\n=> ')
        json_bars = load_json(json_path)

    print('The biggest bar is %s' % get_biggest_bar(json_bars))
    print('The smallest bar is %s' % get_smallest_bar(json_bars))

    user_latitude = float(input('Enter your latitude:\n=> '))

    user_longitude = float(input('Enter your longitude:\n=> '))

    print('The nearest place is "%s"' % get_closest_bar(json_bars, user_longitude, user_latitude))
