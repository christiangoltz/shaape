class Edge:
    def __init__(self, node1, node2):
        self.__start = node1
        self.__end = node2
        return

    def start(self):
        return self.__start

    def end(self):
        return self.__end

    def __ccw(self, a, b, c):
	    return (c[1] - a[1]) * (b[0] - a[0]) > (b[1] - a[1]) * (c[0] - a[0])
    def intersects(self, edge):
        if not isinstance(edge, Edge):
            raise TypeError
            return False
        return self.__ccw(self.start(), edge.start(), edge.end()) != self.__ccw(self.end(), edge.start(), edge.end()) and self.__ccw(self.start(), self.end(), edge.start()) != self.__ccw(self.start(), self.end(), edge.end())
