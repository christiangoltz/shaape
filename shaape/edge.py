class Edge:
    def __init__(self, node1, node2, above = None, below = None, z_order = None):
        self.__start = node1
        self.__end = node2
        self.__above = above
        self.__below = below
        self.__z_order = z_order
        return

    def __getitem__(self, index):
        if index == 0:
            return self.__start
        elif index == 1:
            return self.__end
        else:
            raise IndexError

    def start(self):
        return self.__start

    def end(self):
        return self.__end

    def above(self):
        return self.__above

    def below(self):
        return self.__below

    def z_order(self):
        return self.__z_order

    def __ccw(self, a, b, c):
	    return (c[1] - a[1]) * (b[0] - a[0]) > (b[1] - a[1]) * (c[0] - a[0])

    def intersects(self, edge):
        return self.__ccw(self[0], edge[0], edge[1]) != self.__ccw(self[1], edge[0], edge[1]) and self.__ccw(self[0], self[1], edge[0]) != self.__ccw(self[0], self[1], edge[1])
