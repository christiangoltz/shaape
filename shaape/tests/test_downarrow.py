from shaape.downarrow import DownArrow
import nose
import unittest
from nose.tools import *

class TestDownArrow(unittest.TestCase):
    def test_init(self):
        arrow = DownArrow()
        assert arrow != None
