from shaape.named import Named
import nose
import unittest
from nose.tools import *

class TestNamed(unittest.TestCase):

    def test_init(self):
        named = Named()
        assert named != None

    def test_add_name(self):
        named = Named()
        assert named.names() == ['']
        named.add_name("abc")
        assert "abc" in named.names()
        assert len(named.names()) == 2
        named.add_name("def")
        assert "abc" in named.names()
        assert "def" in named.names()
        assert len(named.names()) == 3

