import json
import csv
import requests
from requests.auth import AuthBase
import hmac
import hashlib
import codecs
import os.path
from datetime import datetime
from datetime import timezone

# 1531363530

APPID = "e6cd4066d9a41879e9436b6bc51a0cf0"
filename = "weather.csv"

def convert_time(epoch_time):
    return datetime.fromtimestamp(epoch_time)

''' Reads the csv file (if one exists and is full - the existence is not checked here) and copies it into a matrix 
   so that new rows can be added at the top'''
def import_matrix():
    file = codecs.open(filename, 'rU', 'utf-16')

    csv_reader = csv.reader(file, delimiter="\t", lineterminator="\n")

    n = 0
    m = 0
    for row in csv_reader:
        if n == 0:
            n = len(row)
        m += 1

    matrix = [[0 for x in range(n)] for y in range(m)]

    file.close()

    file = codecs.open(filename, 'rU', 'utf-16')

    csv_reader = csv.reader(file, delimiter="\t", lineterminator="\n")

    i = 0
    j = 0
    for row in csv_reader:
        matrix[i] = row
        i += 1

    file.close()

    return matrix


def get_weather(lat=-43.976243, lon=171.784063):
    file_exists = os.path.isfile(filename)

    response = requests.get("http://api.openweathermap.org/data/2.5/weather?lat=" + str(lat) + "&lon=" + str(lon) + "&APPID=" + str(APPID) + "&units=metric")

    data = response.json()

    weather_dict = {'Latitude': data['coord']['lat'], 'Longitude': data['coord']['lon'], 'Air Temperature': data['main']['temp'],
                'Humidity': data['main']['humidity'], 'Wind speed': data['wind']['speed'], 'Wind direction': data['wind']['deg'],
                'time': convert_time(data['dt'])}

    for key in weather_dict:
        print('{}: {}'.format(key, weather_dict[key]))




    file = open(filename, 'w')

    csv_writer = csv.writer(file, delimiter=",", lineterminator="\n")

    for key in weather_dict:
        csv_writer.writerow("{}, {}".format(key, weather_dict[key]))

    file.close()


if __name__ == "__main__":
    get_weather()