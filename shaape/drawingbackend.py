from drawable import *

class DrawingBackend(object):
    def __init__(self):
        self._canvas_size = [0, 0]
        self._scale = 1.2
        self.__pixels_per_unit = [10 * self._scale, 20 * self._scale]
        return

    def run(self, drawable_objects, filename):
        self.canvas_size = [0, 0]

        sortable_objects = filter(lambda x: isinstance(x, Drawable), drawable_objects)
        unsortable_objects = filter(lambda x: not isinstance(x, Drawable), drawable_objects)
        drawable_objects = sorted(sortable_objects, key=lambda x: x.min()) + unsortable_objects

        for drawable_object in drawable_objects:
            if isinstance(drawable_object, Scalable):
                drawable_object.scale(self.__pixels_per_unit)

        for drawable_object in drawable_objects:
            if isinstance(drawable_object, Background):
                self._canvas_size = drawable_object.size()
        
        self.create_canvas()
        self.__draw_objects(drawable_objects)
        self.export_to_file(filename)

    def __draw_objects(self, drawable_objects):
        self.push_surface()
        self.translate(4 * self._scale, 4 * self._scale)
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
