import random

def right_bot(board, (x, y)):
    return 'R'

def random_bot(board, (x, y)):
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
    return random.choice(moves)

def random_bot2(board, (x, y)):
    move = random_bot(board, (x, y))
    nx, ny = x

