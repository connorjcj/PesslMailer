'''Function that reads weather data and makes irrigation reccomendations'''

import matplotlib.pyplot as plt

# can also use html hex eg #eeefff
BLUE = "b"
GREEN = "g"
RED = "r"
CYAN = "c"
MAGENTA = "m"
YELLOW = "y"
BLACK = "k"
WHITE = "w"

colours = ["b", "g", "r", "c", "m", "y", "k", "w"]

# Create random data with numpy
import numpy as np

def grapher(data, colour, name):
    data_size = len(data)
    x = list(range(data_size))
    y = data

    plt.plot(x, y, label=name, color=colour)

def change_data_period(soil_moistures, days):
    soil_moistures2 = {}
    data_points = 24 * days

    for key in soil_moistures:
        soil_moistures2[key] = soil_moistures[key][-data_points:]

    return soil_moistures2

def graph_soil_moisture(data_dict, station_id, sum_level=3):
    """Graphs the soil moisture
       Sum level is the depth (in 10mm units) of the root zone"""
    field_capacity = 30
    refill_point = field_capacity * 0.75
    wilting_point = field_capacity * 0.5

    soil_moistures = {}

    soil_moistures["10mm"] = data_dict["EAG Soil moisture"]["avg"][::-1] # [::-1] reverses list order
    soil_moistures["20mm"] = data_dict["EAG Soil moisture2"]["avg"][::-1]
    soil_moistures["30mm"] = data_dict["EAG Soil moisture3"]["avg"][::-1]
    soil_moistures["40mm"] = data_dict["EAG Soil moisture4"]["avg"][::-1]
    soil_moistures["50mm"] = data_dict["EAG Soil moisture5"]["avg"][::-1]
    soil_moistures["60mm"] = data_dict["EAG Soil moisture6"]["avg"][::-1]

    soil_moistures["ET"] = data_dict["ETo[mm]"]["daily"][::-1]

    soil_moistures = change_data_period(soil_moistures, 7)

    root_zone_sum = soil_moistures["10mm"].copy()
    drainage_sum = soil_moistures["{}0mm".format(sum_level+1)].copy()
    soil_moistures["root_zone"] = []
    soil_moistures["drainage"] = soil_moistures["60mm"]

    for x in range(2, 7):
        if x <= sum_level:
            i = 0
            for _ in root_zone_sum:
                root_zone_sum[i] += soil_moistures["{}0mm".format(x)][i]
                i += 1

    i = 0
    for value in root_zone_sum:
        soil_moistures["root_zone"].append(value / sum_level)
        i += 1

    data_size = len(soil_moistures["root_zone"])
    x = list(range(data_size))

    # for x in range(sum_level+1, 7):
    #     grapher(soil_moistures["{}0mm".format(x)], colours[x], "{}0mm".format(x))

    fig, ax1 = plt.subplots()

    color = 'r'
    ax1.set_xlabel('time (d)')
    ax1.set_ylabel('Soil Moisture (%)', color=color)
    ax1.plot(x, soil_moistures["root_zone"], label="root_zone", color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    plt.xlim(xmin=0)
    plt.ylim(ymin=wilting_point)
    (ymin, ymax) = plt.ylim()
    (xmin, xmax) = plt.xlim()

    ax1.axhspan(field_capacity, ymax, xmin, xmax, facecolor='#AFEEEE', alpha=0.5)
    ax1.axhspan(refill_point, field_capacity, xmin, xmax, facecolor='#009A00', alpha=0.5)
    ax1.axhspan(ymin, refill_point, xmin, xmax, facecolor='#FF3232', alpha=0.5)

    ax1.set_aspect('auto')

    plt.ylim(ymin=ymin, ymax=ymax)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'b'
    ax2.set_ylabel('ET', color=color)  # we already handled the x-label with ax1
    ax2.plot(x, soil_moistures["ET"], label="ET", color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    fig.legend()
    # do this for each band

    fig.tight_layout()

    plt.show()

""" This can supposedly give ya different colours
import matplotlib.pyplot as plt

plt.figure()
plt.xlim(0, 5)
plt.ylim(0, 5)

for i in range(0, 5):
    plt.axhspan(i, i+.2, facecolor='0.2', alpha=0.5)
    plt.axvspan(i, i+.5, facecolor='b', alpha=0.5)

plt.show()"""