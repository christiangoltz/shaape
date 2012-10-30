from shaape.cairobackend import CairoBackend
from shaape.tests.utils import TestUtils
from shaape.shaape import Shaape
import nose
import unittest
from nose.tools import *
import cairo

class TestCairoBackend(unittest.TestCase):
    def test_init(self):
        backend = CairoBackend()
        assert backend != None

    def test_blur_surface(self):
        backend = CairoBackend()
        test_img_surface = cairo.ImageSurface.create_from_png(TestUtils.BLUR_INPUT)
        backend.set_image_size(test_img_surface.get_width(), test_img_surface.get_height())
        backend.set_margin(0, 0, 0, 0)
        backend.push_surface()
        backend.ctx().set_source_surface(test_img_surface)
        backend.ctx().paint()
        backend.blur_surface()
        backend.export_to_file(TestUtils.BLUR_GENERATED_IMAGE)
        assert TestUtils.imagesEqual(TestUtils.BLUR_GENERATED_IMAGE, TestUtils.BLUR_EXPECTED_IMAGE)

    def test_push_surface(self):
        backend = CairoBackend()
        assert len(backend.surfaces()) == 0
        backend.push_surface()
        previous_surface = backend.surfaces()[-1]
        for i in range(0, 10):
            backend.push_surface()
            assert previous_surface == backend.surfaces()[-2]
            assert len(backend.surfaces()) == i + 2
            previous_surface = backend.surfaces()[-1]

    def test_pop_surface(self):
        backend = CairoBackend()
        assert len(backend.surfaces()) == 0
        for i in range(0, 10):
            backend.push_surface()
        for i in range(10, 0):
            backend.pop_surface()
            assert len(backend.surfaces()) == i

    def test_set_image_size(self):
        backend = CairoBackend()
        backend.set_image_size(200, 300)
        assert backend.image_size() == (200, 300)

    def test_create_canvas(self):
        backend = CairoBackend()
        backend.create_canvas()
        backend.export_to_file(TestUtils.EMPTY_CANVAS_GENERATED_IMAGE)
        assert TestUtils.imagesEqual(TestUtils.EMPTY_CANVAS_GENERATED_IMAGE, TestUtils.EMPTY_CANVAS_EXPECTED_IMAGE)
        
        
        
