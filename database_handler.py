import csv
import codecs
import os
import sys
from objects import Customer
from objects import Station
from objects import Probe
from collections import defaultdict

filename = 'CustomerDatabase.csv'

def probe_settings_reader_oo(customer_name, station_id):
    file = open("database/{0}/{1}/probes_{1}.csv".format(customer_name, station_id))

    reader = csv.reader(file)

    probes = []

    i = 0
    for row in reader:
        if i == 0:  # First row with probe name
            probe_name = row[0]
            i += 1
        elif i == 1:
            i += 1  # This row contains the keys - should be like so probe_type,10mm,20mm,30mm,40mm,50mm,60mm
        elif i == 2:
            probes.append(Probe(row[0], row[1], row[2:]))
            i = 0

    file.close()

    return probes

def probe_settings_reader(customer_name, station_id):
    file = open("database/{0}/{1}/probes_{1}.csv".format(customer_name, station_id))

    reader = csv.reader(file)

    probe_dict = {}

    keys = []
    values = []
    key = None

    i = 0
    for row in reader:
        if i == 0:  # First row with probe name
            key = row[0]
            i += 1
        elif i == 1:
            for value in row:
                keys.append(value)
            i += 1
        elif i == 2:
            for value in row:
                values.append(value)
            probe = dict(zip(keys, values))
            probe_dict[key] = probe
            i = 0

    file.close()

    return probe

def customer_reader_oo():
    """ Reads the customer info from the customer_list file, containing the customer's name, email and date that their
           subscription ends, this can be modified to add more data that is specific to the customer
           Data is read into a customer object" """

    filename = "database/customer_list.csv"
    file = open(filename, "r", encoding="utf-8-sig")
    reader = csv.reader(file)

    customers = []

    i = 0
    for row in reader:
        if i >= 1:  # Skip header row
            customers.append(Customer(row[0], row[1], row[2]))
        i += 1

    file.close()

    return customers

def customer_reader():
    """ Reads the customer info from the customer_list file, containing the customer's name, email and date that their
       subscription ends, this can be modified to add more data that is specific to the customer
       Data is read into a list of dictionaries - with one dictionary in the list per customer
       Dictionary indexed by "customer_name", "email_address", and "subscription_end" """
    filename = "database/customer_list.csv"
    file = open(filename, "r", encoding="utf-8-sig")
    reader = csv.reader(file)

    customers = []
    keys = []
    values = []

    i = 0
    for row in reader:
        if i == 0:  # first row gives the keys
            keys = row
        else:
            values = row
            customer = dict(zip(keys, values))
            customers.append(customer)
        i += 1

    file.close()

    return customers

def station_reader_oo(customer_name):
    """ Reads station list into a list of dictionaries. Each dictionary has the following indices:
       station_id,station_type,gps_lat,gps_lon,connection,battery,solar_panel,rain_bucket,leaf_wetness,temperature,
       location,eto,forecast"""
    filename = "database/{}/station_list.csv".format(customer_name)
    file = open(filename, "r", encoding="utf-8-sig")
    reader = csv.reader(file)

    stations = []

    i = 0
    for row in reader:
        if i >= 1:
            stations.append(Station(row[0], row[1], row[2], row[3], row[4], row[5], row[6:]))
        i += 1

    file.close()

    return stations

def station_reader(customer_name):
    """ Reads station list into a list of dictionaries. Each dictionary has the following indices:
       station_id,station_type,gps_lat,gps_lon,connection,battery,solar_panel,rain_bucket,leaf_wetness,temperature,
       location,eto,forecast"""
    filename = "database/{}/station_list.csv".format(customer_name)
    file = open(filename, "r", encoding="utf-8-sig")
    reader = csv.reader(file)

    stations = []
    keys = []
    values = []

    i = 0
    for row in reader:
        if i == 0:
            keys = row
        else:
            values = row
            station = dict(zip(keys, values))
            stations.append(station)
        i += 1

    file.close()

    return stations

def data_reader(customer_name):
    file = open(filename, 'r', encoding="utf-8-sig")

    reader = csv.reader(file)

    keys = []

    i = 0
    for row in reader:
        if i == 0: # First row
            customer_info = [[] for _ in range(len(row))]
            for value in row:
                keys.append(value)

        elif row[0] == customer_name:
            k = 0
            for value in row:
                customer_info[k].append(value)
                k += 1
        i += 1

    info = dict(zip(keys, customer_info))

    file.close()

    return info
