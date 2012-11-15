from shaape.drawingbackend import DrawingBackend
from shaape.background import Background
from shaape.node import Node
from shaape.opengraph import OpenGraph
from shaape.polygon import Polygon
from shaape.rightarrow import RightArrow
from shaape.text import Text
from shaape.translatable import Translatable
from shaape.tests.utils import TestUtils
import copy
import nose
import unittest
from mock import MagicMock
from nose.tools import *

class TestDrawingBackend(unittest.TestCase):
    def setUp(self):
        self.__backend = DrawingBackend()

    def test_init(self):
        assert self.__backend != None

    def test_scale(self):
        assert self.__backend.scale() == DrawingBackend.DEFAULT_SCALE
        
    def test_canvas_size(self):
        assert self.__backend.canvas_size() == DrawingBackend.DEFAULT_CANVAS_SIZE
        self.__backend.set_canvas_size(40, 50) 
        assert self.__backend.canvas_size() == (40, 50)

    def test_run(self):
        background = Background((400, 300)) 
        polygon = TestUtils.generate_test_polygon(seed = 0, points = 12, radius_range = (1, 10))
        polygon_copy = copy.deepcopy(polygon)
        objects = [background, polygon, Translatable()]
        self.__backend.draw_objects = MagicMock()
        self.__backend.create_canvas = MagicMock()
        self.__backend.export_to_file = MagicMock()
        self.__backend.run(objects, "testname")
        unit = self.__backend.unit_size()
        assert self.__backend.canvas_size() == (400 * unit[0], 300 * unit[1])
        assert polygon.nodes() == map(lambda point: Node(point[0] * unit[0], point[1] * unit[1]), polygon_copy.nodes())
        self.__backend.draw_objects.assert_called(objects)
        self.__backend.create_canvas.assert_called(objects)
        self.__backend.export_to_file.assert_called_with("testname")
        assert TestUtils.unordered_lists_equal(self.__backend.draw_objects.call_args[0][0], objects)

    def test_draw_objects(self):
        polygon1 = TestUtils.generate_test_polygon(seed = 0, points = 12, radius_range = (1, 10))
        polygon2 = copy.deepcopy(polygon1)
        polygon2.style().set_shadow('off')
        opengraph1 = TestUtils.generate_test_opengraph(seed = 0, points = 12, radius_range = (1, 10))
        opengraph2 = copy.deepcopy(opengraph1)
        opengraph2.style().set_shadow('off')
        text = Text()
        arrow = RightArrow()
        objects = [polygon1, polygon2, opengraph1, opengraph2, text, arrow]
        self.__backend.push_surface = MagicMock()
        self.__backend.pop_surface = MagicMock()
        self.__backend.draw_polygon_shadow = MagicMock()
        self.__backend.draw_polygon = MagicMock()
        self.__backend.draw_open_graph_shadow = MagicMock()
        self.__backend.draw_open_graph = MagicMock()
        self.__backend.draw_text = MagicMock()
        self.__backend.translate = MagicMock()
        self.__backend.blur_surface = MagicMock()
        self.__backend.draw_objects(objects)
        assert self.__backend.push_surface.call_count == self.__backend.pop_surface.call_count
        self.__backend.translate.assert_called_once_with(*(self.__backend.shadow_translation()))

        assert self.__backend.draw_polygon.call_count == 3
        self.__backend.draw_polygon.assert_any_call(polygon1)
        self.__backend.draw_polygon.assert_any_call(polygon2)
        self.__backend.draw_polygon.assert_any_call(arrow)

        assert self.__backend.draw_polygon_shadow.call_count == 2
        self.__backend.draw_polygon_shadow.assert_any_call(polygon1)
        self.__backend.draw_polygon_shadow.assert_any_call(arrow)

        assert self.__backend.draw_open_graph.call_count == 4
        self.__backend.draw_open_graph.assert_any_call(polygon1.frame())
        self.__backend.draw_open_graph.assert_any_call(polygon2.frame())
        self.__backend.draw_open_graph.assert_any_call(opengraph1)
        self.__backend.draw_open_graph.assert_any_call(opengraph2)

        self.__backend.draw_open_graph_shadow.assert_called_once_with(opengraph1)
 
        self.__backend.draw_text.assert_called_once_with(text)

        self.__backend.blur_surface.assert_called_once_with()
         
    def test_abstracts(self):
        assert_raises(NotImplementedError,  self.__backend.draw_polygon_shadow)
        assert_raises(NotImplementedError,  self.__backend.draw_polygon)
        assert_raises(NotImplementedError,  self.__backend.draw_open_graph_shadow)
        assert_raises(NotImplementedError,  self.__backend.draw_open_graph)
        assert_raises(NotImplementedError,  self.__backend.draw_text)
        assert_raises(NotImplementedError,  self.__backend.push_surface)
        assert_raises(NotImplementedError,  self.__backend.pop_surface)
        assert_raises(NotImplementedError,  self.__backend.translate)
        assert_raises(NotImplementedError,  self.__backend.blur_surface)
