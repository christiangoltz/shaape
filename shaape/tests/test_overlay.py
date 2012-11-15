from shaape.overlay import Overlay
from shaape.node import Node
from shaape.edge import Edge
import nose
import unittest
from nose.tools import *

class TestOverlay(unittest.TestCase):
    def test_init(self):
        overlay = Overlay()
        assert overlay != None

    def test_substitutes(self):
        overlay = Overlay([[None, '/'],['+', None]], [Edge(Node(1, 1), Node(0.5, 1.5, fusable = False))])
        graph = overlay.substitutes(["  / "," +  "])
        assert len(graph.edges()) == 1

