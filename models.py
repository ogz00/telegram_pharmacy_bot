class pharmacy(object):
    def __init__(self, place_id, name, location):
        self.place_id = place_id
        self.name = name
        self.location = location


class pharmacy_details(object):
    def __init__(self, place_id, name, address, location, phone, url, distance):
        self.place_id = place_id
        self.name = name
        self.address = address
        self.phone = phone
        self.location = location
        self.url = url
        self.distance = distance


class location(object):
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude


class User(object):
    def __init__(self, first_name="", last_name="", username="", location=None, language="en"):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.location = location
        self.language = language
