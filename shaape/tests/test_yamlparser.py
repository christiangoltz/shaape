from shaape.yamlparser import YamlParser
import nose
import unittest
from nose.tools import *

class TestYamlParser(unittest.TestCase):
    def test_init(self):
        yamlparser = YamlParser()
        assert yamlparser.parsed_data() == []
        assert yamlparser.drawable_objects() == []

    def test_run(self):
        yamlparser = YamlParser()
        data = ['options:',
                '(flat)|(top): {fill:[[1, 0.7, 0, 0.3], no-shadow, flat], frame:[[0.3, 0.8, 0], dotted, 3]}'
                ]
        objects = []
        yamlparser.run(data, objects)
        assert yamlparser.parsed_data() == []
        assert yamlparser.drawable_objects() == objects
        assert len(objects) == 2
        assert [o for o in objects if o.target_type() == 'frame' and o.width() == 3 and o.fill_type() == 'dotted' and o.color() == [0.3, 0.8, 0] and o.name_pattern() == '(flat)|(top)']
        assert [o for o in objects if o.target_type() == 'fill' and o.shadow() == 'off' and o.fill_type() == 'flat' and o.color() == [1, 0.7, 0, 0.3] and o.name_pattern() == '(flat)|(top)']
