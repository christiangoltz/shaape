from drawable import Drawable
from scalable import Scalable
from operator import itemgetter
from named import Named
from graphalgorithms import *
import networkx as nx
import copy

class OpenGraph(Drawable, Scalable, Named):
    def __init__(self, graph = nx.Graph()):
        Drawable.__init__(self)
        Named.__init__(self)
        self.style().set_target_type('fill')
        self.add_name('_line_')
        self.__graph = graph
        self.__generate_paths()
        return

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
    
    def __generate_paths(self):
        self.__paths = []
        graph = copy.deepcopy(self.__graph)
        paths = []
        if not graph.nodes():
            return
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
