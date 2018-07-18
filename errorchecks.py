"""Module handles error checking of the station"""

"""These numbers need to be found automatically by looking at the column headers"""
TIME_COL = 0
WIND_COL = 4
MAXWIND_COL = 5
RAIN_COL = 3
LEAFWET_COL = 7
SOLAR_COL = 1
PV_COL = 2
HUM_COL = 12

MAX_WIND_THRESH = 25 # kmh

def get_data(data, col_number):
    new_data = []

    count = 0
    for row in data:
        if(count > 26): # only take a days worth of data
            break
        elif(count >= 2):
            new_data.append(row[col_number])
        count += 1

    return new_data

def get_max_data(data):
    """Gives the max value from a set and the corresponding index number in dictionary format"""
    max_dict = {'value': 0, 'hour': 0}

    count = 0
    for value in data:
        if(max_dict['value'] < value):
            max_dict['value'] = value
            max_dict['hour'] = count

        count += 1

    return max_dict

def check_wind_data(wind_data, errors):
    """Checks the wind data to see if there is an extended period of zero values. This would indicate that the wind
       sensor has fallen off or become blocked. Takes a list of wind data as an input"""
    is_error = False

    wind_average = sum(wind_data)/len(wind_data)

    if(wind_average < 1): # If there has been no wind for the past day
       errors.append('Wind sensor not working, could be obstructed, fallen over, or a faulty cable/sensor')


def check_rain_data(rain_data, wind_max, leafwet_data, errors):
    """Checks the rain data for oddities, helps if leaf wetness data is available"""
    #if rain_data and no leaf_wetness - alert me to check, bird tampering or wind, or leaf wetness needs replacing
    #could probably just average over the past day - 24 data points

    rain_sum = sum(rain_data)
    leafwet_sum = sum(leafwet_data)

    if(rain_sum > 1): # If the station thinks there has been rain
        if(leafwet_sum < 1): # If the leaves were not wet - wind tipped bucket or paper perished
            if(wind_max['value'] > MAX_WIND_THRESH): # Then the bucket was probably tipped by the wind
                rain_max = get_max_data(rain_data)

                if((wind_max['hour'] - 1) < rain_max['hour'] and rain_max['hour'] < (wind_max['hour'] + 1)):
                    errors.append('Rain bucket possibly being tipped by the wind')
                else: # The time in which the high winds occurred did not correspond with the recorded rain
                    errors.append('Something might not be right with the rain bucket, not sure what')

            else: # No high winds were recorded, so must be the leaf wetness sensor
                errors.append('Leaf wetness sensor paper might have karked it')

    else: # If the station thinks there hasn't been rain
        if(leafwet_sum > 1): # The leaves are wet - rain bucket could be blocked or maybe it was just dewy? Would need
                             # to compare against the forecast or another nearby station
            errors.append('The rain bucket might be blocked, or there has been lots of dew')


    # if (rain_total > 1): # If significant rainfall occurred, > 1mm
    #     if (leafwet_total < 1): # If the leaves were only wet for a short amount of time
    #         # Leafwetness error - new paper needed
    #     else:
    #         # No worries
    #
    # if (rain_total < 0.2): # If no rainfall recorded

    #if leaf wetness and no rain, rain bucket blocked

def check_solar_panel(solar_data, pv_data, errors):
    """Compares the solar panel voltage output (pv_data) to the solar irradience to check if the solar panel is
       working correctly"""
    threshold = 0.15

    solar_max = 285 # W/m2
    pv_max = 90000 # mv

    solar_sum = sum(solar_data)
    pv_sum = sum(pv_data)

    solar_factor = solar_sum/solar_max
    pv_factor = pv_sum/pv_max

    print(solar_factor)
    print(pv_factor)

    if(pv_factor < (1 - threshold) * pv_factor):
        errors.append('Solar panel disconnected or dirty/blocked')


def error_checker(data):
    """Main function, takes a matrix of weather station data for the past 24hrs and does the corresponding error checks,
       returns an error struct"""
    errors = ['Errors:']

    time_data = get_data(data, TIME_COL)
    wind_data = get_data(data, WIND_COL)
    maxwind_data = get_data(data, MAXWIND_COL)
    rain_data = get_data(data, RAIN_COL)
    leafwet_data = get_data(data, LEAFWET_COL)
    solar_data = get_data(data, SOLAR_COL)
    pv_data = get_data(data, PV_COL)
    hum_data = get_data(data, HUM_COL)

    maxwind_dict = get_max_data(maxwind_data)

    check_rain_data(rain_data, maxwind_dict, leafwet_data, errors)

    check_solar_panel(solar_data, pv_data, errors)

    return errors
