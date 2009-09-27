from __future__ import division
import random

from common import *

import pygame
pygame.init()
from pygame.locals import *

class SnakeEngine(object):
    EDGE_COLOR = (255, 255, 255)
    EDGE_WIDTH = 1

    def __init__(self, rows, columns, n_apples, width=800, height=600, fullscreen=False):
        super(SnakeEngine, self).__init__()
        flags = 0
        if fullscreen:
            flags |= pygame.FULLSCREEN
        self.screen = pygame.display.set_mode((width, height), flags)

        self.width = width
        self.height = height

        self.bots = {}

        self.new_game(rows, columns, n_apples)

    def new_game(self, rows, columns, n_apples):
        # make board
        self.board = [[Squares.EMPTY for x in xrange(columns)] for y in xrange(rows)]
        for i in xrange(n_apples):
            x = random.randint(0, columns - 1)
            y = random.randint(0, rows - 1)
            self.board[y][x] = Squares.APPLE

        # make board surface
        board_aspect = columns / rows
        screen_aspect = self.width / self.height
        if board_aspect > screen_aspect:
            # restrict width
            self.board_width = self.width
            self.board_height = self.board_width / board_aspect
        else:
            # restrict height
            self.board_height = self.height
            self.board_width = self.board_height * board_aspect

        self.surface = pygame.Surface((self.board_width, self.board_height))

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

        xscale = self.board_width / columns
        yscale = self.board_height / rows

        for y, row in enumerate(self.board):
            for x, cell in enumerate(row):
                left = int(x * xscale)
                top = int(y * yscale)
                w = int((x + 1) * xscale) - left
                h = int((y + 1) * yscale) - top
                r = Rect(left, top, w, h)
                pygame.draw.rect(self.surface, self.EDGE_COLOR, r,
                                 self.EDGE_WIDTH)

    def run(self):
        # Draw the grid.
        self.draw_board()

        # Center the board.
        x = (self.width - self.board_width) / 2
        y = (self.height - self.board_height) / 2
        self.screen.blit(self.surface, (x, y))

        # Update the display.
        pygame.display.flip()

if __name__ == '__main__':
    from bots import random_bot

    game = SnakeEngine(8, 16, 10)
    game.add_bot('Bob', random_bot)
    game.run()

