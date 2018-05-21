from flask import Flask, jsonify, request
import numpy as np
import math
from .city import City
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__, static_url_path='')


def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def read_tsv_file():
    cities = []
    with open("static/data/canada_usa_cities.tsv", encoding="utf8") as f:
        first_line = True
        for line in f:
          if first_line:
            first_line = False
            continue

          (geo_name_id, name, ascii_name,
            alternate_names, latitude, longitude,
            feature_class, feature_code,
            country_code, cc2, admin1_code,
            admin2_code, admin3_code, admin4_code,
            population, elevation, dem, time_zone,
            modification_date) = line.split("\t")
          alt_names = alternate_names.split(",")
          city = {}
          city["geoNameId"] = geo_name_id
          city["name"] = name
          city["asciiName"] = ascii_name
          city["alternate_names"] = alt_names
          city["latitude"] = latitude
          city["longitude"] = longitude
          city["feature class"] = feature_class
          city["feature code"] = feature_code
          city["country code"] = country_code
          city["cc2"] = cc2
          city["admin1 code"] = admin1_code
          city["admin2 code"] = admin2_code
          city["admin3 code"] = admin3_code
          city["admin4 code"] = admin4_code
          city["population"] = population
          city["elevation"] = elevation
          city["dem"] = dem
          city["timezone"] = time_zone
          city["modification date"] = modification_date
          cities.append(city)
    return cities


def convert_tsv_city_to_output_city(city):
    return City(city["name"],
                city["admin1 code"],
                city["country code"],
                city["alternate_names"],
                city["latitude"],
                city["longitude"],
                city["score"])


def levenshtein_distance(first, second):
    mat = np.zeros((len(first)+1, len(second)+1))

    for x in range(0, len(first)+1):
        mat[x, 0] = x

    for y in range(0, len(second)+1):
        mat[0, y] = y

    for x in range(1, len(first)+1):
        for y in range(1, len(second)+1):
            sub_cost = 0

            if(first[x - 1] == second[y - 1]):
                sub_cost = 0
            else:
                sub_cost = 1

            mat[x, y] = min([mat[x-1, y] + 1, mat[x, y-1] +
                             1, mat[x-1, y-1] + sub_cost])
    cost = mat[(len(first), len(second))] / 2
    return cost


def calculate_city_score(city, name, latitude, longitude):
    score = 0
    if name:
        score += levenshtein_distance(city["name"], name) * 0.01
    if latitude and longitude:
        score += math.sqrt(((float(city["latitude"])-float(latitude))**2)+(
            (float(city["longitude"])-float(longitude))**2))
    elif latitude:
        score += abs(float(city["latitude"]) - float(latitude))
    elif longitude:
        score += abs(float(city["longitude"]) - float(longitude))
    return score


@app.route("/cities/<path:city>", methods=["GET"])
def city_search(city):
    cities = read_tsv_file()
    found_cities = list(filter(lambda c: c["name"] == city, cities))
    city_convert = []
    for found_city in found_cities:
        found_city["score"] = 1.0
        c = convert_tsv_city_to_output_city(found_city)
        city_convert.append(c)
    return jsonify(city_convert)


@app.route("/cities", methods=["GET"])
def city_like_search():
    cities = read_tsv_file()
    city = None
    longitude = None
    latitude = None
    if 'like' in request.args:
        city = request.args["like"]
    if 'longitude' in request.args:
        longitude = request.args["longitude"]
    if 'latitude' in request.args:
        latitude = request.args["latitude"]
    found_cities = {}
    if not city:
        found_cities = cities
    else:
        found_cities = list(
            filter(lambda c: city.upper().lower() in c["name"].upper().lower(), cities))
    city_convert = []
    maxScore = float("-inf")
    minScore = float("inf")
    for found_city in found_cities:
        found_city["score"] = calculate_city_score(
            found_city, city, latitude, longitude)
        if found_city["score"] < minScore:
            minScore = found_city["score"]
        if found_city["score"] > maxScore:
            maxScore = found_city["score"]
        c = convert_tsv_city_to_output_city(found_city)
        city_convert.append(c)

    for c in city_convert:
        c.score = 1 - ((c.score - minScore)/(maxScore - minScore))
        if np.isnan(c.score):
            c.score = 1.0

    returned_cities = sorted(city_convert, key=lambda x: x.score, reverse=True)

    loop_count = min([25, len(returned_cities)])

    json_data = []

    for x in range(0, loop_count):
        json_data.append(returned_cities[x].serialize())

    return jsonify(json_data)
