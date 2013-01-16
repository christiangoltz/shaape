from shaape.nameparser import NameParser
from shaape.text import Text
from shaape.tests.utils import TestUtils
import nose
import unittest
from nose.tools import *

class TestNameParser(unittest.TestCase):

    def test_init(self):
        parser = NameParser()
        assert parser != None

    def test_run(self):
        parser = NameParser()
        polygon = TestUtils.generate_test_polygon(seed = 0, points = 10, radius_range = (9, 10))
        text1 = Text("abc")
        text2 = Text("def", (20, 0))
        raw_data = '123'
        objects = [polygon, text1, text2]
        parser.run(raw_data, objects)
        assert polygon.names() == ['', 'abc']

        
