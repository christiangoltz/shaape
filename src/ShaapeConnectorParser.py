import networkx as nx
import operator
from ShaapeDrawable import *
from ShaapeParser import *

class EdgeIdentifier:

    def __init__(self, connectors, edges):
        self.m_connectors = connectors
        self.m_edges = edges
        return

    def add_connector(self, offset):
        self.m_connectors += offset
        return

    def add_self_edge(self, start, end):
        self.m_edges += (start, end)
        return
    
    def get_connectors(self):
        return self.m_connectors

    def get_edges(self):
        return self.m_edges

class ShaapeConnectorParser(ShaapeParser):
    def __init__(self):
        super(ShaapeConnectorParser, self).__init__()
        self.m_edge_connectors = {}
        self.m_edge_connectors['|'] = EdgeIdentifier(
                                        [ ((0, -0.5), (0, -0.5)),
                                          ((0, 0.5), (0, 0.5)) ],
                                        [ ((0, -0.5), (0, 0.5))] )
        self.m_edge_connectors['-'] = EdgeIdentifier(
                                        [ ((-0.5, 0), (-0.5, 0)),
                                          ((0.5, 0), (0.5, 0)) ],
                                        [ ((-0.5, 0), (0.5, 0))] )
        self.m_edge_connectors['+'] = EdgeIdentifier(
                                        [ ((-0.5, 0), (0, 0)),
                                          ((0.5, 0), (0, 0)), 
                                          ((0, -0.5), (0, 0)),
                                          ((0, 0.5), (0, 0)),
                                          ((0.5, 0.5), (0, 0)),
                                          ((-0.5, 0.5), (0, 0)),
                                          ((0.5, -0.5), (0, 0)),
                                          ((-0.5, -0.5), (0, 0))],
                                        [] )
        self.m_edge_connectors['>'] = EdgeIdentifier(
                                        [ ((-0.5, 0), (0, 0)),
                                          ((0.5, 0), (0, 0)), 
                                          ((0, -0.5), (0, 0)),
                                          ((0, 0.5), (0, 0))],
                                        [] )
        self.m_edge_connectors['<'] = EdgeIdentifier(
                                        [ ((-0.5, 0), (0, 0)),
                                          ((0.5, 0), (0, 0)), 
                                          ((0, -0.5), (0, 0)),
                                          ((0, 0.5), (0, 0))],
                                        [] )
        self.m_edge_connectors['^'] = EdgeIdentifier(
                                        [ ((-0.5, 0), (0, 0)),
                                          ((0.5, 0), (0, 0)), 
                                          ((0, -0.5), (0, 0)),
                                          ((0, 0.5), (0, 0))],
                                        [] )
        self.m_edge_connectors['v'] = EdgeIdentifier(
                                        [ ((-0.5, 0), (0, 0)),
                                          ((0.5, 0), (0, 0)), 
                                          ((0, -0.5), (0, 0)),
                                          ((0, 0.5), (0, 0))],
                                        [] )
        self.m_edge_connectors['\\'] = EdgeIdentifier(
                                        [ ((-0.5, -0.5), (-0.5, -0.5)),
                                          ((0.5, 0.5), (0.5, 0.5))],
                                        [ ((-0.5, -0.5), (0.5, 0.5))] )
        self.m_edge_connectors['/'] = EdgeIdentifier(
                                        [ ((0.5, -0.5), (0.5, -0.5)),
                                          ((-0.5, 0.5), (-0.5, 0.5))],
                                        [ ((0.5, -0.5), (-0.5, 0.5))] )

        return

    def run(self, ascii_data, drawable_objects):
        graph = nx.Graph()
        possible_connections = {}
        
        # find text

        # find connectors and build a graph of them
        for y in range(0, len(ascii_data)):
            for x in range(0, len(ascii_data[0])): 
                if ascii_data[y][x] in self.m_edge_connectors.keys():
                    for (node_from, node_to) in self.m_edge_connectors[ascii_data[y][x]].get_edges():
                        node_from = tuple(map(operator.add, (x + 0.5, y + 0.5), node_from))
                        node_to = tuple(map(operator.add, (x + 0.5, y + 0.5), node_to))
                        graph.add_edge(node_from, node_to)
                    for (node_from, node_to) in self.m_edge_connectors[ascii_data[y][x]].get_connectors():
                        node_to = tuple(map(operator.add, (x + 0.5, y + 0.5), node_to))
                        node_from = tuple(map(operator.add, (x + 0.5, y + 0.5), node_from))
                        connector = node_from
                        if connector in possible_connections:
                            for point in possible_connections[connector]:
                                if connector <> point:
                                    graph.add_edge(connector, point)
                                if connector <> node_to:
                                    graph.add_edge(connector, node_to)
                        else:
                            graph.add_node(connector)

                        if connector not in possible_connections:
                            possible_connections[connector] = []
                        possible_connections[connector].append(node_to)

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
        print(graph.edges())

        for g in open_graphs:
            drawable_objects.append(ShaapeOpenGraph(g))
            g.add_nodes_from(graph)
            graph = nx.difference(graph, g)


        self._drawable_objects = drawable_objects
        self._parsed_data = ascii_data
        return
