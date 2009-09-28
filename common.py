import os

class Squares(object):
    EMPTY = '.'
    APPLE = '*'

class Sprites(object):
    PREFIX = 'images'
    def __getattribute__(self, name):
        try:
            return object.__getattribute__(self, name.upper())
        except AttributeError:
            from pygame.image import load
            filename = os.path.join(self.PREFIX, name.lower() + ".png")
            image = load(filename).convert_alpha()
            setattr(self, name, image)
            return image
Sprites = Sprites()

