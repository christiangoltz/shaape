from drawable import Drawable
from translatable import Translatable
from scalable import Scalable

class Text(Drawable, Translatable, Scalable):
    def __init__(self, text, position = (0, 0)):
        Drawable.__init__(self)
        Translatable.__init__(self, position)
        self.__text = text
        self.__font_size = 1
        return

    def text(self):
        return self.__text

    def font_size(self):
        return self.__font_size

    def scale(self, scale):
        Translatable.scale(self, scale)
        self.__font_size = self.__font_size * scale[0]
        return
    
    def min(self):
        return self.position()

    def max(self):
        return self.position()
