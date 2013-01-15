from shaape.textparser import TextParser
import nose
import unittest
from nose.tools import *

class TestTextParser(unittest.TestCase):
    def test_init(self):
        textparser = TextParser()
        assert textparser.parsed_data() == []
        assert textparser.drawable_objects() == []

    def test_run(self):
        textparser = TextParser()
        data = ['abc a 12345 \'b\'']
        objects = []
        textparser.run(data, objects)
        assert textparser.parsed_data() == data
        assert textparser.drawable_objects() == objects
        assert len(objects) == 3
        assert [o for o in objects if o.text() == 'abc']
        assert [o for o in objects if o.text() == '12345']
        assert [o for o in objects if o.text() == 'b']
        
