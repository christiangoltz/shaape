from shaape.rightarrow import RightArrow
import nose
import unittest
from nose.tools import *

class TestRightArrow(unittest.TestCase):
    def test_init(self):
        arrow = RightArrow()
        assert arrow != None
        arrow = RightArrow((3, -1))
        assert arrow.position() == (3, -1)
