class Translatable(object):
    def __init__(self, position = (0, 0)):
        self.__position = position

    def set_position(self, position):
        self.__position = position

    def position(self):
        return self.__position

    def translate(self, diff):
        self.__position = (self.__position[0] + diff[0], self.__position[1] + diff[1])

    def scale(self, scale):
        self.__position = (self.__position[0] * scale[0], self.__position[1] * scale[1])
        return
