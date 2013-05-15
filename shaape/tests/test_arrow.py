from shaape.arrow import Arrow
from shaape.style import Style
import nose
import unittest
from nose.tools import *

class TestArrow(unittest.TestCase):

    def test_init(self):
        arrow = Arrow((3, 1))
        assert type(arrow) == Arrow

    def test_direction(self):
        arrow = Arrow()
        assert_raises(NotImplementedError, arrow.direction) 
