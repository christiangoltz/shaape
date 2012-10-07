from ShaapeDrawable import *

class ShaapeDrawingBackend(object):
    def __init__(self):
        self._canvas_size = [0, 0]
        self.__pixels_per_unit = (10, 20)
        return

    def run(self, drawable_objects, filename):
        self.canvas_size = [0, 0]

        for drawable_object in drawable_objects:
            drawable_object.scale(self.__pixels_per_unit)

        for drawable_object in drawable_objects:
            if isinstance(drawable_object, ShaapeBackground):
                self._canvas_size = drawable_object.size()
        
        self.create_canvas()
        for drawable_object in drawable_objects:
            if isinstance(drawable_object, ShaapePolygon):
                self.draw_polygon(drawable_object)
                self.draw_frame(drawable_object)
            if isinstance(drawable_object, ShaapeOpenGraph):
                self.draw_open_graph(drawable_object)
        for drawable_object in drawable_objects:
            if isinstance(drawable_object, ShaapeText):
                self.draw_text(drawable_object)

        self.export_to_file(filename)
        return
