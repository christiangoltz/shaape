from drawable import Drawable
from polygon import Polygon
from opengraph import OpenGraph
from scalable import Scalable
from background import Background
from arrow import Arrow
from text import Text

class DrawingBackend(object):

    DEFAULT_SCALE = 1
    DEFAULT_PIXELS_PER_UNIT = 20
    DEFAULT_SHADOW_TRANSLATION = (2, 2)

    def __init__(self, image_scale = DEFAULT_SCALE, image_width = None, image_height = None):
        self.__user_canvas_size = [image_width, image_height] 
        self._canvas_size = [image_width, image_height]
        if image_width:
            self._canvas_size[0] = self._canvas_size[0] * image_scale
        if image_height:
            self._canvas_size[1] = self._canvas_size[1] * image_scale
        self._scale = image_scale
        self.__aspect_ratio = 0.5
        self.__pixels_per_unit = (self.DEFAULT_PIXELS_PER_UNIT * self._scale * self.__aspect_ratio, self.DEFAULT_PIXELS_PER_UNIT * self._scale)
        self.__global_scale = (self.DEFAULT_PIXELS_PER_UNIT * self._scale * self.__aspect_ratio, self.DEFAULT_PIXELS_PER_UNIT * self._scale)
        return

    def scale(self):
        return self._scale

    def shadow_translation(self): 
        return (DrawingBackend.DEFAULT_SHADOW_TRANSLATION[0] * self.scale(), DrawingBackend.DEFAULT_SHADOW_TRANSLATION[1] * self.scale())

    def set_canvas_size(self, width, height):
        if not self.__user_canvas_size[0]:
            self._canvas_size[0] = width * self._scale
        if not self.__user_canvas_size[1]:
            self._canvas_size[1] = height * self._scale

    def canvas_size(self):
        return self._canvas_size

    def unit_size(self):
        return self.__pixels_per_unitself.__global_scale

    def run(self, drawable_objects, filename):
        sortable = lambda x: isinstance(x, Drawable)
        sortable_objects = filter(lambda x: sortable(x), drawable_objects)
        unsortable_objects = filter(lambda x: not sortable(x), drawable_objects)
        drawable_objects = sorted(sortable_objects, key=lambda x: x.min()) + unsortable_objects

        for drawable_object in drawable_objects:
            if isinstance(drawable_object, Background):
                if not self.__user_canvas_size[0]:
                    if self.__user_canvas_size[1]:
                        scale = self.__user_canvas_size[1] / drawable_object.size()[1] * self.__aspect_ratio
                    else:
                        scale = self.__pixels_per_unit[0]
                    self._canvas_size[0] = drawable_object.size()[0] * scale
                if not self.__user_canvas_size[1]:
                    if self.__user_canvas_size[0]:
                        scale = self.__user_canvas_size[0] / drawable_object.size()[0] / self.__aspect_ratio
                    else:
                        scale = self.__pixels_per_unit[1]
                    self._canvas_size[1] = drawable_object.size()[1] * scale
                self.__global_scale = [self._canvas_size[0] / drawable_object.size()[0], self._canvas_size[1] / drawable_object.size()[1]]
                self._scale = self.__global_scale[0] / (self.DEFAULT_PIXELS_PER_UNIT * self.__aspect_ratio)
        
        for drawable_object in drawable_objects:
            if isinstance(drawable_object, Scalable):
                drawable_object.scale(self.__global_scale)

        self.create_canvas()
        self.draw_objects(drawable_objects)
        self.export_to_file(filename)

    def global_scale(self):
        return self.__global_scale

    def draw_polygon_shadow(self, obj):
        raise NotImplementedError

    def draw_polygon(self, obj):
        raise NotImplementedError

    def draw_open_graph(self, obj):
        raise NotImplementedError

    def draw_open_graph_shadow(self, obj):
        raise NotImplementedError

    def draw_text(self, obj):
        raise NotImplementedError

    def draw_text_shadow(self,obj):
        raise NotImplementedError

    def push_surface(self):
        raise NotImplementedError

    def pop_surface(self):
        raise NotImplementedError

    def translate(self, x, y):
        raise NotImplementedError

    def blur_surface(self):
        raise NotImplementedError

    def draw_objects(self, drawable_objects):
        objects = [o for o in drawable_objects if isinstance(o, Drawable)]
        if objects:
            max_depth = max(objects, key=lambda o: o.z_order()).z_order()
            objects_lists_per_depth = [[] for x in xrange(max_depth + 1)]
        else:
            objects_lists_per_depth = []

        for o in objects:
           objects_lists_per_depth[o.z_order()].append(o) 
        i = 0
        for obj_list in objects_lists_per_depth:
            polygons = filter(lambda d: isinstance(d, Polygon) and not isinstance(d, Arrow), obj_list)
            text = filter(lambda d: isinstance(d, Text), obj_list)
            arrows = filter(lambda d: isinstance(d, Arrow), obj_list)
            graphs = filter(lambda d: isinstance(d, OpenGraph), obj_list)

            self.push_surface()
            self.translate(*self.shadow_translation())
            for p in polygons:
                if p.style().shadow() == 'on':
                    self.draw_polygon_shadow(p)
            for drawable_object in graphs:
                if drawable_object.style().shadow() == 'on':
                    self.draw_open_graph_shadow(drawable_object)
            for drawable_object in text:
                if drawable_object.style().shadow() == 'on':
                    self.draw_text_shadow(drawable_object)
            self.blur_surface()
            self.pop_surface()
            self.push_surface()
            for p in polygons:
                self.draw_polygon(p)
            self.pop_surface()
            self.push_surface()
            for p in polygons:
                    self.draw_open_graph(p.frame())
            self.pop_surface()
            i = i + 1

            self.push_surface()
            for drawable_object in graphs:
                self.draw_open_graph(drawable_object)
            self.pop_surface()

            self.push_surface()
            self.translate(*self.shadow_translation())
            for drawable_object in arrows:
                if drawable_object.style().shadow() == 'on':
                    self.draw_polygon_shadow(drawable_object)
            self.blur_surface()
            self.pop_surface()
            self.push_surface()
            for drawable_object in arrows:
                self.draw_polygon(drawable_object)
            self.pop_surface()

            self.push_surface()
            for drawable_object in text:
                self.draw_text(drawable_object)
            self.pop_surface()
        return
