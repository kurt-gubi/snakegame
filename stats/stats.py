#!/usr/bin/env python

from pygooglechart import SimpleLineChart
from collections import defaultdict

WIDTH = 600
HEIGHT = 200

def main():
    data = {}
    order = []
    snakes = []
    for line in open('../results.csv'):
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

    length_chart = SimpleLineChart(WIDTH, HEIGHT)
    time_chart = SimpleLineChart(WIDTH, HEIGHT)

    for name in snakes:
        time_series = []
        length_series = []

        for game_id in order:
            length, time = data[name].get(game_id, (None, None))
            time_series.append(time)
            length_series.append(length)

        time_chart.add_data(time_series)
        length_chart.add_data(length_series)

    length_chart.download('length_chart.png')
    time_chart.download('time_chart.png')

    print 'Chart update!'

if __name__ == '__main__':
    main()

