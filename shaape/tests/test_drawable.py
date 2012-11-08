from shaape.drawable import Drawable
from shaape.style import Style
import nose
import unittest
from nose.tools import *

class TestDrawable(unittest.TestCase):

    def test_init(self):
        drawable = Drawable()
        assert type(drawable.style()) == Style

    def test_style(self):
        drawable = Drawable()
        style = Style(['abc', 'def', 'geh'], 'line', ['flat', 'dotted', 'shadow'])
        drawable.set_style(style)
        assert drawable.style().options() == style.options()

    def test_min(self):
        drawable = Drawable()
        assert_raises(NotImplementedError, drawable.min)

    def test_max(self):
        drawable = Drawable()
        assert_raises(NotImplementedError, drawable.max)
