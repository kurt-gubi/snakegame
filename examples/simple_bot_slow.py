from snakegame.engine import Engine
from snakegame.viewers.pyglet import Viewer

def bot(board, position):
  return 'U'

if __name__ == '__main__':
  engine = Engine(10, 10, 25)
  engine.add_bot(bot)
  viewer = Viewer(engine, speed=0.5)
  viewer.run()
