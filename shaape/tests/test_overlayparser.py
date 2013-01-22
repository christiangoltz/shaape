from shaape.overlayparser import OverlayParser
from shaape.node import Node
from shaape.opengraph import OpenGraph
from shaape.polygon import Polygon
import nose
import unittest
from nose.tools import *

class TestOverlayParser(unittest.TestCase):

    def test_init(self):
        parser = OverlayParser()
        assert parser != None

    def test_cycle_len(self):
        parser = OverlayParser()
        cycle = [Node(0, 0), Node(4, 0), Node(4, 2), Node(0, 2), Node(0, 0)]
        assert parser.cycle_len(cycle) == 12
        
    def test_run(self):
        parser = OverlayParser()
        parser.run("",[])

        parser.run("-",[])
        assert len(parser.drawable_objects()) == 1
        assert type(parser.drawable_objects()[0]) == OpenGraph

        parser.run("- -",[])
        assert len(parser.drawable_objects()) == 2
        assert type(parser.drawable_objects()[0]) == OpenGraph
        assert type(parser.drawable_objects()[1]) == OpenGraph

        parser.run(["++","++"],[])
        assert len(parser.drawable_objects()) == 3, "got " + str(len(parser.drawable_objects())) + " drawable objects"
        assert type(parser.drawable_objects()[0]) == Polygon

        parser.run(["+--+", "| ++", "| ++", "+--+"],[])
        assert len(parser.drawable_objects()) == 6, "got " + str(len(parser.drawable_objects())) + " drawable objects"
        assert type(parser.drawable_objects()[0]) == Polygon
        assert type(parser.drawable_objects()[1]) == Polygon
