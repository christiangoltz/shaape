from shaape.drawingbackend import DrawingBackend
import nose

class TestDrawingBackend(unittest.TestCase):
    def test_init(self):
        backend = DrawingBackend()
        assert_equal(backend.canvas_size(), DrawingBackend.DEFAULT_CANVAS_SIZE)
        assert_equal(backend.pixels_per_unit(), DrawingBackend.DEFAULT_PIXELS_PER_UNIT)

