#!/usr/bin/env python

from __future__ import division

import time

import pyglet
pyglet.resource.path = ['images']
pyglet.resource.reindex()

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
    EDGE_WIDTH = 1

    def __init__(self, rows, columns, n_apples):
        super(PygletSnakeEngine, self).__init__(rows, columns, n_apples)

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
                top = int(y * yscale)
                right = int((x + 1) * xscale)
                bottom = int((y + 1) * yscale)
                r = (left, top, right, top, right, bottom, left, bottom)

                # Draw a square.
# width = self.EDGE_WIDTH
                pyglet.graphics.draw(4, pyglet.gl.GL_LINE_LOOP,
                                     ('v2f', r),
                                     ('c4B', self.EDGE_COLOR * 4))

                # Draw the things on the square.
                if cell == Squares.APPLE:
                    w, h = self.apple.size
                    self.apple.blit(top, left, width=w, height=h)

                elif cell.isalpha(): # Snake...
                    colour = self.bots[cell.lower()][1]
#                    self.surface.fill(colour, r)

                    if cell.isupper(): # Snake head
                        w, h = self.eyes.size
                        self.eyes.blit(top, left, width=w, height=h)

    def run(self):
        clock = pygame.time.Clock()

        running = True
        while running and self.bots:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or \
                   (event.type == pygame.KEYDOWN and event.key == K_ESCAPE):
                    running = False
                    break
            if not running: break

            # Clear the screen.
            self.screen.fill((0, 0, 0))
            self.surface.fill((0, 0, 0))

            # Draw the board.
            self.draw_board()

            # Center the board.
            x = (self.width - self.board_width) / 2
            y = (self.height - self.board_height) / 2
            self.screen.blit(self.surface, (x, y))

            # Update the display.
            pygame.display.flip()
            clock.tick(20)

            # Let the snakes move!
            self.update_snakes()

        if running:
            time.sleep(2)

        # Early window close, late process cleanup.
        pygame.display.quit()

if __name__ == '__main__':
    from bots import *
    from oldbot import BotWrapper

    game = PygletSnakeEngine(25, 25, 50)
    game.add_bot(right_bot)
    game.add_bot(random_bot)
    game.add_bot(random_bounds_bot)
    game.add_bot(random_square_bot)
    game.add_bot(BotWrapper('oldbots/peter.py'))
    pyglet.app.run()

