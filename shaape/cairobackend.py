import cairo
import os
import errno
import math
from drawingbackend import DrawingBackend
import networkx as nx
from translatable import Translatable
from rotatable import Rotatable
from node import Node
import pangocairo
import pango
import warnings

class CairoBackend(DrawingBackend):
    DEFAULT_MARGIN = (10, 10, 10, 10)
    SHADOW_OPAQUENESS = 0.4
    def __init__(self, image_scale = 1.0, image_width = None, image_height = None):
        super(CairoBackend, self).__init__(image_scale, image_width, image_height)
        self.set_margin(*(CairoBackend.DEFAULT_MARGIN))
        self.set_image_size(0, 0)
        self.__surfaces = []
        self.__ctx = None
        self.__drawn_graph = None
        self.__font_map = pangocairo.cairo_font_map_get_default()
        self.__available_font_names = [f.get_name() for f in self.__font_map.list_families()]
        return

    def blur_surface(self):
        try:
            import numpy as np
            from scipy import ndimage

            blurred_surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, int(math.ceil(self.__image_size[0])), int(math.ceil(self.__image_size[1])))
            top_surface = self.__surfaces[-1]
            width = top_surface.get_width()
            height = top_surface.get_height()
            src = np.frombuffer(top_surface.get_data(), np.uint8)
            src.shape = (height, width, 4)
            dst = np.frombuffer(blurred_surface.get_data(), np.uint8)
            dst.shape = (height, width, 4)
            dst[:,:,3] = ndimage.gaussian_filter(src[:,:,3], sigma=3 * self.scale())
            dst[:,:,0] = ndimage.gaussian_filter(src[:,:,0], sigma=3 * self.scale())
            dst[:,:,1] = ndimage.gaussian_filter(src[:,:,1], sigma=3 * self.scale())
            dst[:,:,2] = ndimage.gaussian_filter(src[:,:,2], sigma=3 * self.scale())
            blurred_image = cairo.ImageSurface.create_for_data(dst, cairo.FORMAT_ARGB32, width, height)
            self.__ctx.set_source_surface(blurred_image)
            self.__ctx.set_operator(cairo.OPERATOR_SOURCE)
            self.__ctx.paint()
        except ImportError:
            pass

    def new_surface(self, name = None):
        return cairo.ImageSurface(cairo.FORMAT_ARGB32, int(math.ceil(self.image_size()[0])), int(math.ceil(self.image_size()[1])))

    def push_surface(self):
        surface = self.new_surface()
        self.__surfaces.append(surface)
        self.__ctx = cairo.Context(surface)
        self.__drawn_graph = nx.Graph()

    def pop_surface(self):
        surface = self.__surfaces.pop()
        self.__ctx = cairo.Context(self.__surfaces[-1])
        self.__ctx.set_source_surface(surface)
        self.__ctx.set_operator(cairo.OPERATOR_OVER)
        self.__ctx.paint()
        self.__drawn_graph = None

    def surfaces(self):
        return self.__surfaces

    def set_image_size(self, width, height):
        if not width:
            width = 1
        if not height:
            height = 1
        self.__image_size = (width, height)

    def image_size(self):
        return self.__image_size

    def set_margin(self, left, right, top, bottom):
        self.__margin = (left, right, top, bottom)

    def margin(self):
        return self.__margin

    def create_canvas(self):
        self.set_image_size(self._canvas_size[0], self._canvas_size[1])
        self.push_surface()
        self.__ctx.set_source_rgb(1, 1, 1)
        self.__ctx.rectangle(0.0, 0.0, self.__image_size[0] + self.__margin[0] + self.__margin[1], self.__image_size[1] + self.__margin[2] + self.__margin[3])
        return
    
    def apply_dash(self, drawable):
        if drawable.style().fill_type() == 'dashed':
            width = drawable.style().width() * self._scale
            dash_list = [ width * 4, width]
            self.__ctx.set_dash(dash_list)
        elif drawable.style().fill_type() == 'dotted':
            width = drawable.style().width() * self._scale
            dash_list = [width, width]
            self.__ctx.set_dash(dash_list)
        elif drawable.style().fill_type() == 'dash-dotted':
            width = drawable.style().width() * self._scale
            dash_list = [ width * 4, width, width, width]
            self.__ctx.set_dash(dash_list)
        else:
            self.__ctx.set_dash([])

    def apply_line(self, drawable, opaqueness = 1.0, shadow = False):
        self.__ctx.set_line_cap(cairo.LINE_CAP_BUTT)
        self.__ctx.set_line_join (cairo.LINE_JOIN_ROUND)
        width =  max(1, math.floor(drawable.style().width() * self._scale))
        color = drawable.style().color()[0]
        if len(color) == 3:
            color = tuple(color) + tuple([1])
        if shadow:
            color = map(lambda x: (1 - color[3]) * x, color[:3]) + [color[3]]
        adapted_color = tuple(color[:3]) + tuple([color[3] * opaqueness])
        self.__ctx.set_source_rgba(*adapted_color)
        self.apply_dash(drawable)
        self.__ctx.set_line_width(width)
        return

    def apply_fill(self, drawable, opaqueness = 1.0, shadow = False):
        minimum = drawable.min()
        maximum = drawable.max()
        colors =  drawable.style().color()
        if len(colors) > 1:
            linear_gradient = cairo.LinearGradient(minimum[0], minimum[1], maximum[0], maximum[1])
            n = 0
            for color in colors:
                stop = n * (1.0 / (len(colors) - 1))
                if len(color) == 3:
                    color = tuple(color) + tuple([1])
                if shadow:
                    color = map(lambda x: (1 - color[3]) * x, color[:3]) + [color[3]]
                adapted_color = tuple(color[:3]) + tuple([color[3] * opaqueness])
                linear_gradient.add_color_stop_rgba(stop, *adapted_color)
                n = n + 1
            self.__ctx.set_source(linear_gradient)
        else:
            color = colors[0]
            if len(color) == 3:
                color = tuple(color) + tuple([1])
            if shadow:
                color = map(lambda x: (1 - color[3]) * x, color[:3]) + [color[3]]
            adapted_color = tuple(color[:3]) + tuple([color[3] * opaqueness])
            self.__ctx.set_source_rgba(*adapted_color)
        self.__ctx.set_line_width(1)
    
    def draw_polygon(self, polygon):
        self.__ctx.save()
        self.apply_fill(polygon)
        self.apply_transform(polygon)
        nodes = polygon.nodes()
        self.apply_path(nodes)
        self.__ctx.fill()
        self.__ctx.restore()
        return

    def draw_polygon_shadow(self, polygon):
        self.__ctx.save()
        self.apply_fill(polygon, opaqueness = self.SHADOW_OPAQUENESS, shadow = True)
        self.__ctx.set_operator(cairo.OPERATOR_SOURCE)
        self.apply_transform(polygon)
        nodes = polygon.nodes()
        self.apply_path(nodes)
        self.__ctx.fill()
        self.__ctx.restore()
        return

    def draw_open_graph_shadow(self, open_graph):
        self.apply_line(open_graph, opaqueness = self.SHADOW_OPAQUENESS, shadow = True)
        self.__ctx.save()
        self.apply_transform(open_graph)
        self.__ctx.set_operator(cairo.OPERATOR_SOURCE)
        paths = open_graph.paths()
        if len(paths) > 0:
            for path in paths:
                if path[0] == path[-1]:
                    nodes = [path[-2]] + path 
                else:
                    nodes = [path[0]] + path + [path[-1]]
                self.apply_line(open_graph, opaqueness = self.SHADOW_OPAQUENESS, shadow = True)
                self.apply_path(nodes)
                self.__ctx.set_operator(cairo.OPERATOR_SOURCE)
                self.__ctx.stroke()
        self.__ctx.restore()
        return

    def _transform_to_sharp_space(self, direction, node):
        if self.__ctx.get_line_width() % 2 == 1:
            result = Node(node[0], node[1])
            if direction[0] == 0:
                result.set_position(result[0] + 0.5, result[1])
            if direction[1] == 0:
                result.set_position(result[0], result[1] + 0.5)
            return result
        else:
            return node


    def apply_path(self, nodes):
        cycle = (nodes[0] == nodes[-1])
        if cycle and nodes[0].style() == 'curve':
            line_end = nodes[1] + ((nodes[0] - nodes[1]) * 0.5)
        else: 
            line_end = nodes[0]
        self.__ctx.move_to(*self._transform_to_sharp_space(nodes[1] - nodes[0], line_end))
        for i in range(1, len(nodes)):
            if nodes[i].style() == 'curve':
                if i == len(nodes) - 1:
                    if cycle == True:
                        next_i = 1
                    else:
                        next_i = i
                else:
                    next_i = i + 1
                if i == len(nodes) - 1:
                    direction = nodes[next_i] - nodes[i]
                else:
                    direction = Node(0, 0)
                if i > 0 and nodes[i - 1].style() == 'miter':
                    temp_end = nodes[i - 1] + ((nodes[i] - nodes[i - 1]) * 0.5)
                    self.__ctx.line_to(*self._transform_to_sharp_space(Node(0, 0), temp_end))
                line_end = nodes[i] + ((nodes[next_i] - nodes[i]) * 0.5)
                cp1 = nodes[i - 1] + ((nodes[i] - nodes[i - 1]) * 0.97)
                cp2 = nodes[next_i] + ((nodes[i] - nodes[next_i]) * 0.97)
                cp1 = self._transform_to_sharp_space(direction, cp1)
                cp2 = self._transform_to_sharp_space(direction, cp2)
                self.__ctx.curve_to(cp1[0], cp1[1], cp2[0], cp2[1], *self._transform_to_sharp_space(direction, line_end))
            else:
                if i == len(nodes) - 1:
                    direction = nodes[i] - nodes[i - 1]
                else:
                    direction = Node(0, 0)
                self.__ctx.line_to(*self._transform_to_sharp_space(direction, nodes[i]))
                line_end = nodes[i]
        return

    def draw_open_graph(self, open_graph):
        self.__ctx.save()
        self.apply_transform(open_graph)
        paths = open_graph.paths()
        if len(paths) > 0:
            for path in paths:
                self.apply_line(open_graph)
                self.apply_path(path)
                self.__ctx.set_operator(cairo.OPERATOR_CLEAR)
                self.__ctx.set_dash([])
                self.__ctx.stroke_preserve()
                self.apply_line(open_graph)
                self.__ctx.set_operator(cairo.OPERATOR_SOURCE)
                self.__ctx.stroke()
        self.__ctx.restore()
        return

    def __draw_text(self, text_obj, shadow = False):
        text = text_obj.text()
        self.__ctx.save()
        pangocairo_context = pangocairo.CairoContext(self.__ctx)
        layout = pangocairo_context.create_layout()
        font = pango.FontDescription(text_obj.style().font().name())
        if not font.get_family() in self.__available_font_names:
            warnings.warn("Couldn't find font family for font name \"" + str(font.get_family()) + "\". Using default font. Available fonts are: " + str(self.__available_font_names), RuntimeWarning)

        font_size = font.get_size()

        if font_size == 0:
            font_size = 10 * pango.SCALE

        font.set_size(int(font_size * self._scale))
        layout.set_font_description(font)
        layout.set_text(text_obj.text())

        if shadow == True:
            self.apply_fill(text_obj, opaqueness = self.SHADOW_OPAQUENESS, shadow = True)
        else:
            self.apply_fill(text_obj, shadow = False)

        self.__ctx.translate(*(text_obj.position()))
            
        letter_width, letter_height = layout.get_pixel_size()
        unit_width, unit_height = self.global_scale()
        diff_height = (unit_height - letter_height) / 2
        diff_width = (unit_width - letter_width) / 2
        self.__ctx.translate(0, diff_height)
        for cx, letter in enumerate(text):
            layout.set_text(letter)
            letter_width, letter_height = layout.get_pixel_size()
            unit_width, unit_height = self.global_scale()
            diff_height = (unit_height - letter_height) / 2
            diff_width = (unit_width - letter_width) / 2
            self.__ctx.translate(diff_width, 0)
            fwidth, fheight = layout.get_pixel_size()
            pangocairo_context.update_layout(layout)
            pangocairo_context.layout_path(layout)
            self.__ctx.translate(-diff_width, 0)
            self.__ctx.translate(unit_width, 0)
        self.__ctx.fill()
        self.__ctx.restore()
        return

    
    def draw_text(self, text_obj):
        self.__draw_text(text_obj, shadow = False)

    def draw_text_shadow(self, text_obj):
        self.__draw_text(text_obj, shadow = True)

    def apply_transform(self, obj):
        if isinstance(obj, Translatable):
            self.__ctx.translate(obj.position()[0], obj.position()[1])
        if isinstance(obj, Rotatable):
            self.__ctx.rotate(math.radians(obj.angle()))
        return

    def export_to_file(self, filename):
        path = os.path.dirname(filename)
        if path != '':
            try:
                os.makedirs(path)
            except OSError as exception:
                if exception.errno != errno.EEXIST:
                    raise
        self.__surfaces[-1].write_to_png(filename)
        return

    def ctx(self):
        return self.__ctx

    def translate(self, x, y):
        self.ctx().translate(x, y)
