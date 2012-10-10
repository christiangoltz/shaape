from ShaapeDrawable import *

class ShaapeDrawingBackend(object):
    def __init__(self):
        self._canvas_size = [0, 0]
        self.__pixels_per_unit = (10, 20)
        return

    def run(self, drawable_objects, filename):
        self.canvas_size = [0, 0]

        sortable_objects = filter(lambda x: isinstance(x, ShaapeDrawable), drawable_objects)
        unsortable_objects = filter(lambda x: not isinstance(x, ShaapeDrawable), drawable_objects)
        drawable_objects = sorted(sortable_objects, key=lambda x: x.min()) + unsortable_objects

        for drawable_object in drawable_objects:
            if isinstance(drawable_object, ShaapeScalable):
                drawable_object.scale(self.__pixels_per_unit)

        for drawable_object in drawable_objects:
            if isinstance(drawable_object, ShaapeBackground):
                self._canvas_size = drawable_object.size()
        
        self.create_canvas(filename)
        self.__draw_objects(drawable_objects)
        self.export_to_file(filename)

    def __draw_objects(self, drawable_objects):
        for drawable_object in drawable_objects:
            if isinstance(drawable_object, ShaapePolygon):
                self.draw_polygon_shadow(drawable_object)
        for drawable_object in drawable_objects:
            if isinstance(drawable_object, ShaapeOpenGraph):
                self.draw_open_graph_shadow(drawable_object)
        for drawable_object in drawable_objects:
            if isinstance(drawable_object, ShaapePolygon) and not isinstance(drawable_object, ShaapeArrow):
                self.draw_polygon(drawable_object)
                self.draw_open_graph(drawable_object.frame())
        for drawable_object in drawable_objects:
            if isinstance(drawable_object, ShaapeOpenGraph):
                self.draw_open_graph(drawable_object)
        for drawable_object in drawable_objects:
            if isinstance(drawable_object, ShaapeArrow):
                self.draw_polygon(drawable_object)
                self.draw_open_graph(drawable_object.frame())
        for drawable_object in drawable_objects:
            if isinstance(drawable_object, ShaapeText):
                self.draw_text(drawable_object)
        return
