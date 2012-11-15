from shaape.polygon import Polygon
from shaape.node import Node
import nose
import unittest
from nose.tools import *
from shaape.tests.utils import TestUtils

class TestPolygon(unittest.TestCase):
    def test_init(self):
        polygon = Polygon([Node(0, 0)])
        assert polygon != None
        assert_raises(ValueError, Polygon, [])

    def test_contains(self):
        polygon = TestUtils.generate_test_polygon(seed = 0, points = 12, radius_range = (5, 10))
        assert polygon.contains((2,3)) == True
        assert polygon.contains((11,3)) == False
        assert polygon.contains((3,11)) == False

        polygon = Polygon([Node(0, 0), Node(4, 0), Node(17, 4), Node(0, 4), Node(0, 0)])
        assert polygon.contains((8,1)) == False

    def test_nodes(self):
        polygon = Polygon([Node(0, 0), Node(4, 0)])
        assert polygon.nodes() == [Node(0, 0), Node(4, 0)]

    def test_min_max(self):
        polygon = Polygon([Node(-1, 5), Node(4, 1)])
        assert polygon.min() == (-1, 1)
        assert polygon.max() == (4, 5)

    def test_scale(self):
        polygon = Polygon([Node(-1, 5), Node(4, 1)])
        polygon.scale((2, 3))
        assert polygon.nodes() == [Node(-2, 15), Node(8, 3)]

    def test_frame(self):
        polygon = Polygon([Node(-1, 5), Node(4, 1)])
        assert len(polygon.frame().paths()) == 1
        assert len(polygon.frame().paths()[0]) == 2
        assert TestUtils.unordered_lists_equal([Node(-1, 5), Node(4, 1)], polygon.frame().paths()[0])
