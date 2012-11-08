from arrow import Arrow
from rotatable import Rotatable

class UpArrow(Arrow, Rotatable):
    def __init__(self, position):
        Arrow.__init__(self, (position[0], position[1] - 0.3))
        Rotatable.__init__(self, 270)
