#!/usr/bin/env python

from __future__ import division

import sys
import time
import string
import random
from random import randint
from collections import deque
from copy import deepcopy
import traceback

from common import *

class SnakeEngine(object):
    def __init__(self, rows, columns, n_apples, results=False):
        super(SnakeEngine, self).__init__()

        self.letters = list(string.lowercase)
        self.letters.reverse()

        self.bots = {}
        self.results = None
        if results:
            self.results = open('results.csv', 'a+')

        self.new_game(rows, columns, n_apples)

    def get_random_position(self):
        x = randint(0, self.columns - 1)
        y = randint(0, self.rows - 1)
        return (x, y)

    def replace_random(self, old, new):
        for i in xrange(self.rows * self.columns):
            x, y = self.get_random_position()
            if self.board[y][x] == old:
                self.board[y][x] = new
                return x, y

    def new_game(self, rows, columns, n_apples):
        self.start_time = time.time()
        self.game_id = random.randint(0, sys.maxint)

        self.rows = rows
        self.columns = columns

        # make board
        self.board = [[Squares.EMPTY for x in xrange(columns)] for y in xrange(rows)]
        for i in xrange(n_apples):
            x, y = self.get_random_position()
            self.board[y][x] = Squares.APPLE

    def add_bot(self, bot, colour=None):
        """
        A bot is a callable object, with this method signature:
            def bot_callable(
                board=[[cell for cell in row] for row in board],
                position=(snake_x, snake_y)
                ):
                return random.choice('RULD')
        """
        letter = self.letters.pop()

        position = self.replace_random(Squares.EMPTY, letter.upper())
        if position is None:
            raise KeyError, "Could not insert snake into the board."

        if colour is None:
            colour = (randint(0, 255), randint(0, 255), randint(0, 255))
        self.bots[letter] = [bot, colour, deque([position])]
        return letter

    def remove_bot(self, letter):
        letter = letter.lower()

        time_score = time.time() - self.start_time

        for row in self.board:
            for x, cell in enumerate(row):
                if cell.lower() == letter:
                    row[x] = Squares.EMPTY

        bot = self.bots[letter]
        del self.bots[letter]

        if not self.results:
            return

        try:
            name = bot[0].__name__
        except AttributeError:
            pass
        else:
            apple_score = len(bot[2])
            self.results.write('%s,%s,%s,%s\n' % \
                (self.game_id, name, apple_score, time_score))
            self.results.flush()

    def update_snakes(self, directions_id=id(directions)):
        assert id(directions) == directions_id, \
            "The common.directions dictionary has been modified since startup..."

        for letter, (bot, colour, path) in self.bots.items():
            board = deepcopy(self.board)
            try:
                x, y = path[-1]
                d = bot(board, (x, y))

                # Sanity checking...
                assert isinstance(d, basestring), \
                    "Return value should be a string."
                d = d.upper()
                assert d in directions, "Return value should be 'U', 'D', 'L' or 'R'."

                # Get new position.
                dx, dy = directions[d]
                nx = x + dx
                ny = y + dy

                if ny < 0 or ny >= self.rows or nx < 0 or nx >= self.columns:
                    self.remove_bot(letter)
                    continue

                oldcell = self.board[ny][nx]
                if oldcell in (Squares.EMPTY, Squares.APPLE):
                    # Move snake forward.
                    self.board[ny][nx] = letter.upper()
                    path.append((nx, ny))

                    # Make old head into body.
                    self.board[y][x] = letter.lower()

                    if oldcell == Squares.APPLE:
                        # Add in an apple to compensate.
                        self.replace_random(Squares.EMPTY, Squares.APPLE)
                    else:
                        # Remove last part of snake.
                        ox, oy = path.popleft()
                        self.board[oy][ox] = Squares.EMPTY
                else:
                    self.remove_bot(letter)

            except:
                print "Exception in bot %s (%s):" % (letter.upper(), bot)
                print '-'*60
                traceback.print_exc()
                print '-'*60
                self.remove_bot(letter)

