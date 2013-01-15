from shaape.leftarrow import LeftArrow
import nose
import unittest
from nose.tools import *

class TestLeftArrow(unittest.TestCase):
    def test_init(self):
        arrow = LeftArrow()
        assert arrow != None
        arrow = LeftArrow((3, -1))
        assert arrow.position() == (3, -1)
