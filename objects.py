

class Customer:
    def __init__(self, full_name, email_address, subscription_end):
        self.name = full_name
        self.email = email_address
        self.sub_end_date = subscription_end
        self.stations = []

    def print(self):
        print(self.name)
        print(self.email)
        print(self.sub_end_date)
        for station in self.stations:
            station.print()

class Station:
    def __init__(self, station_id, public_key, private_key, station_type, lat, lon, settings):
        self.id = station_id
        self.public_key = public_key
        self.private_key = private_key
        self.type = station_type
        self.location = Location(lat, lon)

        settings_dict = {"connection": settings[0], "battery": settings[1], "solar_panel": settings[2],
                         "rain_bucket": settings[3], "leaf_wetness": settings[4], "temperature": settings[5],
                         "location": settings[6], "eto": settings[7], "forecast": settings[8]}

        self.settings = settings_dict  # Dictionary of settings for the station
        self.probes = []
        self.data = []

    def print(self):
        print("ID: {}, Type: {}, Settings: {}".format(self.id, self.type, self.settings))
        self.location.print()
        for probe in self.probes:
            probe.print()

class Probe:
    def __init__(self, probe_length, probe_type, field_capacities):
        self.probe_length = probe_length
        self.probe_type = probe_type

        capacity_dict = {}
        i = 0
        for capacity in field_capacities:
            capacity_dict["{}0mm".format(i+1)] = capacity
            i += 1

        self.field_capacity = capacity_dict  # Dictionary of field capacities for the varying depths

    def print(self):
        print("Probe Length: {}, Probe Type: {}".format(self.probe_length, self.probe_type))
        for key in self.field_capacity:
            print("{}: {}".format(key, self.field_capacity[key]))

class Location:
    def __init__(self, latitude, longitude):
        self.lat = latitude
        self.lon = longitude

    def print(self):
        print("lat: {}, lon: {}".format(self.lat, self.lon))
