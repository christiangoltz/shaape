class Edge:
    def __init__(self, node1, node2, top_of = None):
        self.__start = node1
        self.__end = node2
        self.__top_of = top_of
        return

    def start(self):
        return self.__start

    def end(self):
        return self.__end

    def top_of(self):
        return self.__top_of

    def __ccw(self, a, b, c):
	    return (c[1] - a[1]) * (b[0] - a[0]) > (b[1] - a[1]) * (c[0] - a[0])

    def intersects(self, edge):
        if not isinstance(edge, Edge):
            raise TypeError
        return self.__ccw(self.start(), edge.start(), edge.end()) != self.__ccw(self.end(), edge.start(), edge.end()) and self.__ccw(self.start(), self.end(), edge.start()) != self.__ccw(self.start(), self.end(), edge.end())
