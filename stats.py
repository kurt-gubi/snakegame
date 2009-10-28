#!/usr/bin/env python

from collections import defaultdict
from pygooglechart import SimpleLineChart
from colour import hash_colour

WIDTH = 600
HEIGHT = 200
RESULTS_FILE = 'results.csv'

def main():
    data = {}
    order = []
    snakes = []
    for line in open(RESULTS_FILE):
        game_id, name, length, life = line[:-1].split(',')
        game_id = int(game_id)
        length = int(length)
        life = float(life)

        if name not in data:
            snakes.append(name)
            data[name] = {}

        if game_id not in order:
            order.append(game_id)

        data[name][game_id] = (length, life)

    length_data = []
    time_data = []
    colours = []
    for name in snakes:
        time_series = []
        length_series = []

        for game_id in order:
            length, time = data[name].get(game_id, (None, None))
            time_series.append(time)
            length_series.append(length)

        colours.append('%2X%2X%2X' % hash_colour(name))

        time_data.append(time_series)
        length_data.append(length_series)

    for filename, data in (('length_chart.png', length_data),
                           ('time_chart.png', time_data)):
        chart = SimpleLineChart(WIDTH, HEIGHT, colours=colours)
        for series in data:
            chart.add_data(series)
        chart.download(filename)

    print 'Chart update!'

if __name__ == '__main__':
    main()

