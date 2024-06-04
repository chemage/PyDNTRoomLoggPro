#!/usr/bin/env python3
# file:   export_rs500_csv.py
# author: Marcel Gerber (me@marcelgerber.ch)
# source: https://github.com/Churro405/dnt_Weatherstation/blob/main/src/read_rs500.py
# Read data from RoomLogg Pro and write to a CSV file.
# requires python >= 3.10

from rs500reader.reader import Rs500Reader
import csv
import datetime


channel_map = {
    '1': 'Living Room',
    '2': 'Bedroom',
    '3': 'Kitchen',
    '4': 'Office',
    '5': 'Hall',
    '6': '',
    '7': '',
    '8': ''
}


def get_and_print():
    reader = Rs500Reader()
    data = reader.get_data()
    print('--------------------------------')
    print('Channel | Temperature | Humidity')
    print('================================')
    for i in range(1, 9, 1):
        chan_data = data.get_channel_data(i)
        if chan_data is not None:
            print('{:7d} | {:8.1f} °C | {:6d} %'.format(i, chan_data.temperature, chan_data.humidity))
    print('================================')

    return data


def export_csv(file:str):
    data = get_and_print()
    if data is not None:
        row = {'datetime': datetime.datetime.now().isoformat()}
        for i in range(1, 9, 1):
            chan_data = data.get_channel_data(i)
            if chan_data is not None:
                row[f"{channel_map[i]} Temp."] = chan_data.temperature
                row[f"{channel_map[i]} Humid."] = chan_data.humidity

        with open(file, 'w+', newline='') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
            csvwriter.writerow(row)


if __name__ == '__main__':
    export_csv()

