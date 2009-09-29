#!/usr/bin/env python

from __future__ import division

import time

import pygame
pygame.init()
from pygame.locals import *

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

class PygameSnakeEngine(SnakeEngine):
    EDGE_COLOR = (255, 255, 255)
    EDGE_WIDTH = 1

    def __init__(self, rows, columns, n_apples, width=800, height=600, fullscreen=False):
        flags = 0
        if fullscreen:
            flags |= pygame.FULLSCREEN
        self.screen = pygame.display.set_mode((width, height), flags)

        self.width = width
        self.height = height

        super(PygameSnakeEngine, self).__init__(rows, columns, n_apples)

    def new_game(self, rows, columns, n_apples):
        super(PygameSnakeEngine, self).new_game(rows, columns, n_apples)

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
                    colour = self.bots[cell.lower()][1]
                    self.surface.fill(colour, r)

                    if cell.isupper(): # Snake head
                        self.surface.blit(self.eyes, r.topleft)

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

    game = PygameSnakeEngine(25, 25, 50)
    game.add_bot(right_bot)
    game.add_bot(random_bot)
    game.add_bot(random_bounds_bot)
    game.add_bot(random_square_bot)
    game.add_bot(BotWrapper('oldbots/peter.py'))
    game.run()

