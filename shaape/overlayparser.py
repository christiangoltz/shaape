import networkx as nx
import operator
import math
from drawable import *
from parser import *
from node import *

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

class Overlay:
    def __init__(self, array, edges):
        self.__overlay = array
        self.__substitutes = edges
        return

    def substitutes(self, data):
        graph = nx.Graph()
        merge_edges = []
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
                        if edge.action() == 'merge':
                            merge_edges.append(Edge(start[0], start[1], end[0], end[1]))
                        else:
                            graph.add_edge(start, end)

        return graph, merge_edges

class OverlayParser(Parser):
    def __init__(self):
        super(OverlayParser, self).__init__()
        self.__sub_overlays = []
        self.__sub_overlays.append(Overlay([['-']], [Edge(Node(0, 0.5), Node(1, 0.5))]))
        self.__sub_overlays.append(Overlay([['|']], [Edge(Node(0.5, 0), Node(0.5, 1))]))
        self.__sub_overlays.append(Overlay([['/']], [Edge(Node(0, 1), Node(1, 0))]))
        self.__sub_overlays.append(Overlay([['\\']], [Edge(Node(1, 1), Node(0, 0))]))
        self.__sub_overlays.append(Overlay([['-','|']], [Edge(Node(1, 0.5), Node(1.5, 0.5))]))
        self.__sub_overlays.append(Overlay([['+','-']], [Edge(Node(0.5, 0.5, fusable = False), Node(1, 0.5))]))
        self.__sub_overlays.append(Overlay([['-','+']], [Edge(Node(1, 0.5), Node(1.5, 0.5, fusable = False))]))
        self.__sub_overlays.append(Overlay([['+'],['|']], [Edge(Node(0.5, 0.5, fusable = False), Node(0.5, 1))]))
        self.__sub_overlays.append(Overlay([[None, '/'],['+', None]], [Edge(Node(1, 1), Node(0.5, 1.5, fusable = False))]))
        self.__sub_overlays.append(Overlay([['\\', None],[None, '+']], [Edge(Node(1, 1), Node(1.5, 1.5, fusable = False))]))
        self.__sub_overlays.append(Overlay([['+', None],[None, '\\']], [Edge(Node(0.5, 0.5, fusable = False), Node(1, 1))]))
        self.__sub_overlays.append(Overlay([[None, '+'],['/', None]], [Edge(Node(1.5, 0.5, fusable = False), Node(1, 1))]))
        self.__sub_overlays.append(Overlay([['|'],['+']], [Edge(Node(0.5, 1), Node(0.5, 1.5, fusable = False))]))
        self.__sub_overlays.append(Overlay([['|'],['*']], [Edge(Node(0.5, 1), Node(0.5, 1.5, 'curve'))]))
        self.__sub_overlays.append(Overlay([['*'],['|']], [Edge(Node(0.5, 0.5, 'curve'), Node(0.5, 1))]))
        self.__sub_overlays.append(Overlay([['*','-']], [Edge(Node(0.5, 0.5, 'curve'), Node(1, 0.5))]))
        self.__sub_overlays.append(Overlay([['-','*']], [Edge(Node(1, 0.5), Node(1.5, 0.5, 'curve'))]))
        self.__sub_overlays.append(Overlay([['+','+']], [Edge(Node(0.5, 0.5, fusable = False), Node(1.5, 0.5, fusable = False))]))
        self.__sub_overlays.append(Overlay([['+'],['+']], [Edge(Node(0.5, 0.5, fusable = False), Node(0.5, 1.5, fusable = False))]))

        # connect arrows and straight lines
        # self.__sub_overlays.append(Overlay([['-', '>']], [Edge(1, 0.5, 1.5, 0.5)]))
        # self.__sub_overlays.append(Overlay([['<', '-']], [Edge(0.5, 0.5, 1, 0.5)]))
        # self.__sub_overlays.append(Overlay([['|'], ['v']], [Edge(0.5, 1, 0.5, 1.5)]))
        # self.__sub_overlays.append(Overlay([['^'], ['|']], [Edge(0.5, 0.5, 0.5, 1)]))
        self.__sub_overlays.append(Overlay([['|'], ['^']], [Edge(Node(0.5, 1), Node(0.5, 2))]))
        self.__sub_overlays.append(Overlay([['v'], ['|']], [Edge(Node(0.5, 0), Node(0.5, 1))]))
        self.__sub_overlays.append(Overlay([['-', '<']], [Edge(Node(1, 0.5), Node(2, 0.5))]))
        self.__sub_overlays.append(Overlay([['>', '-']], [Edge(Node(0, 0.5), Node(1, 0.5))]))

        self.__sub_overlays.append(Overlay([['*','*']], [Edge(Node(0.5, 0.5, 'curve'), Node(1.5, 0.5, 'curve'))]))
        self.__sub_overlays.append(Overlay([['*'],['*']], [Edge(Node(0.5, 0.5, 'curve'), Node(0.5, 1.5,'curve'))]))
        self.__sub_overlays.append(Overlay([[None, '*'],['*', None]], [Edge(Node(1.5, 0.5, 'curve'), Node(0.5, 1.5,'curve'))]))
        self.__sub_overlays.append(Overlay([['*', None],[None, '*']], [Edge(Node(0.5, 0.5, 'curve'), Node(1.5, 1.5,'curve'))]))

        # connect arrows and +
        # self.__sub_overlays.append(Overlay([['+'], ['^']], [Edge(0.5, 0.5, 0.5, 1.5)]))
        # self.__sub_overlays.append(Overlay([['v'], ['+']], [Edge(0.5, 0.5, 0.5, 1.5)]))
        # self.__sub_overlays.append(Overlay([['+', '<']], [Edge(0.5, 0.5, 1.5, 0.5)]))
        # self.__sub_overlays.append(Overlay([['>', '+']], [Edge(0.5, 0.5, 1.5, 0.5)]))
        return

    def cycle_len(self, cycle):
        length = 0
        for i in range(0, len(cycle) - 1):
            length = length + (cycle[i + 1] - cycle[i]).length()
        return length

    def run(self, raw_data, drawable_objects):
        graphs = []
        merge_edges = []
        for overlay in self.__sub_overlays:
            g, m = overlay.substitutes(raw_data)
            merge_edges = merge_edges + m
            graphs.append(g)

        graph = graphs.pop(0)
        for h in graphs:
            graph = nx.compose(graph, h)
            for a in h:
                for b in graph:
                    if a == b:
                        b.set_fusable(a.fusable() and b.fusable())

        # mapping = dict(zip(graph , graph)) 
        # graph=nx.relabel_nodes(graph, mapping)                 

        g = nx.Graph(graph)        
        for e in merge_edges:
            middle = e.start() + ((e.end() - e.start()) * 0.5)
            for a in graph.edges():
                for b in graph.edges():
                    remove_edges = False
                    if a[0] == e.start() and b[0] == e.end():
                        remove_edges = True
                        g.add_edge(a[1], middle)
                        g.add_edge(b[1], middle)
                    elif a[1] == e.start() and b[0] == e.end():
                        remove_edges = True
                        g.add_edge(a[0], middle)
                        g.add_edge(b[1], middle)
                    elif a[1] == e.start() and b[1] == e.end():
                        remove_edges = True
                        g.add_edge(a[0], middle)
                        g.add_edge(b[0], middle)
                    elif a[0] == e.start() and b[1] == e.end():
                        remove_edges = True
                        g.add_edge(a[1], middle)
                        g.add_edge(b[0], middle)
                    if remove_edges:
                        if g.has_edge(a[0], a[1]):
                            g.remove_edge(a[0], a[1])
                        if g.has_edge(b[0], b[1]):
                            g.remove_edge(b[0],b[1])

        graph = g

        components = nx.connected_component_subgraphs(graph)
        closed_polygons = []
        for component in components:
            # create directed graph
            digraph = nx.DiGraph()
            edges = component.edges()
            # and for every edge add the reversed one
            for edge in edges:
                digraph.add_edge(edge[0], edge[1])
                digraph.add_edge(edge[1], edge[0])

            # get all cycles in the graph and sort them for length
            cycles = nx.simple_cycles(digraph)
            cycles = [cycle for cycle in cycles if len(cycle) > 3]
            cycles_with_length = [(self.cycle_len(cycle), cycle) for cycle in cycles]
            sorted_cycles = sorted(cycles_with_length, key=lambda cycle_with_length: cycle_with_length[0])
            sorted_cycles = [cycle for (length, cycle) in sorted_cycles]

            edges_in_cycle_base = []
            minimum_cycles = []
        
            # go through the sorted cycles and take every cycle which has at least
            # one edge that is not in the minimal cycle base
            for cycle in sorted_cycles:
                edges_in_cycle = []
                for i in range(0, len(cycle) - 1):
                    edges_in_cycle.append((cycle[i],cycle[i+1]))

                cycle_independent = False
                for edge in edges_in_cycle:
                    if edge not in edges_in_cycle_base:
                        cycle_independent = True
                        break;
            
                if cycle_independent == True:
                    polygon = Polygon(cycle)
                    contains_cycle = False
                    for minimum_cycle in minimum_cycles:
                        for node in minimum_cycle:
                            if polygon.contains(node.position()) and node not in cycle:
                                contains_cycle = True
                                break
                        if contains_cycle == True:
                            break
                    if contains_cycle == False:               
                        minimum_cycles.append(cycle)
                        edges_in_cycle_base = edges_in_cycle_base + edges_in_cycle
                        edges_in_cycle = [(node1, node0) for (node0, node1) in edges_in_cycle]
                        edges_in_cycle_base = edges_in_cycle_base + edges_in_cycle

            # the polygons are the same as the minimum cycles
            closed_polygons += minimum_cycles
            path_graph = nx.Graph()
            path_graph.add_nodes_from(component.nodes())

            for polygon in minimum_cycles:
                drawable_objects.append(Polygon(polygon))
                path_graph.add_cycle(polygon)

            remaining_graph = nx.difference(component, path_graph)
            for n in remaining_graph.nodes():
                if remaining_graph.degree(n) == 0:
                    remaining_graph.remove_node(n)
            if len(remaining_graph.edges()) > 0:
                remaining_components = nx.connected_component_subgraphs(remaining_graph)
                for c in remaining_components:
                    drawable_objects.append(OpenGraph(c))

        self._drawable_objects = drawable_objects
        self._parsed_data = raw_data
        return
