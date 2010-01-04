#!/usr/bin/env python

from __future__ import division

import time

import pyglet
pyglet.resource.path = ['images']
pyglet.resource.reindex()

from pyglet.gl import *

from common import *
from snake import SnakeEngine

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

class PygletSnakeEngine(SnakeEngine, pyglet.window.Window):
    EDGE_COLOR = (255, 255, 255, 255)
    EDGE_WIDTH = 2

    def __init__(self, rows, columns, n_apples, *args, **kwargs):
        super(PygletSnakeEngine, self).__init__(rows, columns, n_apples, *args, **kwargs)

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        pyglet.clock.schedule_interval(lambda t: self.update_snakes(), 0.025)

    def new_game(self, rows, columns, n_apples):
        super(PygletSnakeEngine, self).new_game(rows, columns, n_apples)

        # make board surface
        self.board_width, self.board_height = scale_aspect(
            (columns, rows), (self.width, self.height)
        )

        # load sprites
        xscale = self.board_width / self.columns
        yscale = self.board_height / self.rows

        self.apple = pyglet.resource.image('apple.png')
        self.apple.size = scale_aspect(
            (self.apple.width, self.apple.height),
            (xscale, yscale)
        )
        self.eyes = pyglet.resource.image('eyes.png')
        self.eyes.size = scale_aspect(
            (self.eyes.width, self.eyes.height),
            (xscale, yscale)
        )

    def on_draw(self):
        self.clear()

        xscale = self.board_width / self.columns
        yscale = self.board_height / self.rows

        # Draw grid.
        for y, row in enumerate(self.board):
            for x, cell in enumerate(row):
                left = int(x * xscale)
                top = self.height - int(y * yscale)
                right = int((x + 1) * xscale)
                bottom = self.height - int((y + 1) * yscale)
                r = (left, top, right, top, right, bottom, left, bottom)

                # Draw a square.
                glLineWidth(self.EDGE_WIDTH)
                pyglet.graphics.draw(4, GL_LINE_LOOP,
                                     ('v2f', r),
                                     ('c4B', self.EDGE_COLOR * 4))

                # Draw the things on the square.
                if cell == Squares.APPLE:
                    w, h = self.apple.size
                    self.apple.blit(left + (xscale - w) / 2.0, top - h, width=w, height=h)

                elif cell.isalpha(): # Snake...
                    colour = self.bots[cell.lower()][1] + (255,)
                    glPolygonMode(GL_FRONT, GL_FILL)
                    pyglet.graphics.draw(4, GL_POLYGON,
                                         ('v2f', r),
                                         ('c4B', colour * 4),
                    )

                    if cell.isupper(): # Snake head
                        w, h = self.eyes.size
                        self.eyes.blit(left, top - h, width=w, height=h)

    def update_snakes(self, *args):
        if not self.bots:
            pyglet.app.exit()
        super(PygletSnakeEngine, self).update_snakes(*args)

    def run(self):
        pyglet.app.run()

if __name__ == '__main__':
    from bots import random_bounds_bot, random_square_bot
    from processbot import BotWrapper

    game = PygletSnakeEngine(25, 25, 50, results=True)
    game.add_bot(random_bounds_bot)
    game.add_bot(random_square_bot)
    for i in xrange(2):
        game.add_bot(BotWrapper('bots/peter.py'))
    game.run()

