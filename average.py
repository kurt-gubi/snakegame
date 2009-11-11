from collections import defaultdict
from itertools import imap as map
from operator import itemgetter

RESULTS_FILE = 'results.csv'
results = defaultdict(list)

for line in open(RESULTS_FILE, 'rU'):
    game, name, length, time = line[:-1].split(',')
    length = int(length)
    time = int(time)
    results[name].append((length, time))

def average(items):
    s = 0.0
    l = 0
    for item in items:
        s += item
        l += 1
    return s / l

lengths = []
times = []

for name, series in results.items():
    length_average = average(map(itemgetter(0), series))
    lengths.append((length_average, name))
    time_average = average(map(itemgetter(1), series))
    times.append((time_average, name))

lengths.sort(reverse=True)
times.sort(reverse=True)

print 'Lengths'
print '======='
for length, name in lengths:
    print name, length
print

print 'Times'
print '====='
for time, name in times:
    print name, time

