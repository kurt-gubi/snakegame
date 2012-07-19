try:
    from collections import OrderedDict as MaybeOrderedDict
except ImportError:
    MaybeOrderedDict = dict

from snakegame.engines.base import Engine

BUILTIN_ENGINES = MaybeOrderedDict()

try:
    from snakegame.engines.pyglet import PygletEngine
except ImportError:
    pass
else:
    BUILTIN_ENGINES['pyglet'] = PygletEngine

try:
    from snakegame.engines.pygame import PygameEngine
except ImportError:
    pass
else:
    BUILTIN_ENGINES['pygame'] = PygameEngine

try:
    from snakegame.engines.curses import CursesEngine
except ImportError:
    pass
else:
    BUILTIN_ENGINES['curses'] = CursesEngine
