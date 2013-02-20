class Rotatable(object):
    def __init__(self, angle = 0):
        self.__angle = angle

    def set_angle(self, angle):
        self.__angle = angle

    def angle(self):
        return self.__angle
