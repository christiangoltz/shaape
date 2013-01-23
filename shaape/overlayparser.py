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

    CROSSING_LENGTH = 0.5
    CROSSING_HEIGHT = 0.25

    def __init__(self):
        super(OverlayParser, self).__init__()
        self.__sub_overlays = []
        self.__sub_overlays.append(Overlay([['-']], [Edge(Node(0, 0.5), Node(1, 0.5))]))
        self.__sub_overlays.append(Overlay([['|']], [Edge(Node(0.5, 0), Node(0.5, 1))]))
        self.__sub_overlays.append(Overlay([['/']], [Edge(Node(0, 1), Node(1, 0))]))
        self.__sub_overlays.append(Overlay([['\\']], [Edge(Node(1, 1), Node(0, 0))]))
        self.__sub_overlays.append(Overlay([['-','|','-']], [Edge(Node(1, 0.5), Node(2, 0.5))]))
        self.__sub_overlays.append(Overlay([['|'],['-'],['|']], [Edge(Node(0.5, 1), Node(0.5, 2))]))
        self.__sub_overlays.append(Overlay([['+','-']], [Edge(Node(0.5, 0.5, fusable = False), Node(1, 0.5))]))
        self.__sub_overlays.append(Overlay([['-','+']], [Edge(Node(1, 0.5), Node(1.5, 0.5, fusable = False))]))
        self.__sub_overlays.append(Overlay([['+'],['|']], [Edge(Node(0.5, 0.5, fusable = False), Node(0.5, 1))]))
        self.__sub_overlays.append(Overlay([['|'],['+']], [Edge(Node(0.5, 1), Node(0.5, 1.5, fusable = False))]))
        self.__sub_overlays.append(Overlay([[None, '/'],['+', None]], [Edge(Node(1, 1), Node(0.5, 1.5, fusable = False))]))
        self.__sub_overlays.append(Overlay([[None, '*'],['+', None]], [Edge(Node(1.5, 0.5, 'curve'), Node(0.5, 1.5, fusable = False))]))
        self.__sub_overlays.append(Overlay([['*', None],[None, '+']], [Edge(Node(0.5, 0.5, 'curve'), Node(1.5, 1.5, fusable = False))]))
        self.__sub_overlays.append(Overlay([['+', None],[None, '+']], [Edge(Node(0.5, 0.5, fusable = False), Node(1.5, 1.5, fusable = False))]))
        self.__sub_overlays.append(Overlay([[None, '+'],['*', None]], [Edge(Node(1.5, 0.5), Node(0.5, 1.5, 'curve', fusable = False))]))
        self.__sub_overlays.append(Overlay([[None, '+'],['+', None]], [Edge(Node(1.5, 0.5, fusable = False), Node(0.5, 1.5, fusable = False))]))
        self.__sub_overlays.append(Overlay([['+', None],[None, '*']], [Edge(Node(0.5, 0.5), Node(1.5, 1.5, 'curve', fusable = False))]))
        self.__sub_overlays.append(Overlay([['\\', None],[None, '+']], [Edge(Node(1, 1), Node(1.5, 1.5, fusable = False))]))
        self.__sub_overlays.append(Overlay([['+', None],[None, '\\']], [Edge(Node(0.5, 0.5, fusable = False), Node(1, 1))]))
        self.__sub_overlays.append(Overlay([[None, '+'],['/', None]], [Edge(Node(1.5, 0.5, fusable = False), Node(1, 1))]))
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

        self.__sub_overlays.append(Overlay([['+'], ['^']], [Edge(Node(0.5, 0.5), Node(0.5, 1.45))]))
        self.__sub_overlays.append(Overlay([['v'], ['+']], [Edge(Node(0.5, 0.55), Node(0.5, 1.5))]))
        self.__sub_overlays.append(Overlay([['+', '<']], [Edge(Node(0.5, 0.5), Node(2, 0.5))]))
        self.__sub_overlays.append(Overlay([['>', '+']], [Edge(Node(0, 0.5), Node(1.5, 0.5))]))

        self.__sub_overlays.append(Overlay([['*','*']], [Edge(Node(0.5, 0.5, 'curve'), Node(1.5, 0.5, 'curve'))]))
        self.__sub_overlays.append(Overlay([['*'],['*']], [Edge(Node(0.5, 0.5, 'curve'), Node(0.5, 1.5,'curve'))]))
        self.__sub_overlays.append(Overlay([[None, '*'],['*', None]], [Edge(Node(1.5, 0.5, 'curve'), Node(0.5, 1.5,'curve'))]))
        self.__sub_overlays.append(Overlay([['*', None],[None, '*']], [Edge(Node(0.5, 0.5, 'curve'), Node(1.5, 1.5,'curve'))]))

        crossing_top = (1.0 - OverlayParser.CROSSING_LENGTH) / 2.0
        crossing_bottom = 1.0 - (1.0 - OverlayParser.CROSSING_LENGTH) / 2.0
        crossing_top_curve = crossing_top + OverlayParser.CROSSING_LENGTH / 5.0
        crossing_bottom_curve = crossing_bottom - OverlayParser.CROSSING_LENGTH / 5.0
        crossing_left = 0.5 - OverlayParser.CROSSING_HEIGHT
        crossing_right = 0.5 + OverlayParser.CROSSING_HEIGHT

        self.__sub_overlays.append(Overlay([['[']], [Edge(Node(0.5, 0), Node(0.5, crossing_top)), Edge(Node(0.5, crossing_top), Node(crossing_left, crossing_top)), Edge(Node(crossing_left, crossing_top), Node(crossing_left, crossing_bottom)), Edge(Node(0.5, crossing_bottom), Node(crossing_left, crossing_bottom)), Edge(Node(0.5, 1), Node(0.5, crossing_bottom))]))
        self.__sub_overlays.append(Overlay([[']']], [Edge(Node(0.5, 0), Node(0.5, crossing_top)), Edge(Node(0.5, crossing_top), Node(crossing_right, crossing_top)), Edge(Node(crossing_right, crossing_top), Node(crossing_right, crossing_bottom)), Edge(Node(0.5, crossing_bottom), Node(crossing_right, crossing_bottom)), Edge(Node(0.5, 1), Node(0.5, crossing_bottom))]))
        self.__sub_overlays.append(Overlay([[')']], [Edge(Node(0.5, 0, 'curve'), Node(0.5, crossing_top, 'curve')), Edge(Node(0.5, crossing_top, 'curve'), Node(crossing_right, crossing_top_curve, 'curve')), Edge(Node(crossing_right, crossing_top_curve, 'curve'), Node(crossing_right, crossing_bottom_curve, 'curve')), Edge(Node(0.5, crossing_bottom, 'curve'), Node(crossing_right, crossing_bottom_curve, 'curve')), Edge(Node(0.5, 1, 'curve'), Node(0.5, crossing_bottom, 'curve'))]))
        self.__sub_overlays.append(Overlay([['(']], [Edge(Node(0.5, 0, 'curve'), Node(0.5, crossing_top, 'curve')), Edge(Node(0.5, crossing_top, 'curve'), Node(crossing_left, crossing_top_curve, 'curve')), Edge(Node(crossing_left, crossing_top_curve, 'curve'), Node(crossing_left, crossing_bottom_curve, 'curve')), Edge(Node(0.5, crossing_bottom, 'curve'), Node(crossing_left, crossing_bottom_curve, 'curve')), Edge(Node(0.5, 1, 'curve'), Node(0.5, crossing_bottom, 'curve'))]))

        crossing_left = (1.0 - OverlayParser.CROSSING_LENGTH) / 4.0
        crossing_right = 1.0 - (1.0 - OverlayParser.CROSSING_LENGTH) / 4.0
        crossing_left_curve = crossing_left + OverlayParser.CROSSING_LENGTH / 5.0
        crossing_right_curve = crossing_right - OverlayParser.CROSSING_LENGTH / 5.0
        crossing_top = 0.5 - OverlayParser.CROSSING_HEIGHT / 2
        self.__sub_overlays.append(Overlay([['~']], [Edge(Node(0, 0.5, 'curve'), Node(crossing_left, 0.5, 'curve')), Edge(Node(crossing_left, 0.5, 'curve'), Node(crossing_left_curve, crossing_top, 'curve')), Edge(Node(crossing_left_curve, crossing_top, 'curve'), Node(crossing_right_curve, crossing_top, 'curve')), Edge(Node(crossing_right_curve, crossing_top, 'curve'), Node(crossing_right, 0.5, 'curve')), Edge(Node(crossing_right, 0.5, 'curve'), Node(1, 0.5, 'curve'))]))

        for crossing_indicator in ['[', ']', '(', ')']:
            self.__sub_overlays.append(Overlay([['-', crossing_indicator]], [Edge(Node(1, 0.5, fusable = False), Node(1.5, 0.5, fusable = False))]))
            self.__sub_overlays.append(Overlay([[crossing_indicator, '-']], [Edge(Node(0.5, 0.5, fusable = False), Node(1, 0.5, fusable = False))]))

        self.__sub_overlays.append(Overlay([['~'], ['|']], [Edge(Node(0.5, 1, fusable = False), Node(0.5, 0.5, fusable = False))]))
        self.__sub_overlays.append(Overlay([['|'], ['~']], [Edge(Node(0.5, 1, fusable = False), Node(0.5, 1.5, fusable = False))]))
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
        polygons = []
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
                    have_common_node = False
                    for minimum_cycle in minimum_cycles:
                        for node in minimum_cycle:
                            if node in cycle:
                                have_common_node = True
                                break
                        if have_common_node == True:
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
                polygons.append(Polygon(polygon))
                path_graph.add_cycle(polygon)

            remaining_graph = nx.difference(component, path_graph)
            for n in remaining_graph.nodes():
                if remaining_graph.degree(n) == 0:
                    remaining_graph.remove_node(n)
            if len(remaining_graph.edges()) > 0:
                remaining_components = nx.connected_component_subgraphs(remaining_graph)
                for c in remaining_components:
                    drawable_objects.append(OpenGraph(c))

        unordered_polygons = polygons
        current_z_order = 0
        while unordered_polygons:
            for i in range(0, len(unordered_polygons)):
                polygon1 = unordered_polygons[i]
                for j in range(i + 1, len(unordered_polygons)):
                    polygon2 = unordered_polygons[j]
                    if polygon1.contains(polygon2):
                        polygon2.set_z_order(polygon1.z_order() + 1)
                    elif polygon2.contains(polygon1):
                        polygon1.set_z_order(polygon2.z_order() + 1)
            
            current_z_order = current_z_order + 1
            unordered_polygons = filter(lambda p: p.z_order < current_z_order, unordered_polygons)

        drawable_objects = drawable_objects + polygons

        self._drawable_objects = drawable_objects
        self._parsed_data = raw_data
        return
