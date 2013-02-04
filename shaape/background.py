from drawable import Drawable
from scalable import Scalable

class Background(Drawable, Scalable):
    def __init__(self, size = (0, 0)):
        Drawable.__init__(self)
        Scalable.__init__(self)
        self.__size = size
        return
    
    def size(self):
        return self.__size

    def scale(self, scale):
        self.__size = (self.__size[0] * scale[0], self.__size[1] * scale[1])

    def min(self):
        return (0, 0)

    def max(self):
        return self.size()
