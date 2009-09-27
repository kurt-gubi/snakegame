from __future__ import division
import random

from common import *

import pygame
pygame.init()
from pygame.locals import *

class SnakeEngine(object):
    def __init__(self, rows, columns, n_apples, width=800, height=600, fullscreen=False):
        super(SnakeEngine, self).__init__()
        flags = 0
        if fullscreen:
            flags |= pygame.FULLSCREEN
        pygame.display.set_mode((width, height), flags)

        self.width = width
        self.height = height

        self.bots = {}

        self.new_game(rows, columns, n_apples)

    def new_game(self, rows, columns, n_apples):
        self.board = [[Squares.EMPTY for x in xrange(columns)] for y in xrange(rows)]
        for i in xrange(n_apples):
            x = random.randint(0, columns - 1)
            y = random.randint(0, rows - 1)
            self.board[y][x] = Squares.APPLE

    def add_bot(self, name, bot):
        """
        A bot is a callable object, with this method signature:
            def bot_callable(
                board=[[cell for cell in row] for row in board],
                position=(snake_x, snake_y)
                ):
                return random.choice('RULD')
        """
        self.bots[name] = bot

    def remove_bot(self, name):
        del self.bots[name]

    def draw_board(self):
        rows = len(self.board)
        assert rows > 0
        columns = len(self.board[0])

        board_aspect = columns / rows
        screen_aspect = self.width / self.height
        if board_aspect > screen_aspect:
            # restrict width
            width = self.width
            height = width / board_aspect
        else:
            # restrict height
            height = self.height
            width = height * board_aspect

        xscale = width / columns
        yscale = height / rows

        for y, row in enumerate(self.board):
            for x, cell in enumerate(row):
                r = Rect(y * yscale, x * xscale, xscale, yscale)
                print r

    def run(self):
        self.draw_board()

if __name__ == '__main__':
    from bots import random_bot

    game = SnakeEngine(16, 8, 10)
    game.add_bot('Bob', random_bot)
    game.run()

