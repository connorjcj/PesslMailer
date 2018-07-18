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

me = 'carrfieldstechnology@gmail.com'
login = 'carrfieldstechnology@gmail.com'
password = 'Winter12@'

you = 'connor.jaine@carrfields.co.nz'
subject = 'Pessl Mail'
message = 'test test test how are ya'


if __name__ == "__main__":
    # First, pull the weather data
    pessl_mat = pessl.pessl_data_handler()

    errors = errorchecks.error_checker(pessl_mat)
    # weather_mat = jimhickey.get_weather()


    if len(errors) == 1:
        message = "No errors detected"
    else:
        for error in errors:
            message = message + '{} \n'.format(error)

    emailer.sendemail(you, subject, message)

