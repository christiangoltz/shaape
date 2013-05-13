import math


_number_types = (int, long, float)


class Vector(object):
    def __init__(self, x=0.0, y=0.0):
        self.x, self.y = float(x), float(y)

    def __eq__(self, other):
        return self.x == other[0] and self.y == other[1]

    def __add__(self, other):
        return Vector(self.x + other[0], self.y + other[1])

    def __iadd__(self, other):
        self.x += other[0]
        self.y += other[1]
        return self

    def __sub__(self, other):
        return Vector(self.x - other[0], self.y - other[1])

    def __isub__(self, other):
        self.x -= other[0]
        self.y -= other[1]
        return self

    def __mul__(self, other):
        if type(other) in _number_types:
            return Vector(self.x * other, self.y * other)

        return Vector(self.x * other[0], self.y * other[1])

    def __rmul__(self, other):
        return self.__mul__(other)

    def __imul__(self, other):
        if type(other) in _number_types:
            self.x *= other
            self.y *= other
        else:
            self.x *= other[0]
            self.y *= other[1]
        return self

    def __idiv__(self, scalar):
        self.x /= scalar
        self.y /= scalar
        return self

    def __getitem__(self, key):
        if key == 0:
            return self.x
        if key == 1:
            return self.y
        raise IndexError("{0} is neither 0 nor 1".format(key))

    def length(self):
        return math.sqrt(self.x**2 + self.y**2)


def dot(vec_a, vec_b):
    return vec_a.x * vec_b.x + vec_a.y * vec_b.y
