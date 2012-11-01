from shaape.cairobackend import CairoBackend
from shaape.tests.utils import TestUtils
from shaape.shaape import Shaape
from shaape.drawable import Drawable
from shaape.drawable import Polygon
from shaape.node import Node
import nose
import unittest
from nose.tools import *
import cairo
import math

class TestCairoBackend(unittest.TestCase):

    def setUp(self):
        self.__backend = CairoBackend()

    def test_init(self):
        assert self.__backend != None

    def test_blur_surface(self):
        test_img_surface = cairo.ImageSurface.create_from_png(TestUtils.BLUR_INPUT)
        self.__backend.set_image_size(test_img_surface.get_width(), test_img_surface.get_height())
        self.__backend.set_margin(0, 0, 0, 0)
        self.__backend.push_surface()
        self.__backend.ctx().set_source_surface(test_img_surface)
        self.__backend.ctx().paint()
        self.__backend.blur_surface()
        self.__backend.export_to_file(TestUtils.BLUR_GENERATED_IMAGE)
        assert TestUtils.imagesEqual(TestUtils.BLUR_GENERATED_IMAGE, TestUtils.BLUR_EXPECTED_IMAGE)

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
        assert TestUtils.imagesEqual(TestUtils.EMPTY_CANVAS_GENERATED_IMAGE, TestUtils.EMPTY_CANVAS_EXPECTED_IMAGE)
       
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
        drawable = Drawable()
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

    def test_draw_polygon(self):
        point_list = [(10, 10), (40, 10), (30, 20), (40, 40), (20, 30), (10, 10)]
        node_list = [Node(*p) for p in point_list]
        polygon = Polygon(node_list)
                
        self.__backend.set_canvas_size(50, 50)
        self.__backend.create_canvas()
        self.__backend.push_surface()
        self.__backend.draw_polygon(polygon)
        self.__backend.export_to_file(TestUtils.POLYGON_GENERATED_IMAGE)
        self.__backend.pop_surface()
        assert TestUtils.imagesEqual(TestUtils.POLYGON_GENERATED_IMAGE, TestUtils.POLYGON_EXPECTED_IMAGE)
