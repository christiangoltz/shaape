from shaape.rotatable import Rotatable
import nose
import unittest
from nose.tools import *
from shaape.tests.utils import TestUtils

class TestRotatable(unittest.TestCase):
    def test_init(self):
        rotatable = Rotatable()
        assert rotatable != None
        assert rotatable.angle() == 0

    def test_angle(self):
        rotatable = Rotatable()
        rotatable.set_angle(46)
        assert rotatable.angle() == 46
        rotatable.set_angle(-170)
        assert rotatable.angle() == -170
