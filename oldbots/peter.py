#!/usr/bin/env python
"""New and improved bot, OPTIMISED!!"""

import random
import sys

EMPTY_TILE = '.'
APPLE_TILE = '*'

WIDTH, HEIGHT, SNAKE_BODY = raw_input().split()
WIDTH = int(HEIGHT)
HEIGHT = int(HEIGHT)

SNAKE_BODY = SNAKE_BODY.lower()
SNAKE_HEAD = SNAKE_BODY.upper()

HEADX = None
HEADY = None

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
    BOARD.append(row)

md_two = {
    (-1, 0, 'l'): ((-2, 0), (-1, 1), (-1, -1)),
    (0, -1, 'u'): ((-1, -1), (1, -1), (0, -2)),
    (1, 0, 'r'): ((2, 0), (1, 1), (1, -1)),
    (0, 1, 'd'): (((0, 2), (-1, 1), (1, 1))),
}

max_score = 0
max_moves = []

for (dx, dy, move), adj in md_two.items():
    score = 0

    try:
        square = get_cell(BOARD, HEADX + dx, HEADY + dy)
    except KeyError:
        continue

    if square == APPLE_TILE:
        score += 2
    elif square != EMPTY_TILE:
        continue # Definitely cannot move here.

    for ddx, ddy in adj:
        try:
            square = get_cell(BOARD, HEADX + ddx, HEADY + ddy)
        except KeyError:
            score -= 1
            continue

        if square == APPLE_TILE:
            score += 2
        elif square == EMPTY_TILE:
            score += 1
        elif square == SNAKE_BODY:
            score -= 1
        elif square.isupper():
            score += 3

    if score == max_score:
        max_moves.append(move)
    elif score > max_score:
        max_score = score
        max_moves = [move]

if max_moves:
    print random.choice(max_moves)
else:
    print 'U' # Suicide!

