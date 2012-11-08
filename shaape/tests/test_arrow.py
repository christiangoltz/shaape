from shaape.arrow import Arrow
from shaape.style import Style
import nose
import unittest
from nose.tools import *

class TestArrow(unittest.TestCase):

    def test_init(self):
        arrow = Arrow((3, 1))
        assert type(arrow) == Arrow

    def test_scale(self):
        arrow1 = Arrow((1, 2))
        arrow2 = Arrow((1, 2))
        arrow1.scale((2.5, 1.2))
        assert arrow1.max()[0] == arrow2.max()[0] * 2.5
        assert arrow1.max()[1] == arrow2.max()[1] * 1.2
