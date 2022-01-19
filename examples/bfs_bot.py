import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..', 'snakegame'))

from snakegame.engine import Engine
from snakegame.viewers.pyglet import Viewer
import random

# return a list of neighbouring positions on the board
def neighbouring_positions(position, board_width, board_height):
  x,y = position
  return [
    ( (x-1) % board_width,  (y-1) % board_height  ), # above left
    ( x,                    (y-1) % board_height  ), # above middle
    ( (x+1) % board_width,  (y-1) % board_height  ), # above right
    
    ( (x-1) % board_width,  y                     ), # left
    ( (x+1) % board_width,  y                     ), # right
    
    ( (x-1) % board_width,  (y+1) % board_height  ), # below left
    ( x,                    (y+1) % board_height  ), # below middle
    ( (x+1) % board_width,  (y+1) % board_height  )  # below right
  ]

# return the position of the nearest apple, using breadth-first-search
def bfs_search(board, start_position):
  height = len(board)
  width = len(board[0])
  checked = []

  # get the initial neighbouring positions
  to_check = neighbouring_positions(start_position, width, height)
  
  # continue looping while we still have positions left in "to_check"
  while to_check:
    # get the first position, simultaneously removing it from the list
    position = to_check.pop()
    x,y = position
    # 1. If we’ve already looked at this square: move on to the next square in our list.
    if position in checked:
      continue
    else:
      checked.append(position)
    # 2. If the square we’re looking at is food: we’re done!
    if board[y][x] == '*':
      return position
    # 3. If the square we’re looking at is empty: add the squares we can read from here to the end of our “to check” list.
    if board[y][x] == '.':
      nearby = neighbouring_positions(position, height, width)
      to_check.extend(nearby)
    # 4. Otherwise: move on to the next square in our list.
    continue

def bfs_bot(board, position):
  height = len(board)
  width = len(board[0])
  x,y = position

  weights = {
    'U': 100,
    'D': 100,
    'L': 100,
    'R': 100
  }
  
  apple_position = bfs_search(board, position)
  if apple_position:
    apple_x, apple_y = apple_position
    
    # deter direction away from apple
    if apple_x < x:
      weights['R'] = 1
    elif apple_x > x:
      weights['L'] = 1
    if apple_y < y:
      weights['D'] = 1
    elif apple_y > y:
      weights['U'] = 1
  
  # avoid direction into a snake
  if board[ (y-1) % height][x].isalpha():
    weights['U'] = 0
  if board[ (y+1) % height][x].isalpha():
    weights['D'] = 0
  if board[y][(x-1) % width].isalpha():
    weights['L'] = 0
  if board[y][(x+1) % width].isalpha():
    weights['R'] = 0
    
  choices = ['U', 'D', 'L', 'R']
  weights = [weights['U'], weights['D'], weights['L'], weights['R']]
  return random.choices(choices, weights=weights, k=1)[0]

if __name__ == '__main__':
  engine = Engine(10, 10, 25)
  engine.add_bot(bfs_bot)
  viewer = Viewer(engine, speed=0.2)
  viewer.run()
