"""Module handles error checking of the station"""

"""These numbers need to be found automatically by looking at the column headers"""
date_time = 0
solar_radiation = {"avg": None}
solar_panel = {"last": None}
precipitation = {"sum": None}
wind_speed = {"avg": None, "max": None}
battery = {"last": None}
leaf_wetness = {"time": None}
hc_serial_number = {"last": None}
hc_air_temperature = {"avg": None, "max": None, "min": None}
hc_relative_humidity = {"avg": None, "max": None, "min": None}
dew_point = {"avg": None, "min": None}
latitude = {"last": None}
longitude = {"last": None}
altitude = {"last": None}
horizontal_dilusion_of_position = {"last": None}
vpd = {"avg": [], "min": None}
wind_speed_max = {"max": None}
eag_soil_moisture = {"avg1": None, "avg2": None, "avg3": None, "avg4": None, "avg5": None, "avg6": None}
eag_soil_salinity = {"avg1": None, "avg2": None, "avg3": None, "avg4": None, "avg5": None, "avg6": None}
soil_temperature = {"avg1": None, "max1": None, "min1": None, "avg2": None, "max2": None, "min2": None,
                    "avg3": None, "max3": None, "min3": None, "avg4": None, "max4": None, "min4": None,
                    "avg5": None, "max5": None, "min5": None, "avg6": None, "max6": None, "min6": None}



pessl_columns_index = {"Date/Time": date_time, "Solar radiation": solar_radiation, "Solar Panel": solar_panel, "Precipitation": precipitation,
                       "Wind speed": wind_speed, "Battery": battery, "Leaf Wetness": leaf_wetness,
                       "HC Serial Number": hc_serial_number, "HC Air temperature": hc_air_temperature,
                       "HC Relative humidity": hc_relative_humidity, "Dew Point": dew_point, "Latitude": latitude,
                       "Longitude": longitude, "Altitude": altitude,
                       "Horizontal dilusion of position": horizontal_dilusion_of_position, "VPD": vpd,
                       "Wind speed max": wind_speed_max, "EAG Soil moisture": eag_soil_moisture,
                       "Eag soil salinity": eag_soil_salinity, "Soil temperature": soil_temperature}

MAX_WIND_THRESH = 25 # kmh
BATTERY_THRESHOLD = 6050 #mV
########################################################################################################################
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

def get_min_data(data):
    min = None

    if data is not None:
        count = 0
        for value in data:
            if count == 0:
                min = value
            elif min > value:
                min = value

    return min

def get_max_data(data):
    """Gives the max value from a set and the corresponding index number in dictionary format"""
    max_dict = {'value': 0, 'hour': 0}

    if data is not None:
        count = 0
        for value in data:
            if(max_dict['value'] < value):
                max_dict['value'] = value
                max_dict['hour'] = count
            count += 1
    else:
        max_dict = None

    return max_dict


def check_wind_data(wind_data, errors):
    """Checks the wind data to see if there is an extended period of zero values. This would indicate that the wind
       sensor has fallen off or become blocked. Takes a list of wind data as an input"""
    is_error = False

    wind_average = sum(wind_data)/len(wind_data)

    if(wind_average < 1): # If there has been no wind for the past day
        errors['Wind'] = True


def check_rain_data(rain_data, wind_max, leafwet_data, hum_data, errors):
    """Checks the rain data for oddities, helps if leaf wetness data is available"""
    #if rain_data and no leaf_wetness - alert me to check, bird tampering or wind, or leaf wetness needs replacing
    #could probably just average over the past day - 24 data points

    rain_sum = sum(rain_data)
    rain_max = get_max_data(rain_data)

    leafwet_agree = True
    wind_agree = True
    hum_agree = True


    if leafwet_data is not None:
        leafwet_sum = sum(leafwet_data)
    else:
        leafwet_sum = None

    if(rain_sum > 0.8): # If the station thinks there has been rain
        if(leafwet_data is not None):
            if(leafwet_sum < 1): # If the leaves were not wet - wind tipped bucket or paper perished
                leafwet_agree = False
            else:
                leafwet_agree = True

        if(wind_max is not None):
            if(wind_max["value"] > MAX_WIND_THRESH): # Then the bucket was probably tipped by the wind
                if((wind_max["hour"] - 1) < rain_max["hour"] and rain_max["hour"] < (wind_max["hour"] + 1)):
                    wind_agree = False
                else:
                    wind_agree = True

            else:
                wind_agree = True

        if(hum_data is not None):
            if(hum_data[rain_max["hour"]] > 80):
                hum_agree = True

        if(hum_agree is False):
            if(wind_agree is False):
                errors["Rain"] = True # And we know that bucket is being tipped
            else:
                errors["Rain"] = True # Still an error but unclear why
        elif(leafwet_agree is False and wind_agree is True): # so, the leafwetness didn't think there was rain, but humidity was sufficient and there was no wind
            errors["Leaf Wetness"] = True
        else:
            errors["rain"] = False

    else: # If the station thinks there hasn't been rain
        if leafwet_sum is not None:
            if(leafwet_sum > 1): # The leaves are wet - rain bucket could be blocked or maybe it was just dewy? Would need
                                 # to compare against the forecast or another nearby station
                errors['Rain'] = True # Blocked


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

    if(pv_factor < (1 - threshold) * pv_factor):
        errors['Solar'] = True

def check_wind_sensor(wind_data, errors):
    if(sum(wind_data) < 1): # Wind has been very low
        errors["Wind"] = True

def check_battery(battery_data, errors):
    min = get_min_data(battery_data)

    if(min < BATTERY_THRESHOLD):
        errors["Battery"] = True

def error_checker(data):
    """Main function, takes a matrix of weather station data for the past 24hrs and does the corresponding error checks,
       returns an error struct"""
    errors = {'Connection': False, 'Battery': False, 'Solar': False, 'Rain': False, 'Leaf Wetness': False,
              'Temp': False, 'GPS': False, 'Wind': False}

    names = data[0] # First row of data has the names
    other_names = data[1]

    # Could probably create this dictionary from scratch, like the customer database?
    i = 0
    last_value = None

    for value in names:
        if value in pessl_columns_index and value != last_value:
            i2 = 0
            for key in pessl_columns_index[value]:
                pessl_columns_index[value][key] = i + i2
                i2 += 1
            last_value = value
        i += 1

    if(pessl_columns_index["Date/Time"] is not None):
        time_data = get_data(data, pessl_columns_index["Date/Time"])
    else:
        time_data = None
    if(pessl_columns_index["Wind speed max"]["max"] is not None):
        wind_data = get_data(data, pessl_columns_index["Wind speed max"]["max"])
    else:
        wind_data = None
    if(pessl_columns_index["Precipitation"]["sum"] is not None):
        rain_data = get_data(data, pessl_columns_index["Precipitation"]["sum"])
    else:
        rain_data = None
    if(pessl_columns_index["Leaf Wetness"]["time"] is not None):
        leafwet_data = get_data(data, pessl_columns_index["Leaf Wetness"]["time"])
    else:
        leafwet_data = None
    if(pessl_columns_index["Solar radiation"]["avg"] is not None):
        solar_data = get_data(data, pessl_columns_index["Solar radiation"]["avg"])
    else:
        solar_data = None
    if(pessl_columns_index["Solar Panel"]["last"] is not None):
        pv_data = get_data(data, pessl_columns_index["Solar Panel"]["last"])
    else:
        pv_data = None
    if(pessl_columns_index["HC Relative humidity"]["avg"] is not None):
        hum_data = get_data(data, pessl_columns_index["HC Relative humidity"]["avg"])
    else:
        hum_data = None

    battery_data = get_data(data, pessl_columns_index["Battery"]["last"])

    maxwind_dict = get_max_data(wind_data)

    if rain_data is not None and (maxwind_dict is not None or leafwet_data is not None or hum_data is not None):
        check_rain_data(rain_data, maxwind_dict, leafwet_data, hum_data, errors)

    if solar_data is not None and pv_data is not None:
        check_solar_panel(solar_data, pv_data, errors)

    if wind_data is not None:
        check_wind_sensor(wind_data, errors)

    check_battery(battery_data, errors)

    return errors, pessl_columns_index

def check_key(in_dict, key1, key2):
    if key1 in in_dict:
        if key2 in in_dict[key1]: # this should always be true
            return in_dict[key1][key2]
    else:
        return None

def error_checker_dict(data_dict):
    """Same purpose as error checker but dels with the data organised in a dictionary rather than a matrix"""
    errors = {'Connection': False, 'Battery': False, 'Solar': False, 'Rain': False, 'Leaf Wetness': False,
              'Temp': False, 'GPS': False, 'Wind': False}

    time_data = check_key(data_dict, "Date/Time", "hour")

    max_wind_data = check_key(data_dict, "Wind speed", "max")

    rain_data = check_key(data_dict, "Precipitation", "sum")

    leafwet_data = check_key(data_dict, "Leaf Wetness", "time")

    solar_data = check_key(data_dict, "Solar radiation", "avg")

    pv_data = check_key(data_dict, "Solar Panel", "last")

    hum_data = check_key(data_dict, "HC Relative humidity", "avg")

    battery_data = check_key(data_dict, "Battery", "last")

    maxwind_dict = get_max_data(max_wind_data)

    if rain_data is not None and (maxwind_dict is not None or leafwet_data is not None or hum_data is not None):
        check_rain_data(rain_data, maxwind_dict, leafwet_data, hum_data, errors)

    if solar_data is not None and pv_data is not None:
        check_solar_panel(solar_data, pv_data, errors)

    if max_wind_data is not None:
        check_wind_sensor(max_wind_data, errors)

    check_battery(battery_data, errors)

    return errors