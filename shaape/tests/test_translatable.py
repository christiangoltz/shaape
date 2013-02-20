from shaape.translatable import Translatable
import nose
import unittest
from nose.tools import *

class TestTranslatable(unittest.TestCase):
    def test_init(self):
        translatable = Translatable()
        assert translatable != None

    def test_position(self):
        translatable = Translatable()
        assert translatable.position() == (0, 0)
        translatable = Translatable((-4, 5))
        assert translatable.position() == (-4, 5)
        translatable.set_position((16, -1))
        assert translatable.position() == (16, -1)

    def test_scale(self):
        translatable = Translatable((2, -3))
        assert translatable.position() == (2, -3)
        translatable.scale((5.5, 2.3))
        assert translatable.position() == (2 * 5.5, -3 * 2.3)
