def up_bot(board, position):
    return 'U'

if __name__ == '__main__':
    from snakegame.engines.pyglet import PygletEngine
    engine = PygletEngine(10, 10, 20)
    engine.add_bot(up_bot)
    engine.run()
