class City(object):
    """City Object

    Attributes:
        city: City Name
        state: City's State Name
        country: City's Country
        alternate_names: Alternative Names
        latitude: City's Latitude
        longitude: City's Longitude
        score: Score
    """

    def __init__(self, city, state, country, alternate_names, latitude, longitude, score):
        self.city = city
        if country == "US":
            self.state = state
        else:
            self.state = ""
        self.country = country
        self.alternate_names = alternate_names
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        self.score = float(score)

    def serialize(self):
        return {
            "city": self.city,
            "state": self.state,
            "country": self.country,
            "alternate_names": self.alternate_names,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "score": self.score
        }
