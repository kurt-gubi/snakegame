DIRECTIONS = {
    'L': (-1, 0),
    'U': (0, -1),
    'R': (1, 0),
    'D': (1, 0),
}

def closest_apple_bot(board, position):
    x, y = position
    height = len(board)
    width = len(board[0])

    # todo contains the squares we need to explore
    todo = []
    # done contains the squares we've already explored
    done = set()

    # for each initial direction
    for direction in DIRECTIONS:
        dx, dy = DIRECTIONS[direction]
        # find the new position
        nx = (x + dx) % width
        ny = (y + dy) % height
        # add to todo and done
        todo.append((nx, ny, direction))
        done.add((nx, ny))

    while todo:
        # take the first item in todo
        x, y, direction = todo.pop(0)

        cell = board[y][x]

        # if we've reached an apple, we've found the shortest path
        # and direction is the right way to go
        if cell == '*':
            return direction

        # if we can't move into this cell, go to the next square to explore
        if cell != '.':
            continue

        # at this square, we can go any direction,
        # as long as it's not in our done set
        for dx, dy in DIRECTIONS.values():
            nx = (x + dx) % width
            ny = (y + dy) % height

            if (nx, ny) not in done:
                # we haven't visited this square before,
                # add it to our list of squares to visit
                # note that the third item here is the direction we initially
                # took to get to this square
                todo.append((nx, ny, direction))
                done.add((nx, ny))

    # if we get here, there are no apples on the board,
    # so we'll just move up.
    return 'U'

