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

if __name__ == "__main__":
    # First, pull customer data - givs a dictionary of lists
    customer_info = database_handler.data_reader(customer_name)

    # This returns a dictionary with station IDs as keys and the values as the data dictionaries
    pessl_data_dict = pessl.pessl_data_handler(customer_info, "all")

    print("PESSL DATA")
    print(pessl_data_dict)

    errors = {}

    for key in pessl_data_dict:
        (errors[key], pessl_columns_index) = errorchecks.error_checker(pessl_data_dict[key])

    print("ERRORS")
    print(errors)

    print("COLUMN INDEX")
    print(pessl_columns_index)

    # # weather_mat = jimhickey.get_weather()
    #
    #
    # # if len(errors) == 1:
    # #     message = "No errors detected"
    # # else:
    # # else:
    # #     for error in errors:
    # #         message = message + '{} \n'.format(error)
    #

    soil_moisture_data = []

    for key in pessl_data_dict:
        i = 0
        for row in pessl_data_dict[key]:
            if i >= 2:
                soil_moisture_data.insert(0, row[pessl_columns_index["EAG Soil moisture"]["avg1"]])
            i += 1

        irrigator_manager.grapher(soil_moisture_data)
    #
    # html = Write_HTML.send_email(errors)
    #
    # emailer.sendemail(you, subject, html)

