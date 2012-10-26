from shaape.drawingbackend import DrawingBackend
import nose
import unittest

class TestDrawingBackend(unittest.TestCase):
    def test_init(self):
        backend = DrawingBackend()

