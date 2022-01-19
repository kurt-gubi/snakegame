import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..', 'snakegame'))

from snakegame.engine import Engine, SnakeColour
from snakegame.viewers.pyglet import Viewer

import bfs_bot as bfs_bot
import simple_bot as simple_bot
import multiple_bot as multiple_bot

if __name__ == '__main__':
  engine = Engine(20, 20, 25)
  
  engine.add_bot(bfs_bot.bfs_bot, colour=SnakeColour.BLUE.value)
  engine.add_bot(simple_bot.bot, colour=SnakeColour.GREEN.value)
  engine.add_bot(multiple_bot.left_bot, colour=SnakeColour.YELLOW.value)
  engine.add_bot(multiple_bot.right_bot, colour=SnakeColour.PURPLE.value)
  engine.add_bot(multiple_bot.random_bot, colour=SnakeColour.RED.value)

  viewer = Viewer(engine)
  viewer.run()
