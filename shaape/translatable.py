from vector import Vector


class Translatable(object):
    def __init__(self, position = (0, 0)):
        self.__position = Vector(position[0], position[1])

    def set_position(self, position):
        self.__position = Vector(position[0], position[1])

    def position(self):
        return self.__position

    def translate(self, diff):
        self.__position += diff

    def scale(self, scale):
        self.__position *= scale
        return
