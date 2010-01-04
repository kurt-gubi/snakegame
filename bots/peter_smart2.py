#!/usr/bin/env python
"""New and improved bot, OPTIMISED!!"""

import random
import sys

DEBUG = False

# Show tracebacks, then pause for debugging.
if DEBUG:
    sys_excepthook = sys.excepthook
    def excepthook(*args, **kwargs):
        sys_excepthook(*args, **kwargs)
        import time
        time.sleep(10)
    sys.excepthook = excepthook

EMPTY_TILE = '.'
APPLE_TILE = '*'

WIDTH, HEIGHT, SNAKE_BODY = raw_input().split()
WIDTH = int(WIDTH)
HEIGHT = int(HEIGHT)

SNAKE_BODY = SNAKE_BODY.lower()
SNAKE_HEAD = SNAKE_BODY.upper()

HEADX = None
HEADY = None

SNAKE_LENGTH = 0

def get_cell(board, x, y):
    if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
        raise KeyError, 'out of range.'
    return board[y][x]

BOARD = []
for y in xrange(HEIGHT):
    row = raw_input()
    for x, char in enumerate(row):
        if char == SNAKE_HEAD:
            HEADX = x
            HEADY = y
        elif char == SNAKE_BODY:
            SNAKE_LENGTH += 1
    BOARD.append(row)

MOVES = (
    (-1, 0, 'l'),
    (1, 0, 'r'),
    (0, -1, 'u'),
    (0, 1, 'd')
)

def get_score(x, y, n, done=None):
    if done is None:
        done = set()

    done.add((x, y))

    score = 0
    explore = False

    # See if the cell exists.
    try:
        square = get_cell(BOARD, x, y)
    except KeyError:
        return 0

    # Give some extra points for getting an apple.
    if square == APPLE_TILE:
        explore = True
        score += 100

    # Yay - it's empty!
    elif square == EMPTY_TILE:
        explore = True
        score += 50

    elif square.islower():
        score += 2

    elif square.isupper():
        score += 1

    if explore and n > 0:
        # Explore n-1 cells further.
        for dx, dy, move in MOVES:
            nx = x + dx
            ny = y + dy

            if (nx, ny) in done:
                continue

            subscore = get_score(nx, ny, n - 1, done)
            score += subscore / 10

    return score * n

max_score = None
max_moves = []

for dx, dy, move in MOVES:
    score = 0

    x = HEADX + dx
    y = HEADY + dy

    n = (SNAKE_LENGTH + 4) / 2
    n = min([n, 10])
    score = get_score(x, y, n)

#    print 'Score for', move, '=', score

    # Suicide protection squad!
    try:
        square = get_cell(BOARD, x, y)
    except KeyError:
        continue
    else:
        if square not in (APPLE_TILE, EMPTY_TILE):
            continue

    if score == max_score:
        max_moves.append(move)
    elif max_score is None or score > max_score:
        max_score = score
        max_moves = [move]

if max_moves:
    print random.choice(max_moves)
else:
    raise Exception, "No suitable moves found!"

