from polygon import Polygon
from named import Named
from node import Node
from translatable import Translatable

class Arrow(Polygon, Translatable, Named):
    def __init__(self, position = (0, 0)):
        Polygon.__init__(self, [Node(-0.5, 0.2), Node(0.5, 0), Node(-0.5, -0.2)])
        Translatable.__init__(self, position)
        Named.__init__(self)
        self.add_name('_arrow_')

    def scale(self, scale):
        Translatable.scale(self, scale)
        Polygon.scale(self, scale)
        return

