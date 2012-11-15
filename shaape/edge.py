class Edge:
    def __init__(self, node1, node2):
        self.__start = node1
        self.__end = node2
        return

    def start(self):
        return self.__start

    def end(self):
        return self.__end
