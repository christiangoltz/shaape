from shaape.background import Background
import nose
import unittest
from nose.tools import *

class TestBackground(unittest.TestCase):
    def test_init(self):
        background = Background((10, 20))
        assert type(background) == Background

    def test_size(self):
        background = Background((50, 60))
        assert background.size() == (50, 60)

    def test_scale(self):
        background = Background((50, 60))
        background.scale((5.5, 2.3))
        assert background.size() == (50 * 5.5, 60 * 2.3)

    def test_min(self):
        background = Background((50, 60))
        assert background.min() == (0, 0)

    def test_maxn(self):
        background = Background((50, 60))
        assert background.max() == (50, 60)
