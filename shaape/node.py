import math

class Node(object):
    def __init__(self, x, y, style = 'miter', fusable = True):
        self.__position = (x, y)
        self.__style = style
        self.__fusable = fusable
        return

    def position(self):
        return self.__position

    def fusable(self):
        return self.__fusable

    def set_fusable(self, fusable):
        self.__fusable = fusable
        return

    def style(self):
        return self.__style
    
    def __getitem__(self, index):
        if index < 2:
    		return self.__position[index]

    def __add__(self, other):
		return Node(self.position()[0] + other[0], self.position()[1] + other[1], self.style(), self.fusable())

    def __sub__(self, other):
		return Node(self.position()[0] - other[0], self.position()[1] - other[1], self.style(), self.fusable())

    def __div__(self, other):
        if isinstance(other, float):
            return Node(self.position()[0] / other, self.position()[1] / other, self.style(), self.fusable())

    def __mul__(self, other):
        if isinstance(other, float):
    		return Node(self.position()[0] * other, self.position()[1] * other, self.style(), self.fusable())
        else:
    		return Node(self.position()[0] * other[0], self.position()[1] * other[1], self.style(), self.fusable())

    def __key__(self):
        return self.__position

    def __hash__(self):
        return hash(self.__key__())

    def __cmp__(self, other):
        assert isinstance(other, Node)
        return cmp((self.position()[0], self.position()[1]), (other.position()[0], other.position()[1]))

    def __repr__(self):
        return "(" + str(self.position()) + "," + self.style() + "," + str(self.fusable()) + ")"

    def __iter__(self):
        return (n for n in self.position())

    def length(self):
        return math.sqrt(sum(self.__position[i]* self.__position[i] for i in range(len(self.__position))))

    def normalize(self):
        self.__position = (self / self.length()).position()
        return
