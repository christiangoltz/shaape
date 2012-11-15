from polygon import Polygon
from node import Node
from translatable import Translatable

class Arrow(Polygon, Translatable):
    def __init__(self, position = (0, 0)):
        Polygon.__init__(self, [Node(-0.5, 0.2), Node(0.5, 0), Node(-0.5, -0.2)])
        Translatable.__init__(self, position)
        self.style().set_color([0, 0, 0, 1])
        self.style().set_type('flat')
        self.set_frame(None)

    def scale(self, scale):
        Translatable.scale(self, scale)
        Polygon.scale(self, scale)
        return

