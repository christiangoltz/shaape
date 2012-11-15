import networkx as nx
import operator
import math
from opengraph import OpenGraph
from polygon import Polygon
from parser import *
from node import *
from edge import Edge
from overlay import Overlay

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
        self.__sub_overlays.append(Overlay([[None, '*'],['+', None]], [Edge(Node(1.5, 0.5, 'curve'), Node(0.5, 1.5, fusable = False))]))
        self.__sub_overlays.append(Overlay([['*', None],[None, '+']], [Edge(Node(0.5, 0.5, 'curve'), Node(1.5, 1.5, fusable = False))]))
        self.__sub_overlays.append(Overlay([[None, '+'],['*', None]], [Edge(Node(1.5, 0.5), Node(0.5, 1.5, 'curve', fusable = False))]))
        self.__sub_overlays.append(Overlay([['+', None],[None, '*']], [Edge(Node(0.5, 0.5), Node(1.5, 1.5, 'curve', fusable = False))]))
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

        self.__sub_overlays.append(Overlay([['|'], ['v']], [Edge(Node(0.5, 1), Node(0.5, 1.55))]))
        self.__sub_overlays.append(Overlay([['^'], ['|']], [Edge(Node(0.5, 0.45), Node(0.5, 1))]))

        self.__sub_overlays.append(Overlay([['|'], ['^']], [Edge(Node(0.5, 1), Node(0.5, 1.45))]))
        self.__sub_overlays.append(Overlay([['v'], ['|']], [Edge(Node(0.5, 0.55), Node(0.5, 1))]))
        self.__sub_overlays.append(Overlay([['-', '<']], [Edge(Node(1, 0.5), Node(2, 0.5))]))
        self.__sub_overlays.append(Overlay([['>', '-']], [Edge(Node(0, 0.5), Node(1, 0.5))]))

        self.__sub_overlays.append(Overlay([['*','*']], [Edge(Node(0.5, 0.5, 'curve'), Node(1.5, 0.5, 'curve'))]))
        self.__sub_overlays.append(Overlay([['*'],['*']], [Edge(Node(0.5, 0.5, 'curve'), Node(0.5, 1.5,'curve'))]))
        self.__sub_overlays.append(Overlay([[None, '*'],['*', None]], [Edge(Node(1.5, 0.5, 'curve'), Node(0.5, 1.5,'curve'))]))
        self.__sub_overlays.append(Overlay([['*', None],[None, '*']], [Edge(Node(0.5, 0.5, 'curve'), Node(1.5, 1.5,'curve'))]))

        return

    def cycle_len(self, cycle):
        length = 0
        for i in range(0, len(cycle) - 1):
            length = length + (cycle[i + 1] - cycle[i]).length()
        return length

    def run(self, raw_data, drawable_objects):
        graphs = []
        for overlay in self.__sub_overlays:
            g = overlay.substitutes(raw_data)
            graphs.append(g)

        graph = graphs.pop(0)
        for h in graphs:
            graph = nx.compose(graph, h)

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
