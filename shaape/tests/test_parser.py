from shaape.parser import Parser
import nose
import unittest
from nose.tools import *

class TestParser(unittest.TestCase):
    def test_init(self):
        parser = Parser()
        assert parser != None
        assert parser.parsed_data() == []
        assert parser.drawable_objects() == []

    def test_run(self):
        parser = Parser()
        assert_raises(NotImplementedError, parser.run, "", [])

