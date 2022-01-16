from snakegame.engine import Engine
from snakegame.viewers.pyglet import Viewer
import random

def left_bot(board, position):
  return 'L'

def random_bot(board, position):
  return random.choice( ['U', 'D', 'L', 'R'] )

def right_bot(board, position):
  return 'R'

if __name__ == '__main__':
  from snakegame.engine import Engine
  from snakegame.viewers.pyglet import Viewer
  engine = Engine(10, 10, 25)
  engine.add_bot(left_bot)
  engine.add_bot(right_bot)
  engine.add_bot(random_bot)
  viewer = Viewer(engine)
  viewer.run()
