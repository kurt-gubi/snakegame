from snakegame.engine import Engine
from snakegame.viewers import BUILTIN_VIEWERS

def first(d):
    for item in d:
        return item

def rsplit_get(s, sep, default):
    if sep not in s:
        return (s, default)
    return s.rsplit(sep, 1)

def import_thing(name, default_obj):
    pkg, obj = rsplit_get(name, ':', default_obj)
    mod = __import__(pkg, fromlist=[obj])
    return getattr(mod, obj)

def main(argv=None):
    import argparse

    parser = argparse.ArgumentParser(conflict_handler='resolve')
    parser.add_argument(
        '-v', '--viewer',
        default=first(BUILTIN_VIEWERS),
    )
    parser.add_argument(
        '-w', '--width',
        default=30,
    )
    parser.add_argument(
        '-h', '--height',
        default=20,
    )
    parser.add_argument(
        '-a', '--apples',
        default=40,
    )
    parser.add_argument('bot', nargs='+')
    args = parser.parse_args(argv)

    viewer_name = BUILTIN_VIEWERS.get(args.viewer, args.viewer)
    viewer_class = import_thing(viewer_name, 'Viewer')

    game = Engine(args.height, args.width, args.apples)

    for name in args.bot:
        bot = import_thing(name, 'bot')
        game.add_bot(bot)

    viewer = viewer_class(game)
    viewer.run()

