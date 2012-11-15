from drawable import Drawable
from scalable import Scalable
from operator import itemgetter
from graphalgorithms import *
import networkx as nx
import copy

class OpenGraph(Drawable, Scalable):
    def __init__(self, graph = nx.Graph()):
        Drawable.__init__(self)
        self.style().set_target_type('line')
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

    def __generate_paths(self):
        self.__paths = []
        nodes = [node for node in self.__graph.nodes() if self.__graph.degree(node) == 1]
        if nodes == []:
            nodes = [node for node in self.__graph.nodes() if node.fusable() == False]
        if nodes == []:
            nodes = self.__graph.nodes()
        if nodes == []:
            return
        min_node = sorted(nodes, key=itemgetter(0, 1))[0] 
        path_gen = nx.dfs_labeled_edges(self.__graph, min_node)
        path = []
        paths = []
        last_dir = ''
        for start, end, direction_dir in path_gen:
            direction = direction_dir['dir']
            if direction == 'forward':
                if len(path) == 0 or path[-1] <> start:
                    path.append(start)
                last_dir = direction
            elif direction == 'reverse':
                if last_dir <> 'reverse':
                    copy_path = copy.copy(path)
                    copy_path.append(end)
                    if len(path) > 2 and (self.__graph.has_edge(copy_path[0], copy_path[-1]) or self.__graph.has_edge(copy_path[-1], copy_path[0])):
                        copy_path.append(copy_path[0])
                    paths.append(copy_path)
                if len(path) > 0:
                    path.pop()
                last_dir = direction
        
        for path in paths:
            self.__paths.append(reduce_path(path))
        
        return        

    def paths(self):
        return self.__paths
