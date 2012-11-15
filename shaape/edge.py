class Edge:
    def __init__(self, node1, node2, action = 'none'):
        self.__start = node1
        self.__end = node2
        self.__action = action
        return

    def start(self):
        return self.__start

    def end(self):
        return self.__end

    def action(self):
        return self.__action

