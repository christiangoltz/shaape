import networkx as nx
import operator
import math
from ShaapeDrawable import *
from ShaapeParser import *

class ShaapeEdge:
    def __init__(self, x0, y0, x1, y1):
        self.__start = (x0, y0)
        self.__end = (x1, y1)
        return

    def start(self):
        return self.__start

    def end(self):
        return self.__end

class ShaapeOverlay:
    def __init__(self, array, edges):
        self.__overlay = array
        self.__substitutes = edges
        return

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
                        start = edge.start()
                        end = edge.end()
                        start = (edge.start()[0] + data_x, edge.start()[1] + data_y)
                        end = (edge.end()[0] + data_x, edge.end()[1] + data_y)
                        graph.add_edge(start, end)

        return graph

class ShaapeOverlayParser(ShaapeParser):
    def __init__(self):
        super(ShaapeOverlayParser, self).__init__()
        self.__sub_overlays = []
        self.__sub_overlays.append(ShaapeOverlay([['-']], [ShaapeEdge(0, 0.5, 1, 0.5)]))
        self.__sub_overlays.append(ShaapeOverlay([['|']], [ShaapeEdge(0.5, 0, 0.5, 1)]))
        self.__sub_overlays.append(ShaapeOverlay([['/']], [ShaapeEdge(0, 1, 1, 0)]))
        self.__sub_overlays.append(ShaapeOverlay([['\\']], [ShaapeEdge(1, 1, 0, 0)]))
        self.__sub_overlays.append(ShaapeOverlay([['-','|']], [ShaapeEdge(1, 0.5, 1.5, 0.5)]))
        self.__sub_overlays.append(ShaapeOverlay([['+','-']], [ShaapeEdge(0.5, 0.5, 1, 0.5)]))
        self.__sub_overlays.append(ShaapeOverlay([['-','+']], [ShaapeEdge(1, 0.5, 1.5, 0.5)]))
        self.__sub_overlays.append(ShaapeOverlay([['+'],['|']], [ShaapeEdge(0.5, 0.5, 0.5, 1)]))
        self.__sub_overlays.append(ShaapeOverlay([[None, '/'],['+', None]], [ShaapeEdge(1, 1, 0.5, 1.5)]))
        self.__sub_overlays.append(ShaapeOverlay([['\\', None],[None, '+']], [ShaapeEdge(1, 1, 1.5, 1.5)]))
        self.__sub_overlays.append(ShaapeOverlay([['+', None],[None, '\\']], [ShaapeEdge(0.5, 0.5, 1, 1)]))
        self.__sub_overlays.append(ShaapeOverlay([[None, '+'],['/', None]], [ShaapeEdge(1.5, 0.5, 1, 1)]))
        self.__sub_overlays.append(ShaapeOverlay([['|'],['+']], [ShaapeEdge(0.5, 1, 0.5, 1.5)]))
        self.__sub_overlays.append(ShaapeOverlay([['+','+']], [ShaapeEdge(0.5, 0.5, 1.5, 0.5)]))
        self.__sub_overlays.append(ShaapeOverlay([['+'],['+']], [ShaapeEdge(0.5, 0.5, 0.5, 1.5)]))

        # connect arrows and straight lines
        # self.__sub_overlays.append(ShaapeOverlay([['-', '>']], [ShaapeEdge(1, 0.5, 1.5, 0.5)]))
        # self.__sub_overlays.append(ShaapeOverlay([['<', '-']], [ShaapeEdge(0.5, 0.5, 1, 0.5)]))
        # self.__sub_overlays.append(ShaapeOverlay([['|'], ['v']], [ShaapeEdge(0.5, 1, 0.5, 1.5)]))
        # self.__sub_overlays.append(ShaapeOverlay([['^'], ['|']], [ShaapeEdge(0.5, 0.5, 0.5, 1)]))
        self.__sub_overlays.append(ShaapeOverlay([['|'], ['^']], [ShaapeEdge(0.5, 1, 0.5, 2)]))
        self.__sub_overlays.append(ShaapeOverlay([['v'], ['|']], [ShaapeEdge(0.5, 0, 0.5, 1)]))
        self.__sub_overlays.append(ShaapeOverlay([['-', '<']], [ShaapeEdge(1, 0.5, 2, 0.5)]))
        self.__sub_overlays.append(ShaapeOverlay([['>', '-']], [ShaapeEdge(0, 0.5, 1, 0.5)]))

        # connect arrows and +
        # self.__sub_overlays.append(ShaapeOverlay([['+'], ['^']], [ShaapeEdge(0.5, 0.5, 0.5, 1.5)]))
        # self.__sub_overlays.append(ShaapeOverlay([['v'], ['+']], [ShaapeEdge(0.5, 0.5, 0.5, 1.5)]))
        # self.__sub_overlays.append(ShaapeOverlay([['+', '<']], [ShaapeEdge(0.5, 0.5, 1.5, 0.5)]))
        # self.__sub_overlays.append(ShaapeOverlay([['>', '+']], [ShaapeEdge(0.5, 0.5, 1.5, 0.5)]))
        return

    def cycle_len(self, cycle):
        length = 0
        for i in range(0, len(cycle) - 1):
            length = length + math.sqrt((cycle[i + 1][0] - cycle[i][0])**2 + (cycle[i + 1][1] - cycle[i][1])**2)
        return length

    def run(self, raw_data, drawable_objects):
        graphs = []

        for overlay in self.__sub_overlays:
            graphs.append(overlay.substitutes(raw_data))

        graph = graphs.pop(0)
        for h in graphs:
            graph = nx.compose(graph, h)

        # mapping = dict(zip(graph , graph)) 
        # graph=nx.relabel_nodes(graph, mapping)                 

        # create directed graph
        digraph = nx.DiGraph(graph)
        edges = graph.edges()
        # and for every edge add the reversed one
        for edge in edges:
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
                polygon = ShaapePolygon(cycle)
                contains_cycle = False
                for minimum_cycle in minimum_cycles:
                    for node in minimum_cycle:
                        if polygon.contains(node) and node not in polygon.nodes():
                            contains_cycle = True
                            break
                    if contains_cycle == True:
                        break

                if contains_cycle == False:               
                    minimum_cycles.append(cycle)
                    edges_in_cycle_base = edges_in_cycle_base + edges_in_cycle
                    edges_in_cycle = [(node1, node0) for (node0, node1) in edges_in_cycle]
                    edges_in_cycle_base = edges_in_cycle_base + edges_in_cycle

        # our polygons are the same as the minimum cycles
        closed_polygons = minimum_cycles
        path_graph = nx.Graph()
        path_graph.add_nodes_from(graph.nodes())
        for polygon in closed_polygons:
            drawable_objects.append(ShaapePolygon(polygon))
            path_graph.add_cycle(polygon)

        graph = nx.difference(graph, path_graph)
        for n in graph.nodes():
            if graph.degree(n) == 0:
                graph.remove_node(n)

        open_graphs = nx.connected_component_subgraphs(graph)

        for g in open_graphs:
            drawable_objects.append(ShaapeOpenGraph(g))
            g.add_nodes_from(graph)
            graph = nx.difference(graph, g)
        self._drawable_objects = drawable_objects
        self._parsed_data = raw_data
        return
