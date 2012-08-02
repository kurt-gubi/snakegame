from random import choice

def random_avoid_bot(board, position):
    x, y = position
    height = len(board)
    width = len(board[0])

    valid_moves = []

    left = board[y][(x - 1) % width]
    if left == '.' or left == '*':
        valid_moves.append('L')

    right = board[y][(x + 1) % width]
    if right == '.' or right == '*':
        valid_moves.append('R')

    up = board[(y - 1) % height][x]
    if up == '.' or up == '*':
        valid_moves.append('U')

    down = board[(y + 1) % height][x]
    if down == '.' or down == '*':
        valid_moves.append('D')

    return choice(valid_moves)
