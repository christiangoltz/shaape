import math

class ShaapeNode(object):
    def __init__(self, x, y, style = 'miter'):
        self.__position = (x, y)
        self.__style = style
        return

    def position(self):
        return self.__position

    def style(self):
        return self.__style
    
    def __getitem__(self, index):
        if index < 2:
    		return self.__position[index]

    def __add__(self, other):
		return ShaapeNode(self.position()[0] + other[0], self.position()[1] + other[1], self.style())

    def __sub__(self, other):
		return ShaapeNode(self.position()[0] - other[0], self.position()[1] - other[1], self.style())

    def __div__(self, other):
        if isinstance(other, float):
            return ShaapeNode(self.position()[0] / other, self.position()[1] / other, self.style())

    def __mul__(self, other):
        if isinstance(other, float):
    		return ShaapeNode(self.position()[0] * other, self.position()[1] * other, self.style())
        else:
    		return ShaapeNode(self.position()[0] * other[0], self.position()[1] * other[1], self.style())

    def __key__(self):
        return self.__position

    def __hash__(self):
        return hash(self.__key__())

    def __cmp__(self, other):
        assert isinstance(other, ShaapeNode)
        return cmp((self.position()[0], self.position()[1]), (other.position()[0], other.position()[1]))

    def __repr__(self):
        return "(" + str(self.position()) + "," + self.style() + ")"

    def __iter__(self):
        return (n for n in self.position())

    def length(self):
        return math.sqrt(sum(self.__position[i]* self.__position[i] for i in range(len(self.__position))))

    def normalize(self):
        self.__position = (self / self.length()).position()
        return
