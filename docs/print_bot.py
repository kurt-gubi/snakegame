def print_bot(board, position):
    print position
    print board

if __name__ == '__main__':
    from snakegame.engines.pyglet import PygletEngine
    engine = PygletEngine(3, 4, 3)
    engine.add_bot(print_bot)
    engine.run()
