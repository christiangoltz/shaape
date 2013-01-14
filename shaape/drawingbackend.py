from drawable import Drawable
from polygon import Polygon
from opengraph import OpenGraph
from scalable import Scalable
from background import Background
from arrow import Arrow
from text import Text

class DrawingBackend(object):

    DEFAULT_SCALE = 1.2
    DEFAULT_CANVAS_SIZE = (0, 0)
    DEFAULT_SHADOW_TRANSLATION = (1, 1)

    def __init__(self):
        self._canvas_size = DrawingBackend.DEFAULT_CANVAS_SIZE
        self._scale = DrawingBackend.DEFAULT_SCALE
        self.__pixels_per_unit = (10 * self._scale, 20 * self._scale)
        return

    def scale(self):
        return self._scale

    def shadow_translation(self):
        return (DrawingBackend.DEFAULT_SHADOW_TRANSLATION[0] * self.scale(), DrawingBackend.DEFAULT_SHADOW_TRANSLATION[1] * self.scale())

    def set_canvas_size(self, width, height):
        self._canvas_size = (width, height)

    def canvas_size(self):
        return self._canvas_size

    def unit_size(self):
        return self.__pixels_per_unit

    def run(self, drawable_objects, filename):
        sortable = lambda x: isinstance(x, Drawable)
        sortable_objects = filter(lambda x: sortable(x), drawable_objects)
        unsortable_objects = filter(lambda x: not sortable(x), drawable_objects)
        drawable_objects = sorted(sortable_objects, key=lambda x: x.min()) + unsortable_objects

        for drawable_object in drawable_objects:
            if isinstance(drawable_object, Scalable):
                drawable_object.scale(self.__pixels_per_unit)

        for drawable_object in drawable_objects:
            if isinstance(drawable_object, Background):
                self._canvas_size = drawable_object.size()
        
        self.create_canvas()
        self.draw_objects(drawable_objects)
        self.export_to_file(filename)

    def draw_polygon_shadow(self):
        raise NotImplementedError

    def draw_polygon(self):
        raise NotImplementedError

    def draw_open_graph(self):
        raise NotImplementedError

    def draw_open_graph_shadow(self):
        raise NotImplementedError

    def draw_text(self):
        raise NotImplementedError

    def push_surface(self):
        raise NotImplementedError

    def pop_surface(self):
        raise NotImplementedError

    def translate(self):
        raise NotImplementedError

    def blur_surface(self):
        raise NotImplementedError

    def draw_objects(self, drawable_objects):
        self.push_surface()
        self.translate(*self.shadow_translation())
        for drawable_object in drawable_objects:
            if isinstance(drawable_object, Polygon):
                if drawable_object.style().shadow() == 'on':
                    self.draw_polygon_shadow(drawable_object)
        for drawable_object in drawable_objects:
            if isinstance(drawable_object, OpenGraph):
                if drawable_object.style().shadow() == 'on':
                    self.draw_open_graph_shadow(drawable_object)
        self.blur_surface()
        self.pop_surface()
        self.push_surface()
        for drawable_object in drawable_objects:
            if isinstance(drawable_object, Polygon) and not isinstance(drawable_object, Arrow):
                self.draw_polygon(drawable_object)
        self.pop_surface()
        self.push_surface()
        for drawable_object in drawable_objects:
            if isinstance(drawable_object, Polygon) and not isinstance(drawable_object, Arrow):
                self.draw_open_graph(drawable_object.frame())
        self.pop_surface()
        self.push_surface()
        for drawable_object in drawable_objects:
            if isinstance(drawable_object, OpenGraph):
                self.draw_open_graph(drawable_object)
        self.pop_surface()
        self.push_surface()
        for drawable_object in drawable_objects:
            if isinstance(drawable_object, Arrow):
                self.draw_polygon(drawable_object)
#                self.draw_open_graph(drawable_object.frame())
        self.pop_surface()
        self.push_surface()
        for drawable_object in drawable_objects:
            if isinstance(drawable_object, Text):
                self.draw_text(drawable_object)
        self.pop_surface()
        return
