from shaape.text import Text
import nose
import unittest
from nose.tools import *

class TestText(unittest.TestCase):

    def test_init(self):
        text = Text()
        assert text != None

    def test_text(self):
        text = Text("123456asdf")
        assert text.text() == "123456asdf"

    def test_font_size(self):
        text = Text()
        assert text.font_size() == 1

    def test_scale(self):
        text = Text()
        assert text.font_size() == 1
        text.scale((2, 2))
        assert text.font_size() == 2
        text.scale((3, 3))
        assert text.font_size() == 6

    def test_min_max(self):
        text = Text()
        assert text.min() == (0, 0)
        assert text.max() == (0, 0)
        text = Text(position = (5, -6))
        assert text.min() == (5, -6)
        assert text.max() == (5, -6)

