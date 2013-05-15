import networkx as nx
import re
from edge import Edge
from node import Node

class Overlay:
    def __init__(self, array = [], edges = [], options = []):
        self.__overlay = array
        self.__substitutes = edges
        self.__options = options

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
                        if not re.match(str(self.__overlay[ov_y][ov_x]), str(data[orig_y][orig_x]), re.UNICODE):
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
                    for obj in self.__substitutes:
                        if isinstance(obj, Edge):
                            edge = obj
                            start = edge.start() + (data_x, data_y)
                            end = edge.end() + (data_x, data_y)
                            _above = None
                            _below = None
                            z_order = None
                            if edge.above() != None:
                                above_start = edge.above().start() + (data_x, data_y)
                                above_end = edge.above().end() + (data_x, data_y)
                                _above =  Edge(above_start, above_end)
                            if edge.below() != None:
                                below_start = edge.below().start() + (data_x, data_y)
                                below_end = edge.below().end() + (data_x, data_y)
                                _below = Edge(below_start, below_end)
                            graph.add_node(start, options = self.__options)
                            graph.add_node(end, options = self.__options)
                            graph.add_edge(start, end, above = _above, below = _below, z_order = edge.z_order())
                        elif isinstance(obj, Node):
                            start = obj + (data_x, data_y)
                            graph.add_node(start, options = self.__options)
        return graph
