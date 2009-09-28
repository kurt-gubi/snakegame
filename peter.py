#!/usr/bin/env python
"""New and improved bot, OPTIMISED!!"""

import random
import sys

from common import *

def peter_bot(board, (HEADX, HEADY)):
    HEIGHT = len(board)
    WIDTH = len(board[0])
    SNAKE_BODY = board[HEADY][HEADX]

    SNAKE_BODY = SNAKE_BODY.lower()
    SNAKE_HEAD = SNAKE_BODY.upper()

    def get_cell(board, x, y):
        if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
            raise KeyError, 'out of range.'
        return board[y][x]

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
            square = get_cell(board, HEADX + dx, HEADY + dy)
        except KeyError:
            continue

        if square == Squares.APPLE:
            score += 2
        elif square != Squares.EMPTY:
            continue # Definitely cannot move here.

        for ddx, ddy in adj:
            try:
                square = get_cell(board, HEADX + ddx, HEADY + ddy)
            except KeyError:
                score -= 1
                continue

            if square == Squares.APPLE:
                score += 2
            elif square == Squares.EMPTY:
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
        return random.choice(max_moves)
    else:
        return 'U' # Suicide!

