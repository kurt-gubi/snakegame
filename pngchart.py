from pngcanvas import PNGCanvas

try:
    from itertools import izip as zip
except ImportError:
    pass

class SimpleLineChart(object):
    def __init__(self, width, height, colours=None, legend=None):
        self.canvas = PNGCanvas(width, height)

        self.width = width
        self.height = height

        self.colours = colours
        self.legend = legend

        self.series = []

    def add_data(self, series):
        self.series.append(series)

    def render(self):
        max_width = max(map(len, self.series))
        max_height = max(map(max, self.series))
        x_scale = float(self.width) / max_width
        y_scale = float(self.height) / max_height

        data = zip(self.series, self.colours or [], self.legend or [])
        for series, colour, legend in data:
            colour = int(colour, 16)
            self.canvas.color = (
                colour>>16 & 0xff,
                colour>>8 & 0xff,
                colour & 0xff,
                0xff,
            )
            last = None
            for x, y in enumerate(series):
                if y is not None:
                    y = self.height - y * y_scale
                    if last is not None:
                        x *= x_scale
                        self.canvas.line(x - x_scale, last, x, y)
                last = y

    def download(self, filename):
        self.render()

        f = open(filename, 'wb')
        f.write(self.canvas.dump())
        f.close()

