import json
import csv
import re
import requests
from requests.auth import AuthBase
import hmac
import hashlib
import codecs
import os.path
from datetime import datetime
from datetime import timezone

# Endpoint of the API, version for example: v1
apiURI = "https://api.fieldclimate.com/v1"

# HMAC Authentication credentials
publicKey = "ac696b8139646f6d330b5be3b845844c4b232e2f"
privateKey = "5188bcaabe41b925dff9783b77f6af223ca71304"

# Class to perform HMAC encoding
class AuthHmacMetosGet(AuthBase):
    # Creates HMAC authorization header for Metos REST service GET request.
    def __init__(self, apiRoute, publicKey, privateKey):
        self._publicKey = publicKey
        self._privateKey = privateKey
        self._method = 'GET'
        self._apiRoute = apiRoute

    def __call__(self, request):
        dateStamp = datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
        request.headers['Date'] = dateStamp
        msg = (self._method + self._apiRoute + dateStamp + self._publicKey).encode(encoding='utf-8')
        h = hmac.new(self._privateKey.encode(encoding='utf-8'), msg, hashlib.sha256)
        signature = h.hexdigest()
        request.headers['Authorization'] = 'hmac ' + self._publicKey + ':' + signature
        return request

def date_format_converter(date_time):
    """Converts from the form FieldClimate outputs to the type expected by the datetime module so a UNIX timestamp can
       be calculated"""
    date_time_separated = date_time.split()
    date = date_time_separated[0]
    time = date_time_separated[1]

    date_separated = re.split('/|-', date)
    time_separated = time.split(':')

    year = int(date_separated[0])
    month = int(date_separated[1])
    day = int(date_separated[2])

    hour = int(time_separated[0]) + 1 # + 1 prevents the data for this timestamp being fetched again
    minute = int(time_separated[1])
    second = 0

    formatted_date = datetime(year, month, day, hour, minute, second)

    return formatted_date

def find_last_timestamp(filename):
    """Reads the existing csv file and finds the last timestamp that data was stored from"""
    file = open(filename, 'r')

    csv_reader = csv.reader(file)

    i = 0
    for row in csv_reader:
        if i == 2:
            last_date = row[0]
            break
        i += 1

    file.close()

    formatted_date = date_format_converter(last_date)

    timestamp = formatted_date.replace(tzinfo=timezone.utc).timestamp()

    return timestamp, last_date

def import_matrix(filename):
    ''' Reads the csv file (if one exists and is full - the existence is not checked here) and copies it into a matrix
       so that new rows can be added at the top'''
    file = open(filename, 'r')

    csv_reader = csv.reader(file)

    matrix = []

    i = 0
    for row in csv_reader:
        if i >= 2: # need to convert string representation on numbers to floats
            new_row = []
            j = 0
            for value in row:
                if j >= 1:
                    try:
                        new_row.append(float(value))
                    except ValueError:
                        new_row.append(None)
                else:
                    new_row.append(value)

                j += 1
            matrix.append(new_row)
        else:
            matrix.append(row)
        i += 1

    file.close()

    return matrix

def combine_keys(keys1, keys2):
    """Takes two lists of keys and links them together in a nested dictionary structure"""
    indices_dict = {'0': ["Date/Time", "hour"]}
    hour_dict = {"hour": []}
    key_dict = {"Date/Time": hour_dict}

    key_dict["indices"] = indices_dict

    print()
    print("KEYS")
    print()
    print(keys1)
    print(keys2)
    print()

    last_key = None

    count = 0
    repeats = 0
    for key in keys1:
        if count >= 1:
            if str(key) != "0" and key != last_key:
                repeats = 0
                key_dict[key] = {}
                key_dict[key][keys2[count]] = []
                key_dict["indices"]["{}".format(count)] = [key, keys2[count]]
            elif str(key) == "0" and last_key is not None:
                if repeats == 0:
                    key_dict[last_key][keys2[count]] = []
                    key_dict["indices"]["{}".format(count)] = [last_key, keys2[count]]
                else:
                    new_key = "{}{}".format(last_key, (repeats + 1))
                    key_dict[new_key][keys2[count]] = []
                    key_dict["indices"]["{}".format(count)] = [new_key, keys2[count]]
            elif key == last_key: #soil moisture probes
                repeats += 1
                new_key = "{}{}".format(key, (repeats+1))
                key_dict[new_key] = {}
                key_dict[new_key][keys2[count]] = []
                key_dict["indices"]["{}".format(count)] = [new_key, keys2[count]]

            if str(key) != "0":
                last_key = key
        count += 1

    return key_dict

def create_dictionary(matrix):
    """Reads matrix into a dictionary"""

    keys1 = []
    keys2 = []

    i = 0
    for row in matrix:
        if i >= 2:  # need to convert string representation on numbers to floats
            j = 0
            for value in row:
                # need to get the key from the index
                [key1, key2] = pessl_dict["indices"]["{}".format(j)]
                pessl_dict[key1][key2].append(value)
                j += 1
        elif i == 0:
            keys1 = row
        elif i == 1:
            keys2 = row
            pessl_dict = combine_keys(keys1, keys2)
        i += 1

    return pessl_dict

def create_matrix(sensor_data, dates, et_data=None):
    """If no matrix exists, create one from the data that has just been read from fieldclimate"""
    n = 1  # col count, stats at 1 to account for dates col

    for sensor in sensor_data:
        for key in sensor_data[sensor]['aggr']:
            if n == 1:
                m = len(sensor_data[sensor]['aggr'][key]) # number of rows needed for data
            n += 1

    m += 2  # account for the two header rows

    matrix = [[0 for x in range(n)] for y in range(m)] # Creates blank matrix

    # Can now populate the matrix with data
    i = 1
    j = 0
    matrix[i][j] = 'Date/Time'
    for date in dates:
        matrix[-i][j] = date
        i += 1

    j += 1

    for sensor in sensor_data:
        i = 0
        matrix[i][j] = sensor_data[sensor]['name']

        for key in sensor_data[sensor]['aggr']:
            i = 1
            matrix[i][j] = key

            for value in sensor_data[sensor]['aggr'][key]:
                matrix[-i][j] = value
                i += 1
            j += 1

    if et_data is not None:
        i = 0
        for row in matrix:
            if i >= 2:
                row.append(et_data["ETo[mm]"][i-2])
            elif i == 0:
                row.append("ETo[mm]")
            elif i == 1:
                row.append("daily")
            i += 1


    return matrix

def append_to_matrix(old_matrix, new_matrix):
    """Appends the new data to the matrix"""
    final_matrix = new_matrix

    i = 2
    while i < len(old_matrix):
        final_matrix.append(old_matrix[i])
        i += 1

    return final_matrix

def api_call(apiRoute):
    """Calls the fieldclimate API"""
    auth = AuthHmacMetosGet(apiRoute, publicKey, privateKey)
    response = requests.get(apiURI + apiRoute, headers={'Accept': 'application/json'}, auth=auth)
    return response

def get_dates(id):
    """Checks the fieldclimate data, returns the date of the last datapoint"""
    dates = "/data/{}".format(id)
    return api_call(dates)

def get_data(id):
    """Gets the data from fieldclimate using the API returns a response in json form"""
    dates = get_dates(id).json()
    read_data = '/data/optimized/{}/hourly/last/1m'.format(id)
    return api_call(read_data)

def get_et(id, last_date = 0):
    """Gets the Evapotranspiration data from fieldclimate using the API returns a response in json form"""
    read_data = '/disease/{}/last/5w'.format(id)
    return api_call(read_data)

def write_to_csv(matrix, filename):

    file = open(filename, 'w')

    csv_writer = csv.writer(file, delimiter=",", lineterminator="\n")

    for row in matrix:
        csv_writer.writerow(row)

    file.close()

def check_dates(date1, date2):
    if date1 == date2:
        return False
    else:
        return True

def format_et_data(et_data, dates):
    """Comes in a really niggly form, list of dicts like so [{'date': '2018-06-07 23:00:00', 'ETo[mm]': 0.6}, ...
       need to drag data out over the entire day too so that it matches up with soil moisture data
       The timestamp is the time that the last piece of weather station data was collected"""
    et_dict = {"dates": [], "ETo[mm]": []}

    for item in et_data:
        et_dict["dates"].append(item["date"])
        et_dict["ETo[mm]"].append(item["ETo[mm]"])

    new_et_dict = {"dates": [], "ETo[mm]": []}

    reverse_dates = dates[::-1]  # Reverses the dates list
    last_date = dates[0]
    total_days = len(et_dict["dates"])
    day = 1
    for date in reverse_dates:
        if et_dict["dates"][-day] == date:  # New day
            new_et_dict["dates"].append(date)
            new_et_dict["ETo[mm]"].append(et_dict["ETo[mm]"][-day])
            day += 1
        elif date < et_dict["dates"][0]:
            new_et_dict["dates"].append(date)
            new_et_dict["ETo[mm]"].append(0)
        else:
            new_et_dict["dates"].append(date)
            new_et_dict["ETo[mm]"].append(et_dict["ETo[mm]"][-day])

    return new_et_dict


########################################################################################################################
def pessl_data_handler(customer_info, time_period='day'):
    """Just gets all data fresh from fieldclimate"""
    station_data_dict = {}
    data_up_to_date = False

    for id in customer_info["station_id"]:
        filename = "{0}/{0}_{1}.csv".format(customer_info['customer_name'][0], id)

        response_main = get_data(id)
        response_et = get_et(id)

        data_parsed = response_main.json()     # Turns JSON object into a python dictionary of dictionaries
        et_data_parsed = response_et.json()
        sensor_data = data_parsed['data'] # Isolates the dictionary containing sensor data
        dates = data_parsed['dates']      # Isolates the dictionary containing the timestaps for each data point in data
        et_data = format_et_data(et_data_parsed, dates)

        matrix = create_matrix(sensor_data, dates, et_data)

        write_to_csv(matrix, filename)

        if(time_period == "day"):
            day_matrix = [[0 for x in range(len(matrix[0]))] for y in range(26)]
            i = 0
            while(i < 26):
                day_matrix[i] = matrix[i]
                i += 1
            pessl_dict = create_dictionary(day_matrix)

        elif(time_period == "all"):
            pessl_dict = create_dictionary(matrix)

        station_data_dict["{}".format(id)] = pessl_dict

    return station_data_dict

########################################################################################################################
def old_pessl_data_handler(customer_info, time_period='day'):
    station_data_dict = {}
    data_up_to_date = False

    for id in customer_info["station_id"]:
        filename = "{0}/{0}_{1}.csv".format(customer_info['customer_name'][0], id)
        file_exists = os.path.isfile(filename)

        if file_exists:
            (timestamp, last_date) = find_last_timestamp(filename)
            pessl_timestamp = check_fieldclimate(id)
            date_range_dict = pessl_timestamp.json()  # want to check if the max_date and timestamp are equivilent
            data_up_to_date = check_dates(max_date, date_range_dict['max_date'])

            print(last_date, pessl_timestamp.json())

            response_main = get_data(id, timestamp)
            response_et = get_et(id, timestamp)
        else:
            response_main = get_data(id)
            response_et = get_et(id)

        try:
            data_parsed = response_main.json()     # Turns JSON object into a python dictionary of dictionaries
        except json.decoder.JSONDecodeError:
            # No new data to be got =- is this strictly true? could check the response instead
            print('Data up to date')
            data_up_to_date = True

        try:
            et_data_parsed = response_et.json()
        except json.decoder.JSONDecodeError:
            print('Data up to date')

        if(data_up_to_date is False):
            print(data_parsed)
            sensor_data = data_parsed['data'] # Isolates the dictionary containing sensor data
            dates = data_parsed['dates']      # Isolates the dictionary containing the timestaps for each data point in data
            unformatted_et_data = et_data_parsed["ETo[mm]"]

            et_data = format_et_data(et_data, dates)

            new_matrix = create_matrix(sensor_data, et_data, dates)

            if file_exists:
                old_matrix = import_matrix(filename)
                matrix = append_to_matrix(old_matrix, new_matrix)
            else:
                matrix = new_matrix
        else:
            matrix = import_matrix(filename)

        write_to_csv(matrix, filename)

        if(time_period == "day"):
            day_matrix = [[0 for x in range(len(matrix[0]))] for y in range(26)]
            i = 0
            while(i < 26):
                day_matrix[i] = matrix[i]
                i += 1
            pessl_dict = create_dictionary(day_matrix)

        elif(time_period == "all"):
            pessl_dict = create_dictionary(matrix)

        station_data_dict["{}".format(id)] = pessl_dict

    return station_data_dict

def pessl_data_handler_test():
    matrix = import_matrix(filename)
    return matrix