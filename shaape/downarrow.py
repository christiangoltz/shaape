from node import Node
from arrow import Arrow
from polygon import Polygon

class DownArrow(Arrow):
    def __init__(self, position = (0, 0)):
        Arrow.__init__(self, position, [Node(-0.4, 0.0), Node(0, 0.5), Node(0.4, 0.0)])

    def tip(self):
        return Node(*(self.position())) + self.nodes()[1]

    def direction(self):
        return Node(0, 1)

    def connector(self):
        return Node(self.position()[0], self.position()[1])
