from shaape.node import Node
import nose
import unittest

class TestNode(unittest.TestCase):
    def test_init(self):
        node = Node(3.2, 5.0)
        assert node.position() == (3.2, 5.0)

