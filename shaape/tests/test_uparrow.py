from shaape.uparrow import UpArrow
import nose
import unittest
from nose.tools import *

class TestUpArrow(unittest.TestCase):
    def test_init(self):
        arrow = UpArrow()
        assert arrow != None
