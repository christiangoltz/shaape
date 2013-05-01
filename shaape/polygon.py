from drawable import Drawable
from edge import Edge
from named import Named
from scalable import Scalable
import networkx as nx
from opengraph import OpenGraph
from graphalgorithms import *

class Polygon(Drawable, Named, Scalable):
    def __init__(self, node_list, options = []):
        Drawable.__init__(self, options)
        Named.__init__(self)
        self.__node_list = node_list 
        cycle_graph = nx.Graph()
        if node_list :
            for n in range(1, len(node_list)):
                cycle_graph.add_edge(node_list[n - 1], node_list[n])
        self.style().set_target_type('fill')
        self.__frame = OpenGraph(cycle_graph, options)
        self.__frame.style().set_target_type('frame')
        return

    def reduce_nodes(self):
        self.__node_list = reduce_path(self.__node_list)

    def contains(self, obj):
        if type(obj) == Polygon:
            # check if all nodes are inside
            for p in obj.nodes():
                if not self.contains(p):
                    return False

            # check for edge intersections
            outer_edges = [Edge(self.nodes()[i], self.nodes()[i + 1]) for i in range(0, len(self.nodes()) - 1)]
            inner_edges = [Edge(obj.nodes()[i], obj.nodes()[i + 1]) for i in range(0, len(obj.nodes()) - 1)]
            for inner_edge in inner_edges:
                for outer_edge in outer_edges:
                    if inner_edge.intersects(outer_edge):
                        return False
            return True
        else:
            n = len(self.__node_list)
            inside = False
            x,y = obj
            p1x,p1y = self.__node_list[0]
            for i in range(n+1):
                p2x,p2y = self.__node_list[i % n]
                if y > min(p1y,p2y):
                    if y <= max(p1y,p2y):
                        if x <= max(p1x,p2x):
                            xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                            if p1x == p2x or x <= xinters:
                                inside = not inside
                p1x,p1y = p2x,p2y
            return inside

    def nodes(self):
        return self.__node_list

    def edges(self):
        return [(self.__node_list[i], self.__node_list[i + 1]) for i in range(0, len(self.__node_list) - 1)] 

    def has_edge(self, start, end):
        i = 0
        while True:
            try:
                i = self.__node_list.index(start, i + 1)
                if self.__node_list[i - 1] == end or (i < len(self.__node_list) - 1 and self.__node_list[i + 1] == end):
                    return True
            except ValueError:
                return False

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
