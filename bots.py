import random

from common import *

def right_bot(board, (x, y)):
    return 'R'

def random_bot(board, (x, y)):
    return random.choice('UDLR')

def random_bounds_bot(board, (x, y)):
    height = len(board)
    width = len(board[0])
    moves = []
    if x > 0:
        moves.append('L')
    if x < width - 1:
        moves.append('R')
    if y > 0:
        moves.append('U')
    if y < height - 1:
        moves.append('D')

    move = 'U'
    while moves and move not in moves:
        move = random_bot(board, (x, y))
    return move

def random_square_bot(board, (x, y)):
    def in_bounds(x, y, w, h):
        return x >= 0 and y >= 0 and x < w and y < h

    h = len(board)
    w = len(board[0])

    todo = directions.keys()

    move = random_bot(board, (x, y))
    dx, dy = directions[move]
    nx = x + dx
    ny = y + dy

    while todo and in_bounds(nx, ny, w, h) and \
          board[ny][nx] not in (Squares.EMPTY, Squares.APPLE):
        if move in todo:
            todo.remove(move)
        move = random_bot(board, (x, y))
        dx, dy = directions[move]
        nx = x + dx
        ny = y + dy
    return move

