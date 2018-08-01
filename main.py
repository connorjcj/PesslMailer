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

SOIL_1 = 24
SOIL_2 = 25

me = 'carrfieldstechnology@gmail.com'
login = 'carrfieldstechnology@gmail.com'
password = 'Winter12@'

you = 'connor.jaine@carrfields.co.nz'
subject = 'Pessl Mail'
message = 'test test test how are ya'

customer_name = 'Daniel Lovett'

class Customer:
    def __init__(self, full_name, email_address, subscription_end):
        self.name = full_name
        self.email = email_address
        self.sub_end_date = subscription_end
        self.stations = []

class Station:
    pass

class Probe:
    pass

def make_dashboard(customer):
    """Receives customer info, fetches the data, makes a dashboard and emails this to the customer"""
    # Pull new data for each of the customers stations
    station_list = database_handler.station_reader(customer["customer_name"])

    customer["stations"] = station_list  # Link the stations to the customer, makes things easier

    for station in station_list:
        station["probe_settings"] = database_handler.probe_settings_reader(customer["customer_name"], station["station_id"])

        pessl_data_dict = pessl.pessl_data_handler(customer, "all")


if __name__ == "__main__":
    #  Everything a bit different now
    # pull in customer list, iterate through each person
    # Customer list is a list of dictionaries
    customer_list = database_handler.customer_reader()

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
