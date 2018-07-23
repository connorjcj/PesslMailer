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

    pessl_mat = pessl.pessl_data_handler(customer_info)

    print(pessl_mat)

    errors = errorchecks.error_checker(pessl_mat)
    # # weather_mat = jimhickey.get_weather()
    #
    #
    # # if len(errors) == 1:
    # #     message = "No errors detected"
    # # else:
    # #     for error in errors:
    # #         message = message + '{} \n'.format(error)
    #
    # irrigator_manager.grapher(errorchecks.get_data(pessl_mat, SOIL_1))
    #
    # html = Write_HTML.send_email(errors)
    #
    # emailer.sendemail(you, subject, html)

