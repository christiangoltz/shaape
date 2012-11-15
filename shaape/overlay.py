import networkx as nx
from edge import Edge

class Overlay:
    def __init__(self, array = [], edges = []):
        self.__overlay = array
        self.__substitutes = edges

    def substitutes(self, data):
        graph = nx.Graph()
        for data_y in range(0, len(data)):
            for data_x in range(0, len(data[data_y])):
                orig_x = data_x
                orig_y = data_y
                ov_y = 0
                ov_x = 0
                matched = True
                while True == matched and ov_y < len(self.__overlay):
                    if None != self.__overlay[ov_y][ov_x]:
                        if data[orig_y][orig_x] != self.__overlay[ov_y][ov_x]:
                            matched = False
                    if ov_x < len(self.__overlay[ov_y]) - 1:
                        ov_x = ov_x + 1
                        orig_x = orig_x + 1
                        if orig_x >= len(data[orig_y]):
                            matched = False
                    else:
                        ov_x = 0
                        orig_x = data_x
                        ov_y = ov_y + 1
                        orig_y = orig_y + 1
                        if orig_y >= len(data) and ov_y < len(self.__overlay):
                            matched = False
                if True == matched:
                    for edge in self.__substitutes:
                        start = edge.start() + (data_x, data_y)
                        end = edge.end() + (data_x, data_y)
                        graph.add_edge(start, end)
        return graph
