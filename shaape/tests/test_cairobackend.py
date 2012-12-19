from shaape.cairobackend import CairoBackend
from shaape.tests.utils import TestUtils
from shaape.shaape import Shaape
from shaape.drawable import Drawable
from shaape.polygon import Polygon
from shaape.opengraph import OpenGraph
from shaape.text import Text
from shaape.translatable import Translatable
from shaape.rotatable import Rotatable
from shaape.node import Node
import nose
import unittest
from nose.tools import *
import cairo
import math
import networkx as nx
import operator
import os
import copy
import errno
from mock import patch

class TestCairoBackend(unittest.TestCase):

    def setUp(self):
        self.__backend = CairoBackend()

    def test_init(self):
        assert self.__backend != None

    def test_margin(self):
        assert self.__backend.margin() == CairoBackend.DEFAULT_MARGIN
        self.__backend.set_margin(50, 40, 30, 20)
        assert self.__backend.margin() == (50, 40, 30, 20)

    def test_blur_surface(self):
        test_img_surface = cairo.ImageSurface.create_from_png(TestUtils.BLUR_INPUT)
        self.__backend.set_image_size(test_img_surface.get_width(), test_img_surface.get_height())
        self.__backend.set_margin(0, 0, 0, 0)
        self.__backend.push_surface()
        self.__backend.ctx().set_source_surface(test_img_surface)
        self.__backend.ctx().paint()
        self.__backend.blur_surface()
        self.__backend.export_to_file(TestUtils.BLUR_GENERATED_IMAGE)
        assert TestUtils.images_equal(TestUtils.BLUR_GENERATED_IMAGE, TestUtils.BLUR_EXPECTED_IMAGE)

    def test_push_surface(self):
        assert len(self.__backend.surfaces()) == 0
        self.__backend.push_surface()
        previous_surface = self.__backend.surfaces()[-1]
        for i in range(0, 10):
            self.__backend.push_surface()
            assert previous_surface == self.__backend.surfaces()[-2]
            assert len(self.__backend.surfaces()) == i + 2
            previous_surface = self.__backend.surfaces()[-1]

    def test_pop_surface(self):
        assert len(self.__backend.surfaces()) == 0
        for i in range(0, 10):
            self.__backend.push_surface()
        for i in range(10, 0):
            self.__backend.pop_surface()
            assert len(self.__backend.surfaces()) == i

    def test_set_image_size(self):
        self.__backend.set_image_size(200, 300)
        assert self.__backend.image_size() == (200, 300)

    def test_create_canvas(self):
        self.__backend.create_canvas()
        self.__backend.export_to_file(TestUtils.EMPTY_CANVAS_GENERATED_IMAGE)
        assert TestUtils.images_equal(TestUtils.EMPTY_CANVAS_GENERATED_IMAGE, TestUtils.EMPTY_CANVAS_EXPECTED_IMAGE)
        with patch('os.makedirs', side_effect=OSError(errno.EPERM)):
            assert_raises(OSError, self.__backend.export_to_file, TestUtils.EMPTY_CANVAS_GENERATED_IMAGE)
       
    def test_apply_dash(self):
        drawable = Drawable()
        drawable.style().set_type('dashed')  
        self.__backend.create_canvas()
        self.__backend.apply_dash(drawable)
        dash = self.__backend.ctx().get_dash()
        assert len(dash) == 2
        assert len(dash[0]) == 2
        assert dash[0][0] != 0
        assert dash[0][0] == 4 * dash[0][1]
        assert dash[1] == 0
        
        drawable.style().set_type('dotted')  
        self.__backend.create_canvas()
        self.__backend.apply_dash(drawable)
        dash = self.__backend.ctx().get_dash()
        assert len(dash) == 2
        assert len(dash[0]) == 2
        assert dash[0][0] != 0
        assert dash[0][0] == dash[0][1]
        assert dash[1] == 0

        drawable.style().set_type('dash-dotted')  
        self.__backend.create_canvas()
        self.__backend.apply_dash(drawable)
        dash = self.__backend.ctx().get_dash()
        assert len(dash) == 2
        assert len(dash[0]) == 4
        assert dash[0][0] != 0
        assert dash[0][0] == 4 * dash[0][1]
        assert dash[0][0] == 4 * dash[0][2]
        assert dash[0][0] == 4 * dash[0][3]
        assert dash[1] == 0

        drawable.style().set_type('solid')  
        self.__backend.create_canvas()
        self.__backend.apply_dash(drawable)
        dash = self.__backend.ctx().get_dash()
        assert len(dash) == 2
        assert len(dash[0]) == 0

    def test_apply_line(self):
        drawable = Drawable()
        self.__backend.create_canvas()
        drawable.style().set_width(4.5)  
        drawable.style().set_color((0.1, 0.2, 0.3)) 
        self.__backend.apply_line(drawable)
        assert self.__backend.ctx().get_line_cap() == cairo.LINE_CAP_BUTT 
        assert self.__backend.ctx().get_line_join() == cairo.LINE_JOIN_ROUND 
        assert math.fabs(self.__backend.ctx().get_line_width() - drawable.style().width() * self.__backend.scale()) < 0.1
        assert type(self.__backend.ctx().get_source()) == cairo.SolidPattern
        assert self.__backend.ctx().get_source().get_rgba() == (0.1, 0.2, 0.3, 1.0)
        
        drawable.style().set_color((0.1, 0.2, 0.3, 0.4)) 
        self.__backend.apply_line(drawable)
        assert type(self.__backend.ctx().get_source()) == cairo.SolidPattern
        assert self.__backend.ctx().get_source().get_rgba() == (0.1, 0.2, 0.3, 0.4)

        dash = self.__backend.ctx().get_dash()
        assert len(dash) == 2
        assert len(dash[0]) == 0

    def test_apply_fill(self):
        drawable = Polygon([Node(0,0)])
        self.__backend.create_canvas()
        drawable.style().set_color((0.1, 0.2, 0.3)) 
        drawable.style().set_type('solid') 
        self.__backend.apply_fill(drawable)
        assert type(self.__backend.ctx().get_source()) == cairo.SolidPattern
        assert self.__backend.ctx().get_source().get_rgba() == (0.1, 0.2, 0.3, 1.0)

        drawable.style().set_color((0.1, 0.2, 0.3, 0.4)) 
        self.__backend.apply_fill(drawable)
        assert self.__backend.ctx().get_source().get_rgba() == (0.1, 0.2, 0.3, 0.4)

        drawable.style().set_color((0.1, 0.2, 0.3)) 
        drawable.style().set_type('gradient') 
        self.__backend.apply_fill(drawable)
        assert type(self.__backend.ctx().get_source()) == cairo.LinearGradient

        drawable.style().set_color((0.1, 0.2, 0.3, 0.4)) 
        drawable.style().set_type('gradient') 
        self.__backend.apply_fill(drawable)
        assert type(self.__backend.ctx().get_source()) == cairo.LinearGradient

    def test_draw_polygon(self):
        point_list = [(10, 10), (40, 10), (30, 20), (40, 40), (20, 30), (10, 10)]
        node_list = [Node(*p) for p in point_list]
        polygon1 = Polygon(node_list)
        polygon2 = Polygon(node_list[:-1])
                
        self.__backend.set_canvas_size(50, 100)
        self.__backend.create_canvas()
        self.__backend.push_surface()
        self.__backend.draw_polygon(polygon1)
        self.__backend.translate(0, 50)
        self.__backend.draw_polygon(polygon2)
        self.__backend.export_to_file(TestUtils.POLYGON_GENERATED_IMAGE)
        self.__backend.pop_surface()
        assert TestUtils.images_equal(TestUtils.POLYGON_GENERATED_IMAGE, TestUtils.POLYGON_EXPECTED_IMAGE)

    def test_draw_polygon_shadow(self):
        point_list = [(10, 10), (40, 10), (30, 20), (40, 40), (20, 30), (10, 10)]
        node_list = [Node(*p) for p in point_list]
        polygon1 = Polygon(node_list)
        polygon2 = Polygon(node_list[:-1])
                
        self.__backend.set_canvas_size(50, 100)
        self.__backend.create_canvas()
        self.__backend.push_surface()
        self.__backend.draw_polygon_shadow(polygon1)
        self.__backend.translate(0, 50)
        self.__backend.draw_polygon_shadow(polygon2)
        self.__backend.export_to_file(TestUtils.POLYGON_SHADOW_GENERATED_IMAGE)
        self.__backend.pop_surface()
        assert TestUtils.images_equal(TestUtils.POLYGON_SHADOW_GENERATED_IMAGE, TestUtils.POLYGON_SHADOW_EXPECTED_IMAGE)

    def test_draw_open_graph(self):
        self.__backend.set_canvas_size(80, 80)
        self.__backend.create_canvas()
        graph = nx.Graph()
        open_graph = OpenGraph(graph)

        self.__backend.push_surface()
        self.__backend.draw_open_graph(open_graph)
        self.__backend.export_to_file(TestUtils.OPEN_GRAPH_EMPTY_GENERATED_IMAGE)
        self.__backend.pop_surface()
        assert TestUtils.images_equal(TestUtils.OPEN_GRAPH_EMPTY_GENERATED_IMAGE, TestUtils.OPEN_GRAPH_EMPTY_EXPECTED_IMAGE)

        graph.add_edge(Node(10, 10), Node(20, 10))
        graph.add_edge(Node(20, 10), Node(20, 20))
        graph.add_edge(Node(20, 20), Node(10, 20))
        graph.add_edge(Node(10, 20), Node(10, 10))
        open_graph = OpenGraph(graph)
        self.__backend.push_surface()
        self.__backend.draw_open_graph(open_graph)
        self.__backend.export_to_file(TestUtils.OPEN_GRAPH_CLOSED_GENERATED_IMAGE)
        self.__backend.pop_surface()
        assert TestUtils.images_equal(TestUtils.OPEN_GRAPH_CLOSED_GENERATED_IMAGE, TestUtils.OPEN_GRAPH_CLOSED_EXPECTED_IMAGE)



        graph = nx.Graph()
        edge_list = [((10, 10), (40, 10)), ((40, 10), (60, 10)), ((40, 10), (50, 40)), ((50, 40), (20, 30)), ((50, 40), (50, 60))]
        for edge in edge_list:
            graph.add_edge(Node(*edge[0]), Node(*edge[1]))
        graph.add_edge(Node(50, 60, 'curve'), Node(20, 80, 'curve'))
        graph.add_edge(Node(20, 80, 'curve'), Node(40, 90, 'curve'))
        open_graph = OpenGraph(graph)
                
        self.__backend.push_surface()
        self.__backend.draw_open_graph(open_graph)
        self.__backend.export_to_file(TestUtils.OPEN_GRAPH_GENERATED_IMAGE)
        self.__backend.pop_surface()
        assert TestUtils.images_equal(TestUtils.OPEN_GRAPH_GENERATED_IMAGE, TestUtils.OPEN_GRAPH_EXPECTED_IMAGE)

    def test_draw_open_graph_shadow(self):
        self.__backend.set_canvas_size(50, 150)
        self.__backend.create_canvas()
        graph = nx.Graph()
        open_graph = OpenGraph(graph)

        self.__backend.push_surface()
        self.__backend.draw_open_graph_shadow(open_graph)
        self.__backend.export_to_file(TestUtils.OPEN_GRAPH_SHADOW_EMPTY_GENERATED_IMAGE)
        self.__backend.pop_surface()
        assert TestUtils.images_equal(TestUtils.OPEN_GRAPH_SHADOW_EMPTY_GENERATED_IMAGE, TestUtils.OPEN_GRAPH_SHADOW_EMPTY_EXPECTED_IMAGE)

        edge_list = [((10, 10), (40, 10)), ((40, 10), (60, 10)), ((40, 10), (50, 40)), ((50, 40), (20, 30)), ((50, 40), (50, 60))]
        edge_list2 = [((10, 10), (40, 10)), ((40, 10), (50, 40)), ((50, 40), (20, 30)),((20, 30), (10, 10))]
        for edge in edge_list:
            graph.add_edge(Node(*edge[0]), Node(*edge[1]))
        graph2 = nx.Graph()
        for edge in edge_list2:
            graph2.add_edge(Node(*edge[0], style = 'curve'), Node(*edge[1], style = 'curve'))
        open_graph = OpenGraph(graph)
        open_graph2 = OpenGraph(graph2)
                
        self.__backend.push_surface()
        self.__backend.draw_open_graph_shadow(open_graph)
        self.__backend.translate(0, 60)
        self.__backend.draw_open_graph_shadow(open_graph2)
        self.__backend.export_to_file(TestUtils.OPEN_GRAPH_SHADOW_GENERATED_IMAGE)
        self.__backend.pop_surface()
        assert TestUtils.images_equal(TestUtils.OPEN_GRAPH_SHADOW_GENERATED_IMAGE, TestUtils.OPEN_GRAPH_SHADOW_EXPECTED_IMAGE)

    def test_draw_text(self):
        text = Text("abcdef123456!=_/>")
        text.scale((10,20))
        self.__backend.set_canvas_size(160, 30)
        self.__backend.create_canvas()
        self.__backend.push_surface()
        self.__backend.draw_text(text)
        self.__backend.export_to_file(TestUtils.TEXT_GENERATED_IMAGE)
        self.__backend.pop_surface()
        self.__backend.push_surface()
        assert TestUtils.images_equal(TestUtils.TEXT_GENERATED_IMAGE, TestUtils.TEXT_EXPECTED_IMAGE)

    def test_apply_transform(self):
        translatable = Translatable((10, 20))
        angle = 145
        rotatable = Rotatable(angle)
        self.__backend.create_canvas()

        self.__backend.push_surface()
        self.__backend.apply_transform(translatable)
        matrix = self.__backend.ctx().get_matrix()
        assert matrix[4] == 10
        assert matrix[5] == 20
        self.__backend.pop_surface()

        self.__backend.push_surface()
        self.__backend.apply_transform(rotatable)
        matrix = self.__backend.ctx().get_matrix()
        c = math.cos(math.radians(angle))
        s = math.sin(math.radians(angle))
        assert sum(map(operator.sub, matrix, (c, s, -1 * s, c, 0, 0))) == 0
        self.__backend.pop_surface()

    def test_export_to_file(self):
        if os.path.exists(TestUtils.EXPORT_TEST_FILE):
            os.remove(TestUtils.EXPORT_TEST_FILE)
        self.__backend.create_canvas()
        self.__backend.export_to_file(TestUtils.EXPORT_TEST_FILE)
        assert os.path.exists(TestUtils.EXPORT_TEST_FILE)

    def test_ctx(self):
        assert self.__backend.ctx() == None
        self.__backend.create_canvas()
        assert type(self.__backend.ctx()) == cairo.Context

    def test_translate(self):
        self.__backend.create_canvas()
        self.__backend.push_surface()
        self.__backend.translate(15, 20)
        matrix = self.__backend.ctx().get_matrix()
        assert matrix[4] == 15
        assert matrix[5] == 20
        self.__backend.pop_surface()

