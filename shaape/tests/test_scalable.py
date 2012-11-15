from shaape.scalable import Scalable
import nose
import unittest
from nose.tools import *

class TestScalable(unittest.TestCase):
    def test_init(self):
        scalable = Scalable()
        assert scalable != None

    def test_scale(self):
        scalable = Scalable()
        assert_raises(NotImplementedError, scalable.scale, (1, 2))
