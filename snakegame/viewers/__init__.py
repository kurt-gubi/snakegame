from snakegame.utils import MaybeOrderedDict

BUILTIN_VIEWERS = MaybeOrderedDict()

def add_viewer(name):
    BUILTIN_VIEWERS[name] = 'snakegame.viewers.%s:Viewer' % name

add_viewer('pyglet')
add_viewer('pygame')
add_viewer('curses')
