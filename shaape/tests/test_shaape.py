from shaape.shaape import Shaape
from shaape.shaape import main as shaape_main
from shaape.overlayparser import OverlayParser
from shaape.cairobackend import CairoBackend
import nose
import unittest
from nose.tools import *
from shaape.tests.utils import *
import copy
import sys
from mock import MagicMock
import runpy

class TestShaape(unittest.TestCase):
    def test_init(self):
        shaape = Shaape(TestUtils.EMPTY_INPUT)
        assert shaape != None
        sys.stdin = MagicMock()
        sys.stdin.read = MagicMock(returns = "")
        shaape = Shaape()
        assert shaape != None

    def test_register_parser(self):
        shaape = Shaape(TestUtils.EMPTY_INPUT)
        original_parsers = copy.copy(shaape.parsers())
        overlayparser = OverlayParser()
        shaape.register_parser(overlayparser)
        assert shaape.parsers() == original_parsers + [overlayparser]
        assert_raises(TypeError, shaape.register_parser, CairoBackend())

    def test_register_backend(self):
        shaape = Shaape(TestUtils.EMPTY_INPUT)
        original_backends = copy.copy(shaape.backends())
        cairobackend = CairoBackend()
        shaape.register_backend(cairobackend)
        assert shaape.backends() == original_backends + [cairobackend]
        assert_raises(TypeError, shaape.register_backend, OverlayParser())

    def test_run(self):
        shaape = Shaape(TestUtils.EMPTY_INPUT)
        for parser in shaape.parsers():
            parser.run = MagicMock()
        for backend in shaape.backends():
            backend.run = MagicMock()
        shaape.run()
        for parser in shaape.parsers():
            parser.run.assert_called_once()
        for backend in shaape.backends():
            backend.run.assert_called_once()
         
    def test_main(self):
        shaape_main([TestUtils.EMPTY_INPUT])
        shaape_main(['-o',TestUtils.EMPTY_OUTPUT, TestUtils.EMPTY_INPUT])
