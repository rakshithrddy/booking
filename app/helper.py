import datetime
import math
import os
import uuid
import json
import pandas as pd

from config import basedir

path_to_app = os.path.join(basedir, 'app')
path_to_static = os.path.join(path_to_app, 'static')


def get_city_coordinates():
    data = pd.read_csv(os.path.join(path_to_static, 'in.csv'), index_col=False)
    cities = data['city'].values
    data.set_index('city', inplace=True, drop=True)
    return data, cities


def get_distance(source, destination, trip_type='One Way', operational_optimize=True) -> int:
    """
    takes in source city name and destination name to calculate distance.
    :return: distance in kms (float)
    """
    data, _ = get_city_coordinates()
    source_city_lat, source_city_long = data.loc[source]
    destination_city_lat, destination_city_long = data.loc[destination]
    R = 6373.0
    lat1 = math.radians(source_city_lat)
    lon1 = math.radians(source_city_long)
    lat2 = math.radians(destination_city_lat)
    lon2 = math.radians(destination_city_long)

    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    if trip_type == 'Round Trip' or operational_optimize is False:
        distance *= 2
    return int(distance)


def cost(distance: float, cost_per_km: int, operational_optimized=True) -> float:
    total_cost = distance * cost_per_km
    if operational_optimized is False:
        total_cost *= 2
    return total_cost


def generate_ticket(user_id):
    ticket = uuid.uuid5(namespace=uuid.NAMESPACE_DNS, name=(str(datetime.datetime.now()) + str(user_id)))
    return str(ticket)


def create_maps(languages):
    from app.models import Driver
    driver_names = Driver.get_driver_names()
    drivers_details = Driver.jsonify_drivers()
    driver_to_cost_map = {}
    language_to_driver_map = {}
    if len(driver_names) == 0 or len(drivers_details) == 0:
        raise Exception("Drivers details are currently not available")
    for driver in driver_names:
        if driver is not None:
            driver_to_cost_map[driver] = drivers_details[driver]['cost_per_km']
    for language in languages:
        dr = []
        for driver in driver_names:
            if driver is not None:
                if language in drivers_details[driver]['languages']:
                    if language is not None:
                        dr.append(driver)
        language_to_driver_map[language] = dr
    return driver_to_cost_map, language_to_driver_map


def get_languages():
    with open(os.path.join(path_to_static, 'languages.json')) as f:
        json_data = json.load(f)
    languages = json_data['languages']
    return languages
