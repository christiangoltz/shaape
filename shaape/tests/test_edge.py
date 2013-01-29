from shaape.edge import Edge
from shaape.node import Node
import nose
import unittest
from nose.tools import *

class TestEdge(unittest.TestCase):
    def test_init(self):
        edge = Edge(Node(0, 0), Node(2, 2))
        assert edge != None

    def test_start_end(self):
        start = Node(1.5, -0.5)
        end = Node(3.5, -0.5)
        edge = Edge(start, end)
        assert edge.start() == start
        assert edge.end() == end

    def test_intersects(self):
        edge1 = Edge(Node(-2, 0), Node(2, 1))
        edge2 = Edge(Node(0, 1), Node(0, -1))
        edge3 = Edge(Node(-2, 1), Node(2, 2))
        assert edge1.intersects(edge2)
        assert not edge1.intersects(edge3)
        assert_raises(TypeError, edge1.intersects, 1)
        

