from shaape.cairobackend import CairoBackend
from shaape.tests.utils import TestUtils
from shaape.shaape import Shaape
import nose
import unittest
from nose.tools import *

class TestCairoBackend(unittest.TestCase):
    def test_init(self):
        backend = CairoBackend()
        assert backend != None

    def test_blur_surface(self):
        main = Shaape(TestUtils.BLUR_INPUT, TestUtils.BLUR_GENERATED_IMAGE)
        main.run()
        assert TestUtils.imagesEqual(TestUtils.BLUR_GENERATED_IMAGE, TestUtils.BLUR_EXPECTED_IMAGE)
