'''Function that reads weather data and makes irrigation reccomendations'''

import matplotlib.pyplot as plt


# Create random data with numpy
import numpy as np


def grapher(data):
    print(data)
    data_size = len(data)
    x = list(range(data_size))
    y = data

    plt.scatter(x, y, label='Soil Moisture', color='k')

    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Interesting Graph\nCheck it out')
    plt.legend()
    plt.show()
