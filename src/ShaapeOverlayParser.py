import networkx as nx
import operator
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
        self.__sub_overlays.append(ShaapeOverlay([['-', '>']], [ShaapeEdge(1, 0.5, 1.5, 0.5)]))
        self.__sub_overlays.append(ShaapeOverlay([['<', '-']], [ShaapeEdge(0.5, 0.5, 1, 0.5)]))
        self.__sub_overlays.append(ShaapeOverlay([['|'], ['v']], [ShaapeEdge(0.5, 1, 0.5, 1.5)]))
        self.__sub_overlays.append(ShaapeOverlay([['^'], ['|']], [ShaapeEdge(0.5, 0.5, 0.5, 1)]))
        return


    def run(self, raw_data, drawable_objects):
        graphs = []

        for overlay in self.__sub_overlays:
            graphs.append(overlay.substitutes(raw_data))

        graph = graphs.pop(0)
        for h in graphs:
            graph = nx.compose(graph, h)

        mapping = dict(zip(graph , graph)) 
        graph=nx.relabel_nodes(graph, mapping)                 

        closed_polygons = nx.cycle_basis(graph) 
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
