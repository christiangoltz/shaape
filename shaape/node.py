import math

class Node(object):
    def __init__(self, x, y, style = 'miter', fusable = True):
        self.m_position = (x, y)
        if style in ['miter', 'curve']:
            self.__style = style
        else:
            raise ValueError
        self.__fusable = fusable
        return

    def set_position(self, x, y):
        self.m_position = (x, y)

    def position(self):
        return self.m_position

    def fusable(self):
        return self.__fusable

    def set_fusable(self, fusable):
        self.__fusable = fusable
        return

    def style(self):
        return self.__style
    
    def __getitem__(self, index):
        if index == 0 or index == 1:
    		return self.m_position[index]
        raise IndexError

    def __add__(self, other):
		return Node(self.m_position[0] + other[0], self.m_position[1] + other[1], self.style(), self.fusable())

    def __sub__(self, other):
		return Node(self.m_position[0] - other[0], self.m_position[1] - other[1], self.style(), self.fusable())

    def __div__(self, other):
        if isinstance(other, (float, int)):
            return Node(self.m_position[0] / other, self.m_position[1] / other, self.style(), self.fusable())
        else:
            raise NotImplementedError

    def __mul__(self, other):
        if isinstance(other, (float, int)):
    		return Node(self.m_position[0] * other, self.m_position[1] * other, self.style(), self.fusable())
        else:
    		return Node(self.m_position[0] * other[0], self.m_position[1] * other[1], self.style(), self.fusable())

    def __key__(self):
        return self.m_position

    def __hash__(self):
        return hash(self.m_position)

    def __cmp__(self, other):
        return cmp(self.m_position, other.m_position)

    def __repr__(self):
        return "(" + str(self.m_position) + "," + self.style() + "," + str(self.fusable()) + ")"

    def __iter__(self):
        return (n for n in self.m_position)

    def length(self):
        return math.sqrt(sum(self.m_position[i]* self.m_position[i] for i in range(len(self.m_position))))

    def normalize(self):
        length = self.length()
        if length == 0:
            raise ArithmeticError
        self.m_position = (self / length).m_position
        return
