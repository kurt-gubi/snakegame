from pyglet_snake import PygletSnakeEngine

def my_bot(board, position):
    x, y = position
    print board[y][x]
    return 'U'

p = PygletSnakeEngine(25, 25, 10)
p.add_bot(my_bot)
p.run()

