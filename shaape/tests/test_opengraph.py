from shaape.opengraph import OpenGraph
from shaape.node import Node
from shaape.tests.utils import TestUtils
import nose
import unittest
from nose.tools import *
import networkx as nx
import copy

class TestOpenGraph(unittest.TestCase):

    def test_init(self):
        opengraph = OpenGraph()
        assert opengraph != None
        assert opengraph.style().target_type() == 'line'
        assert opengraph.paths() == []

    def test_graph(self):
        opengraph = OpenGraph()
        assert opengraph.graph().nodes() == []

    def test_min_max(self):
        graph = nx.Graph()
        graph.add_node(Node(0,-1))
        graph.add_node(Node(1,1))
        graph.add_node(Node(-2,4))
        graph.add_node(Node(3,-5))
        opengraph = OpenGraph(graph)
        assert opengraph.min() == (-2, -5)
        assert opengraph.max() == (3, 4)

    def test_scale(self):
        original_g = TestUtils.generate_test_opengraph(seed = 0, points = 12, radius_range = (5, 5))
        g = copy.deepcopy(original_g)
        scale = (2, 3)
        g.scale(scale)
        assert len(g.graph().nodes()) == len(original_g.graph().nodes())
        for node in original_g.graph().nodes():
            assert Node(node[0] * scale[0], node[1] * scale[1]) in g.graph().nodes()

    def test_paths(self):
        g = nx.Graph()
        g.add_edge(Node(0, 0), Node(1, 0))
        g.add_edge(Node(3, 0), Node(2, 0))
        g.add_edge(Node(2, 0), Node(1, 0))
        g.add_edge(Node(2, 0), Node(2, 2))
        g.add_edge(Node(3, 0), Node(3, 2))
        opengraph = OpenGraph(g)
        assert len(opengraph.paths()) == 2
        

        
