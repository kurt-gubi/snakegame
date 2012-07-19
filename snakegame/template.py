from pyglet_snake import PygletSnakeEngine

def your_name_here_bot(board, position):
    x, y = position
    mychar = board[y][x]
    return 'U'

# Test code to run the snake game.
# Leave the if statement as is, otherwise I won't be able to run your bot with
# the other bots.
if __name__ == '__main__':
    p = PygletSnakeEngine(25, 25, 10)
    p.add_bot(your_name_here_bot)
    p.run()

