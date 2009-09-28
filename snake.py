#!/usr/bin/env python

from __future__ import division

import string
import random

from common import *

import pygame
pygame.init()
from pygame.locals import *

def scale_aspect((source_width, source_height), (target_width, target_height)):
    source_aspect = source_width / source_height
    target_aspect = target_width / target_height
    if source_aspect > target_aspect:
        # restrict width
        width = target_width
        height = width / source_aspect
    else:
        # restrict height
        height = target_height
        width = height * source_aspect
    return (width, height)

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

        self.letters = list(string.lowercase)
        self.letters.reverse()

        self.bots = {}

        self.new_game(rows, columns, n_apples)

    def get_random_position(self):
        x = random.randint(0, self.columns - 1)
        y = random.randint(0, self.rows - 1)
        return (x, y)

    def new_game(self, rows, columns, n_apples):
        self.rows = rows
        self.columns = columns

        # make board
        self.board = [[Squares.EMPTY for x in xrange(columns)] for y in xrange(rows)]
        for i in xrange(n_apples):
            x, y = self.get_random_position()
            self.board[y][x] = Squares.APPLE

        # make board surface
        self.board_width, self.board_height = scale_aspect(
            (columns, rows), (self.width, self.height)
        )
        self.surface = pygame.Surface((self.board_width, self.board_height))

        # load sprites
        xscale = self.board_width / self.columns
        yscale = self.board_height / self.rows

        def load_image(image):
            new_size = scale_aspect(image.get_size(), (xscale, yscale))
            return pygame.transform.smoothscale(image, new_size)

        self.apple = load_image(Sprites.APPLE)
        self.eyes = load_image(Sprites.EYES)

    def add_bot(self, bot):
        """
        A bot is a callable object, with this method signature:
            def bot_callable(
                board=[[cell for cell in row] for row in board],
                position=(snake_x, snake_y)
                ):
                return random.choice('RULD')
        """
        letter = self.letters.pop()

        for i in xrange(self.rows * self.columns):
            x, y = self.get_random_position()
            if self.board[y][x] == Squares.EMPTY:
                break
        else:
            raise KeyError, "Could not insert snake into the board."

        colour = (255, 0, 0)
        self.bots[letter] = (bot, (x, y), colour)
        self.board[y][x] = letter.upper()
        return letter

    def remove_bot(self, letter):
        del self.bots[letter]

    def draw_board(self):
        xscale = self.board_width / self.columns
        yscale = self.board_height / self.rows

        # Draw grid.
        for y, row in enumerate(self.board):
            for x, cell in enumerate(row):
                left = int(x * xscale)
                top = int(y * yscale)
                w = int((x + 1) * xscale) - left
                h = int((y + 1) * yscale) - top
                r = Rect(left, top, w, h)

                # Draw a square.
                pygame.draw.rect(self.surface, self.EDGE_COLOR, r,
                                 self.EDGE_WIDTH)

                # Draw the things on the square.
                if cell == Squares.APPLE:
                    self.surface.blit(self.apple, r.topleft)

                elif cell.isalpha(): # Snake...
                    colour = self.bots[cell.lower()][2]
                    self.surface.fill(colour, r)

                    if cell.isupper(): # Snake head
                        self.surface.blit(self.eyes, r.topleft)

    def run(self):
        # Draw the board.
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
    game.add_bot(random_bot)
    game.run()

