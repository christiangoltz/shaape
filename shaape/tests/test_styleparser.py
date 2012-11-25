from shaape.styleparser import StyleParser
from shaape.style import Style
from shaape.polygon import Polygon
from shaape.opengraph import OpenGraph
from shaape.arrow import Arrow
from shaape.node import Node
from shaape.background import Background
import nose
import unittest
from nose.tools import *

class TestStyleParser(unittest.TestCase):

    def test_init(self):
        parser = StyleParser()
        assert parser != None

    def test_run(self):
        parser = StyleParser()
        arrow_style = Style(['_default_'], 'arrow', ['red'])
        fill_style = Style(['_default_'], 'fill', ['blue'])
        line_style = Style(['_default_'], 'line', ['green'])
        frame_style = Style(['_default_'], 'frame', [[0.1, 0.2, 0.3]])
        custom_fill_style = Style(['abc', 'def'], 'fill', [[0.3, 0.2, 0.3]])
        custom_line_style = Style(['abc', 'def'], 'line', [[0.4, 0.3, 0.3]])
        custom_frame_style = Style(['abc', 'def'], 'frame', [[0.5, 0.2, 0.3]])
        polygon1 = Polygon([Node(0, 0)])
        opengraph1 = OpenGraph()
        opengraph2 = OpenGraph()
        opengraph2.add_name('abc')
        arrow = Arrow()
        background = Background()
        polygon2 = Polygon([Node(0, 0)])
        polygon2.add_name('abc')
        polygon3 = Polygon([Node(0, 0)])
        polygon3.add_name('def')
        
        objects = [arrow_style, fill_style, line_style, frame_style, custom_fill_style, custom_line_style, custom_frame_style, polygon1, polygon2, polygon3, opengraph1, opengraph2, arrow, background]
        parser.run([], objects)
        assert arrow.style().color() == arrow_style.color()
        assert polygon1.style().color() == fill_style.color()
        assert polygon1.frame().style().color() == frame_style.color()
        assert opengraph1.style().color() == line_style.color()
        assert opengraph2.style().color() == custom_line_style.color()
        assert polygon2.style().color() == custom_fill_style.color()
        assert polygon3.style().color() == custom_fill_style.color()
        assert polygon2.frame().style().color() == custom_frame_style.color()
        assert polygon3.frame().style().color() == custom_frame_style.color()

