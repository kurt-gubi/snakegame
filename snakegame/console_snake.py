#!/usr/bin/env python

from __future__ import division

import time

import curses

from common import *
from snake import SnakeEngine

class ConsoleSnakeEngine(SnakeEngine):
    def new_game(self, *args):
        super(ConsoleSnakeEngine, self).new_game(*args)

        self.window = curses.initscr()
        curses.start_color()

        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)

        self.EMPTY_COLOUR = curses.color_pair(0)
        self.APPLE_COLOUR = curses.color_pair(1)
        self.SNAKE_COLOUR = curses.color_pair(4)

    def draw_board(self):
        # Draw grid.
        for y, row in enumerate(self.board):
            for x, cell in enumerate(row):
                char = '.'
                colour = self.EMPTY_COLOUR

                # Draw the things on the square.
                if cell == Squares.APPLE:
                    char = '@'
                    colour = self.APPLE_COLOUR

                elif cell.isalpha(): # Snake...
#                    colour = self.bots[cell.lower()][1]
                    char = cell
                    colour = self.SNAKE_COLOUR

                self.window.addstr(y, x, char, colour)

    def run(self):
        while self.bots:
            # Clear the screen.
            self.window.erase()

            # Draw the board.
            self.draw_board()

            # Update the display.
            self.window.refresh()
            time.sleep(0.025)

            # Let the snakes move!
            self.update_snakes()

def main(*args):
    import sys
    from processbot import BotWrapper

    rows, columns, apples = map(int, sys.argv[1:4])
    game = ConsoleSnakeEngine(rows, columns, apples)
    for filename in sys.argv[4:]:
        bot = BotWrapper(filename)
        game.add_bot(bot)
    game.run()

if __name__ == '__main__':
    curses.wrapper(main)

