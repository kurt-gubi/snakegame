import random
from string import ascii_lowercase as lowercase, ascii_uppercase as uppercase
alphabet = lowercase + uppercase

directions = {
    'U': (0, -1),
    'D': (0, 1),
    'L': (-1, 0),
    'R': (1, 0),
}

EMPTY = '.'
APPLE = '*'
WALL = '#'
ICE_CREAM = '+'
SHRINK_POTION = '-'
TELEPORTER = '?'

is_empty = EMPTY.__eq__
is_apple = APPLE.__eq__
is_wall = WALL.__eq__

def is_vacant(cell):
    return cell in (EMPTY, APPLE, ICE_CREAM, SHRINK_POTION, TELEPORTER)

def is_blocking(cell):
    return not is_vacant(cell)

def is_snake(cell):
    return cell in alphabet

def is_snake_head(cell):
    return cell in uppercase

def is_snake_body(cell):
    return cell in lowercase

def is_enemy_snake(cell, me):
    assert me.isupper()
    return is_snake(cell) and cell.upper() != me

def is_my_snake(cell, me):
    assert me.isupper()
    return cell.upper() == me

def get_size(board):
    height = len(board)
    width = len(board[0])
    return width, height

def in_bounds(x, y, width, height):
    return (
        x >= 0 and x < width and
        y >= 0 and y < height
    )

def get_cell(board, x, y, wrap=True):
    width, height = get_size(board)
    if wrap:
        x %= width
        y %= height
    elif not in_bounds(x, y, width, height):
        return None
    return board[y][x]

def get_neighbours(x, y, width, height):
    for d, (dx, dy) in directions.iteritems():
        nx = (x + dx) % width
        ny = (y + dy) % height
        yield d, nx, ny

def max_items(items, alpha=1.0):
    """
    >>> max_items([(1, 'a'), (2, 'b'), (2, 'c'), (0, 'd')])
    [(2, 'b'), (2, 'c')]
    """
    max_score, _ = max(items)
    return [
        (score, item)
        for score, item in items
        if score >= max_score * alpha
    ]

def choose_move(choices, default='U', random=random):
    if not choices:
        return default
    return random.choice(choices)
