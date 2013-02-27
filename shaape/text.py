from drawable import Drawable
from translatable import Translatable
from scalable import Scalable
from named import Named
import numpy as np

class Text(Drawable, Translatable, Scalable, Named):
    def __init__(self, text = "", position = (0, 0)):
        Drawable.__init__(self)
        Translatable.__init__(self, position)
        Named.__init__(self)
        self.__text = text
        self.__font_size = 1
        self.__scaled_direction = np.array([1, 0])
        return

    def text(self):
        return self.__text

    def font_size(self):
        return self.__font_size

    def scale(self, scale):
        Translatable.scale(self, scale)
        self.__font_size = self.__font_size * scale[0]
        self.__scaled_direction = (self.__scaled_direction[0] * scale[0], self.__scaled_direction[1] * scale[1])
        return
    
    def min(self):
        return self.position()

    def max(self):
        return tuple(np.array(self.position()) + np.array(self.__scaled_direction) * len(self.__text))

    def anchor(self):
        return np.array(self.position()) + np.array([0.5, 0.5])

    def letter_position(self, index):
        if index < len(self.__text):
            return self.anchor() + (self.__scaled_direction * index)
