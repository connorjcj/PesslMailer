'''The main file for the customr/maintainence email app

The app pulls data from the pessl api and from the openweatherapp api. Comparisons are then made between the two
data sets and within the data sets. These comparisons are used for checking errors in the station eg reporting no rain
when open weather app reported rain indicating a blocked rain gauge etc.

After comparisons are made, an email is sent to the carrfields technology team indicating the errors present at each
station, if any'''

import pessl
import jimhickey
import errorchecks
import emailer
import irrigator_manager
import Write_HTML
import database_handler
import objects
from objects import Customer
from objects import Station
from objects import Probe

def make_dashboard(customer):
    """Receives customer info, fetches the data, makes a dashboard and emails this to the customer"""
    # Pull new data for each of the customers stations
    station_list = database_handler.station_reader_oo(customer.name)

    for station in station_list:
        customer.stations.append(station)  # Link the stations to the customer, makes things easier

    for station in customer.stations:
        probes = database_handler.probe_settings_reader_oo(customer.name, station.id)
        for probe in probes:
            station.probes.append(probe)

        pessl.pessl_data_handler_oo(customer, "all")  # Attaches data in dict form to the station

        print(station.data)


if __name__ == "__main__":
    #  Everything a bit different now
    # pull in customer list, iterate through each person
    # Customer list is a list of customer objects
    customer_list = database_handler.customer_reader_oo()

    for customer in customer_list:
        # Make dashboard for each customer in the list
        make_dashboard(customer)

    # # First, pull customer data - givs a dictionary of lists
    # customer_info = database_handler.data_reader(customer_name)
    #
    # for station_id in customer_info["station_id"]:
    #     customer_info[station_id]["probe_settings"] = database_handler.probe_settings_reader(customer_name, customer_info["station_id"][0])
    #
    # print(customer_info)
    #
    # # This returns a dictionary with station IDs as keys and the values as the data dictionaries
    # pessl_data_dict = pessl.pessl_data_handler(customer_info, "all")
    #
    # print("PESSL DATA")
    # print(pessl_data_dict)
    #
    # errors = {}
    #
    # for key in pessl_data_dict:
    #     (errors[key]) = errorchecks.error_checker_dict(pessl_data_dict[key])
    #
    # print("ERRORS")
    # print(errors)
    #
    # # # weather_mat = jimhickey.get_weather()
    # #
    # #
    # # # if len(errors) == 1:
    # # #     message = "No errors detected"
    # # # else:
    # # # else:
    # # #     for error in errors:
    # # #         message = message + '{} \n'.format(error)
    # #
    # for key in pessl_data_dict:
    #     irrigator_manager.graph_soil_moisture(pessl_data_dict[key], customer_info[key]["probe_settings"], key)
    # #
    # # html = Write_HTML.send_email(errors)
    # #
    # # emailer.sendemail(you, subject, html)
    #
