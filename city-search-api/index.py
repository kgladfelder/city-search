from flask import Flask, jsonify, request
app = Flask(__name__, static_url_path='')

def read_tsv_file():
  cities = []
  with open("static/data/canada_usa_cities.tsv", encoding="utf8") as f:
    for line in f:
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
      city["dem"] = dem
      city["timezone"] = time_zone
      city["modification date"] = modification_date
      cities.append(city)
  return cities

def convert_tsv_city_to_output_city(city):
  c = {}
  c["city"] = city["name"]
  c["state"] = city["admin1 code"]
  c["country"] = city["country code"]
  c["alternate_names"] = city["alternate_names"]
  c["latitude"] = city["latitude"]
  c["longitude"] = city["longitude"]
  return c

@app.route("/cities/<path:city>", methods=["GET"])
def city_search(city):
  cities = read_tsv_file()
  found_cities = list(filter(lambda c: c["name"] == city, cities))
  cityJSON = []
  for found_city in found_cities:
    c = convert_tsv_city_to_output_city(found_city)
    cityJSON.append(c)
  return jsonify(cityJSON)

@app.route("/cities", methods=["GET"])
def city_like_search():
  cities = read_tsv_file()
  city = request.args["like"]
  found_cities = list(filter(lambda c: city in c["name"], cities))
  cityJSON = []
  for found_city in found_cities:
    c = convert_tsv_city_to_output_city(found_city)
    cityJSON.append(c)
  return jsonify(cityJSON)