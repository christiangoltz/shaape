from shaape.node import Node
import nose
import unittest
from nose.tools import *

class TestNode(unittest.TestCase):
    @raises(ValueError)
    def test_init(self):
        node = Node(3.2, 5.0)
        assert node.position() == (3.2, 5.0)
        assert node.style() == 'miter'
        assert node.fusable() == True

        node = Node(3.2, 5.0, 'curve', False)
        assert node.position() == (3.2, 5.0)
        assert node.style() == 'curve'
        assert node.fusable() == False

        node = Node(3.2, 5.0, 'dummy', False)

    def test_position(self):
        node = Node(1.5, -0.5)
        assert node.position() == (1.5, -0.5)

    def test_fusable(self):
        node = Node(0, 0)
        assert node.fusable() == True
        
        node.set_fusable(False)
        assert node.fusable() == False

        node.set_fusable(True)
        assert node.fusable() == True

    def test_style(self):
        node = Node(0, 0, 'miter')
        assert node.style() == 'miter'
        
        node = Node(0, 0, 'curve')
        assert node.style() == 'curve'

    def test_get_item(self):
        node = Node(5.0, -1.7)
        assert node[0] == 5.0
        assert node[1] == -1.7
        
    @raises(IndexError)
    def test_get_item_exception_too_low(self):
        node = Node(5.0, -1.7)
        node[-1]

    @raises(IndexError)
    def test_get_item_exception_too_high(self):
        node = Node(5.0, -1.7)
        node[2]

    def test_add(self):
        node1 = Node(1.1, -3.0, 'curve', True)
        node2 = Node(-4.0, 9.1, 'miter', False)
        sum1 = node1 + node2
        sum2 = node2 + node1
        assert sum1.position() == (-2.9, 6.1)
        assert sum2.position() == sum1.position()
        assert sum1.style() == node1.style()
        assert sum1.fusable() == node1.fusable()
        assert sum2.style() == node2.style()
        assert sum2.fusable() == node2.fusable()

    def test_sub(self):
        node1 = Node(1.1, -3.0, 'curve', True)
        node2 = Node(-4.0, 9.2, 'miter', False)
        sum1 = node1 - node2
        sum2 = node2 - node1
        assert sum1.position() == (5.1, -12.2)
        assert sum2.position() == (-5.1, 12.2)
        assert sum1.style() == node1.style()
        assert sum1.fusable() == node1.fusable()
        assert sum2.style() == node2.style()
        assert sum2.fusable() == node2.fusable()
    
    @raises(NotImplementedError)
    def test_div(self):
        node = Node(5.5, -10.0, 'curve', True)
        quotient = node / 5
        assert quotient.position() == (1.1, -2.0)
        assert quotient.style() == node.style()
        assert quotient.fusable() == node.fusable()
        quotient = node / 'a'

    def test_mul(self):
        node = Node(1.1, -2.0, 'curve', True)
        product = node * 5
        assert product.position() == (5.5, -10.0)
        assert product.style() == node.style()
        assert product.fusable() == node.fusable()

        product = node * (2, 3)
        assert product.position() == (2.2, -6.0)
        assert product.style() == node.style()
        assert product.fusable() == node.fusable()

    def test_key_and_hash(self):
        node1 = Node(1.1, 2.2)
        node2 = Node(2.2, 1.1)
        node_dict = { node1 : 'node1', node2 : 'node2' }
        assert node_dict[node1] == 'node1'
        assert node_dict[node2] == 'node2'

    def test_cmp(self):
        node1 = Node(1.1, 2.2, 'miter', True)
        node2 = Node(2.2, 3.3, 'miter', True)
        node3 = Node(1.1, 2.2, 'curve', False)
        assert node1 != node2
        assert node1 < node2
        assert node2 > node1
        assert node1 == node3

    def test_repr(self):
        assert str(Node(1.1, 2.2, 'miter', True)) == "((1.1, 2.2),miter,True)"

    def test_length(self):
        node1 = Node(0, 0) 
        node2 = Node(3.0, 4.0) 
        assert node1.length() == 0
        assert node2.length() == 5
    
    def test_iter(self):
        node = Node(1.1, 2.2)
        i = 0
        for n in node:
            if i == 0:
                assert n == 1.1
            elif i == 1:
                assert n == 2.2
            i = i + 1

    def test_normalize(self):
        node1 = Node(2.0, 4.0) 
        node1.normalize()
        print(node1.length(), node1.length() == 1.0)
        assert node1.length() - 1.0 < 0.001

        node2 = Node(0.0, 0.0) 
        assert_raises(ArithmeticError, node2.normalize)
        
        
