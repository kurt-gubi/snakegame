import random

from common import *

import pygame
pygame.init()

class SnakeEngine(object):
    def __init__(self, rows, columns, n_apples, width=800, height=600, fullscreen=False):
        super(SnakeEngine, self).__init__()
        flags = 0
        if fullscreen:
            flags |= pygame.FULLSCREEN
        pygame.display.set_mode((width, height), flags)

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

    def run(self):
        pass

if __name__ == '__main__':
    game = SnakeEngine(8, 16, 10)

