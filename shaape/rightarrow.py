from arrow import Arrow
from rotatable import Rotatable

class RightArrow(Arrow, Rotatable):
    def __init__(self, position = (0, 0)):
        Arrow.__init__(self, position)
        Rotatable.__init__(self, 0)
