from drawable import Drawable
from named import Named
from scalable import Scalable
import networkx as nx
from opengraph import OpenGraph
from graphalgorithms import *

class Polygon(Drawable, Named, Scalable):
    def __init__(self, node_list):
        Drawable.__init__(self)
        Named.__init__(self)
        self.__node_list = node_list
        cycle_graph = nx.Graph()
        if node_list == []:
            raise ValueError
        cycle_graph.add_cycle(node_list)
        self.__frame = OpenGraph(cycle_graph)
        self.style().set_target_type('fill')
        self.__frame.style().set_target_type('frame')
        self.__node_list = reduce_path(self.__node_list)
        return

    def contains(self, point):
        # point inside polygon
        n = len(self.__node_list)
        inside = False
        x,y = point
        p1x,p1y = self.__node_list[0]
        for i in range(n+1):
            p2x,p2y = self.__node_list[i % n]
            if y > min(p1y,p2y):
                if y <= max(p1y,p2y):
                    if x <= max(p1x,p2x):
                        if p1y != p2y:
                            xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x,p1y = p2x,p2y
        return inside

    def nodes(self):
        return self.__node_list

    def max(self):
        return (max([n[0] for n in self.__node_list]), max([n[1] for n in self.__node_list]))

    def min(self):
        return (min([n[0] for n in self.__node_list]), min([n[1] for n in self.__node_list]))

    def scale(self, scale):
        for n in range(0, len(self.__node_list)):
            node = self.__node_list[n]
            self.__node_list[n] = node * scale
        self.__frame.scale(scale)

    def frame(self):
        return self.__frame
