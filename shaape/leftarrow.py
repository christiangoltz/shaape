from node import Node
from arrow import Arrow
from polygon import Polygon

class LeftArrow(Arrow):
    def __init__(self, position = (0, 0)):
        Arrow.__init__(self, position, [Node(0.5, 0.2), Node(-0.5, 0), Node(0.5, -0.2)])

    def tip(self):
        return Node(*(self.position())) + self.nodes()[1]

    def direction(self):
        return Node(-1, 0)

    def connector(self):
        return Node(self.position()[0] + 0.5, self.position()[1])
