from shaape.backgroundparser import BackgroundParser
from shaape.drawable import Background
import nose
import unittest
from nose.tools import *

class TestBackroundParser(unittest.TestCase):
    def test_init(self):
        backgroundparser = BackgroundParser()
        assert backgroundparser.parsed_data() == []
        assert backgroundparser.drawable_objects() == []

    def test_run(self):
        backgroundparser = BackgroundParser()
        data = ['----------'] * 10 + ['-----\n'] * 10
        objects = []
        backgroundparser.run(data, objects)
        assert len(backgroundparser.parsed_data()) == 20
        assert backgroundparser.drawable_objects() == objects
        assert len(objects) == 1
        assert type(objects[0]) == Background
        print(objects[0].size())
        assert objects[0].size() == (10, 20)
        for line in backgroundparser.parsed_data():
            assert line[-1] == '\n'

