from shaape.graphalgorithms import *
from shaape.node import Node
import nose
import unittest
from nose.tools import *

class TestGraphAlgorithms(unittest.TestCase):

    def test_reduce_path(self):
        path = [Node(0, 0), Node(1, 0), Node(2, 0), Node(3,0), Node(4, 1), Node(5, 2)]
        reduced_path = reduce_path(path)
        assert reduced_path == [Node(0, 0), Node(3, 0), Node(5, 2)]

        path = [Node(0, 0), Node(1, 0), Node(2, 0), Node(3,0), Node(3, 3), Node(-1, 0), Node(0, 0)]
        reduced_path = reduce_path(path)
        assert reduced_path == [Node(-1, 0), Node(3, 0), Node(3, 3), Node(-1, 0)]

    def test_has_same_direction(self):
        assert has_same_direction(Node(0, 0), Node(0, 0)) == False
        assert has_same_direction(Node(0, 0), Node(1, 0)) == False
        assert has_same_direction(Node(1, 0), Node(-2, 0)) == True
        assert has_same_direction(Node(1, 2), Node(2, 4)) == True
        assert has_same_direction(Node(1, 2), Node(-2, -4)) == True
        assert has_same_direction(Node(1, 2), Node(2, 3)) == False

    def test_is_chord_free(self):
        graph = nx.Graph()
        graph.add_edge(Node(0.5, 0.5), Node(0.5, 1.5))
        graph.add_edge(Node(0.5, 0.5), Node(1.5, 1.5))
        graph.add_edge(Node(0.5, 0.5), Node(1.5, 0.5))
        graph.add_edge(Node(0.5, 1.5), Node(1.5, 1.5))
        graph.add_edge(Node(0.5, 1.5), Node(1.5, 0.5))
        graph.add_edge(Node(1.5, 0.5), Node(1.5, 1.5))
        cycle = [Node(1.5, 1.5), Node(0.5, 1.5), Node(0.5, 0.5), Node(1.5, 0.5), Node(1.5, 1.5)]
        assert is_chord_free(graph, cycle) == False
