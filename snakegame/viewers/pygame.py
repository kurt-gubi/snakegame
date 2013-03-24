from __future__ import absolute_import

import time

import pkg_resources

import pygame
from pygame.image import load
pygame.init()

from snakegame import common
from snakegame.utils import scale_aspect

sprite_cache = {}

def load_sprite(filename):
    if filename in sprite_cache:
        return sprite_cache[filename]

    f = pkg_resources.resource_stream('snakegame', filename)
    image = load(f).convert_alpha()

    sprite_cache[filename] = image
    return image

def load_image(filename, xscale, yscale):
    image = load_sprite(filename)
    w, h = scale_aspect(image.get_size(), (xscale, yscale))
    return pygame.transform.smoothscale(image, (int(w), int(h)))

class Viewer(object):
    EDGE_COLOR = (255, 255, 255)
    EDGE_WIDTH = 1

    def __init__(self, engine, width=800, height=600, fullscreen=False, **kwargs):
        super(Viewer, self).__init__(**kwargs)

        self.engine = engine

        flags = 0
        if fullscreen:
            flags |= pygame.FULLSCREEN
        self.screen = pygame.display.set_mode((width, height), flags)

        self.width = width
        self.height = height

        self.columns = None
        self.rows = None

    def on_resize(self):
        # make board surface
        self.board_width, self.board_height = scale_aspect(
            (self.columns, self.rows), (self.width, self.height)
        )
        self.surface = pygame.Surface((self.board_width, self.board_height))

        # load sprites
        xscale = self.board_width / self.columns
        yscale = self.board_height / self.rows

        self.items = {
            common.APPLE : 'images/apple.png',
            common.ICE_CREAM : 'images/icecream.png',
            common.SHRINK_POTION : 'images/shrinkpotion.png',
            common.WALL : 'images/wall.png',
        }
        for item in self.items:
            self.items[item] = load_image(self.items[item], xscale, yscale)
        self.eyes = load_image('images/eyes.png', xscale, yscale)

    def draw_board(self, board):
        xscale = self.board_width / self.columns
        yscale = self.board_height / self.rows

        # Draw grid.
        for y, row in enumerate(board):
            for x, cell in enumerate(row):
                left = int(x * xscale)
                top = int(y * yscale)
                w = int((x + 1) * xscale) - left
                h = int((y + 1) * yscale) - top
                r = pygame.Rect(left, top, w, h)

                # Draw a square.
                pygame.draw.rect(self.surface, self.EDGE_COLOR, r,
                                 self.EDGE_WIDTH)

                # Draw the things on the square.
                if cell in self.items:
                    self.surface.blit(self.items[cell], r.topleft)

                elif common.is_snake(cell):
                    bot = self.engine.bots[cell.lower()]
                    colour = bot[1]
                    self.surface.fill(colour, r)

                    if common.is_snake_head(cell):
                        self.surface.blit(self.eyes, r.topleft)

    def run(self):
        clock = pygame.time.Clock()

        running = True

        for board in self.engine:
            columns, rows = common.get_size(board)
            if columns != self.columns or rows != self.rows:
                self.columns = columns
                self.rows = rows
                self.on_resize()

            for event in pygame.event.get():
                if event.type == pygame.QUIT or \
                   (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    running = False
                    break
            if not running: break

            # Clear the screen.
            self.screen.fill((0, 0, 0))
            self.surface.fill((0, 0, 0))

            # Draw the board.
            self.draw_board(board)

            # Center the board.
            x = (self.width - self.board_width) / 2
            y = (self.height - self.board_height) / 2
            self.screen.blit(self.surface, (x, y))

            # Update the display.
            pygame.display.flip()
            clock.tick(20)

        if running:
            time.sleep(2)

