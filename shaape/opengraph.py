from drawable import Drawable
from edge import Edge
from scalable import Scalable
from operator import itemgetter
from named import Named
from graphalgorithms import *
import networkx as nx
import copy

class OpenGraph(Drawable, Scalable, Named):
    def __init__(self, graph = nx.Graph(), options = []):
        Drawable.__init__(self, options)
        Named.__init__(self)
        self.style().set_target_type('fill')
        self.add_name('_line_')
        self.__graph = graph
        self.__generate_paths()
        return

    def reduce_nodes(self):
        node_reduced = True
        while node_reduced == True:
            node_reduced = False
            for node in self.__graph.nodes():
                if self.__graph.degree(node) == 2:
                    neighbors = self.__graph.neighbors(node)
                    if has_same_direction(neighbors[0] - node, node - neighbors[1]):
                        self.__graph.add_edge(neighbors[0], neighbors[1])
                        self.__graph.remove_node(node)
                        node_reduced = True


    def graph(self):
        return self.__graph

    def min(self):
        return (min([n[0] for n in self.__graph.nodes()]), min([n[1] for n in self.__graph.nodes()]))

    def max(self):
        return (max([n[0] for n in self.__graph.nodes()]), max([n[1] for n in self.__graph.nodes()]))

    def scale(self, scale):
        old_nodes = self.__graph.nodes()
        new_nodes = {}
        for node in old_nodes:
            new_nodes[node] = node * scale
        self.__graph = nx.relabel_nodes(self.__graph, new_nodes)
        for path in self.__paths:
            for i in range(0, len(path)):
                path[i] = path[i] * scale
        return

    def edges(self):
        return self.__graph.edges()

    def nodes(self):
        return self.__graph.nodes()

    def has_edge(self, start, end):
        return self.__graph.has_edge(start, end)

    def has_node(self, node):
        return self.__graph.has_node(node)

    def intersects(self, obj):
        for edge in self.edges():
            if line_segments_intersect(edge, obj):
                return True
        return False
    
    def __generate_paths(self):
        self.__paths = []
        graph = copy.deepcopy(self.__graph)
        paths = []
        if not graph.nodes():
            return
        start_nodes = [n for n in graph.nodes() if (n.style() != 'curve' or (nx.degree(graph, n) == 1)) ]
        start_nodes = sorted(start_nodes, key = lambda n: nx.degree(graph, n))
        if start_nodes:
            path = [start_nodes[0]]
        else:
            path = [graph.nodes()[0]]

        while path:
            neighbors = nx.neighbors(graph, path[-1])
            if neighbors:
                node = neighbors[0]
                graph.remove_edge(path[-1], node)
                path.append(node)
            else:
                paths.append(copy.copy(path))
                while path and not graph.neighbors(path[-1]):
                    path.pop()
                
        for path in paths:
            self.__paths.append(reduce_path(path))
        
        return        

    def paths(self):
        return self.__paths

    def add_path(self, path):
        self.__paths.append(path)
