from __future__ import absolute_import

import pyglet.resource
pyglet.resource.path.append('@snakegame')
pyglet.resource.reindex()

from pyglet import gl

from snakegame import common
from snakegame.utils import scale_aspect

class Viewer(pyglet.window.Window):
    EDGE_COLOR = (255, 255, 255, 255)
    EDGE_WIDTH = 2

    def __init__(self, engine, caption='SnakeGame Window', resizable=True, **kwargs):
        super(Viewer, self).__init__(
            caption=caption,
            resizable=resizable,
            **kwargs
        )

        self.engine = engine
        self.engine_iter = iter(engine)

        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

        pyglet.clock.schedule_interval(lambda t: self.update_snakes(), 1/30.0)

        self.board = None
        self.columns = None
        self.rows = None

    def update_snakes(self, *args):
        self.board = next(self.engine_iter, None)
        if self.board is None:
            pyglet.app.exit()
            return

        columns, rows = common.get_size(self.board)
        if columns != self.columns or rows != self.rows:
            self.columns = columns
            self.rows = rows
            self.on_resize(self.width, self.height)

    def on_resize(self, width, height):
        super(Viewer, self).on_resize(width, height)

        if self.board is None:
            return

        # make board surface
        self.board_width, self.board_height = scale_aspect(
            (self.columns, self.rows), (self.width, self.height)
        )

        # load sprites
        xscale = float(self.board_width) / self.columns
        yscale = float(self.board_height) / self.rows

        self.apple = pyglet.resource.image('images/apple.png')
        self.apple.size = scale_aspect(
            (self.apple.width, self.apple.height),
            (xscale, yscale)
        )
        self.eyes = pyglet.resource.image('images/eyes.png')
        self.eyes.size = scale_aspect(
            (self.eyes.width, self.eyes.height),
            (xscale, yscale)
        )

    def on_draw(self):
        self.clear()

        if self.board is None:
            return

        xscale = float(self.board_width) / self.columns
        yscale = float(self.board_height) / self.rows

        # Draw grid.
        for y, row in enumerate(self.board):
            for x, cell in enumerate(row):
                left = int(x * xscale)
                top = self.height - int(y * yscale)
                right = int((x + 1) * xscale)
                bottom = self.height - int((y + 1) * yscale)
                r = (left, top, right, top, right, bottom, left, bottom)

                # Draw a square.
                gl.glLineWidth(self.EDGE_WIDTH)
                pyglet.graphics.draw(4, gl.GL_LINE_LOOP,
                                     ('v2f', r),
                                     ('c4B', self.EDGE_COLOR * 4))

                # Draw the things on the square.
                if cell == common.APPLE:
                    w, h = self.apple.size
                    self.apple.blit(left + (xscale - w) / 2.0, top - h, width=w, height=h)

                elif common.is_snake(cell):
                    bot = self.engine.bots[cell.lower()]
                    colour = bot[1] + (255,)
                    gl.glPolygonMode(gl.GL_FRONT, gl.GL_FILL)
                    pyglet.graphics.draw(4, gl.GL_POLYGON,
                                         ('v2f', r),
                                         ('c4B', colour * 4),
                    )

                    if common.is_snake_head(cell):
                        w, h = self.eyes.size
                        self.eyes.blit(left, top - h, width=w, height=h)

    def run(self):
        pyglet.app.run()

