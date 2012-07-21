from __future__ import absolute_import

import curses
import time

from snakegame import common

class Viewer(object):
    def __init__(self, engine, *args, **kwargs):
        super(Viewer, self).__init__(*args, **kwargs)

        self.engine = engine

        self.window = curses.initscr()
        curses.start_color()

        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)

        self.EMPTY_COLOUR = curses.color_pair(0)
        self.APPLE_COLOUR = curses.color_pair(1)
        self.SNAKE_COLOUR = curses.color_pair(4)

    def draw_board(self, board):
        # Draw grid.
        for y, row in enumerate(board):
            for x, cell in enumerate(row):
                char = '.'
                colour = self.EMPTY_COLOUR

                # Draw the things on the square.
                if cell == common.APPLE:
                    char = '@'
                    colour = self.APPLE_COLOUR

                elif cell.isalpha(): # Snake...
#                    colour = self.bots[cell.lower()][1]
                    char = cell
                    colour = self.SNAKE_COLOUR

                self.window.addstr(y, x, char, colour)

    def run(self):
        for board in self.engine:
            # Clear the screen.
            self.window.erase()

            # Draw the board.
            self.draw_board(board)

            # Update the display.
            self.window.refresh()
            time.sleep(0.025)

