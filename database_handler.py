import csv
import codecs
import os
import sys
from collections import defaultdict

filename = 'CustomerDatabase.csv'


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

    return(info)
