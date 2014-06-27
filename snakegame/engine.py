from collections import defaultdict, deque
from copy import deepcopy
from random import Random
from string import ascii_lowercase as lowercase
import time
import traceback

import six
from six.moves import xrange

from snakegame.colour import hash_colour
from snakegame import common

SOFT_TIME_LIMIT = 0.5
HARD_TIME_LIMIT = 1.0

class Engine(object):
    def __init__(
        self,
        rows, columns, n_apples,
        n_ice_creams=0, n_shrink_potions=0, n_walls=0,
        wrap=True,
        random=None,
        *args, **kwargs
    ):
        super(Engine, self).__init__(*args, **kwargs)

        if random is None:
            random = Random()
        self.random = random

        self.wrap = wrap
        self.bots = {}

        self.new_game(
            rows, columns, n_apples,
            n_ice_creams, n_shrink_potions, n_walls,
        )

    def get_random_position(self):
        x = self.random.randrange(0, self.columns)
        y = self.random.randrange(0, self.rows)
        return (x, y)

    def replace_random(self, old, new):
        for i in xrange(self.rows * self.columns):
            x, y = self.get_random_position()
            if self.board[y][x] == old:
                self.board[y][x] = new
                return x, y

    def add_items(self, item, amount):
        for i in xrange(amount):
            x, y = self.get_random_position()
            self.board[y][x] = item

    def shrink(self, path):
        if len(path) > 1:
            x, y = path.popleft()
            self.board[y][x] = common.EMPTY

    def new_game(
        self,
        rows, columns, n_apples,
        n_ice_creams, n_shrink_potions, n_walls,
    ):
        self.game_ticks = 0

        self.letters = list(lowercase)
        self.letters.reverse()

        self.rows = rows
        self.columns = columns

        self.messages_by_team = defaultdict(dict)

        # make board
        self.board = [[common.EMPTY for x in xrange(columns)] for y in xrange(rows)]
        self.add_items(common.APPLE, n_apples)
        self.add_items(common.ICE_CREAM, n_ice_creams)
        self.add_items(common.SHRINK_POTION, n_shrink_potions)
        self.add_items(common.WALL, n_walls)

    def add_bot(self, bot, team=None, colour=None):
        """
        A bot is a callable object, with this method signature:
            def bot_callable(
                board=[[cell for cell in row] for row in board],
                position=(snake_x, snake_y)
                ):
                return random.choice('RULD')

        If team is not None, this means you will get a third parameter,
        containing messages from the other bots on your team.
        """
        letter = self.letters.pop()

        name = bot.__name__
        if colour is None:
            colour = hash_colour(name)

        position = self.replace_random(common.EMPTY, letter.upper())
        if position is None:
            raise KeyError("Could not insert snake into the board.")

        self.bots[letter] = [bot, colour, deque([position]), team]
        return letter

    def remove_bot(self, letter):
        letter = letter.lower()

        for row in self.board:
            for x, cell in enumerate(row):
                if cell.lower() == letter:
                    row[x] = common.EMPTY

        del self.bots[letter]

    def update_snakes(self):
        self.game_ticks += 1

        for letter, (bot, colour, path, team) in list(self.bots.items()):
            board = deepcopy(self.board)
            try:
                x, y = path[-1]

                start = time.time()

                if team is None:
                    d = bot(board, (x, y))
                else:
                    messages = self.messages_by_team[team]
                    d, message = bot(board, (x, y), messages)

                    assert isinstance(message, str), \
                        "Message should be a byte string, not %s (%r)." % (
                            type(message),
                            message,
                        )
                    messages[letter] = message

                end = time.time()
                delta = end - start
                assert delta < HARD_TIME_LIMIT, 'Exceeded hard time limit.'
                if delta >= SOFT_TIME_LIMIT:
                    print('Bot %s (%r) exceeded soft time limit.' % (letter.upper(), bot))

                # Sanity checking...
                assert isinstance(d, six.string_types), \
                    "Return value should be a string."
                d = d.upper()
                assert d in common.directions, "Return value should be 'U', 'D', 'L' or 'R'."

                # Get new position.
                dx, dy = common.directions[d]
                nx = x + dx
                ny = y + dy

                if self.wrap:
                    ny %= self.rows
                    nx %= self.columns
                else:
                    if ny < 0 or ny >= self.rows or nx < 0 or nx >= self.columns:
                        self.remove_bot(letter)
                        continue

                oldcell = self.board[ny][nx]
                if common.is_vacant(oldcell):
                    # Move snake forward.
                    self.board[ny][nx] = letter.upper()
                    path.append((nx, ny))
                    tail = path[0]

                    # Make old head into body.
                    self.board[y][x] = letter.lower()

                    if oldcell == common.APPLE:
                        path.appendleft(tail)
                        self.replace_random(common.EMPTY, common.APPLE)
                    elif oldcell == common.ICE_CREAM:
                        for i in xrange(3):
                            path.appendleft(tail)
                        self.replace_random(common.EMPTY, common.ICE_CREAM)
                    elif oldcell == common.SHRINK_POTION:
                        self.shrink(path)
                        self.replace_random(common.EMPTY, common.SHRINK_POTION)

                    self.shrink(path)

                else:
                    self.remove_bot(letter)

            except:
                print("Exception in bot %s (%s):" % (letter.upper(), bot))
                print('-'*60)
                traceback.print_exc()
                print('-'*60)
                self.remove_bot(letter)

    def __iter__(self):
        yield self.board
        while self.bots:
            self.update_snakes()
            yield self.board

