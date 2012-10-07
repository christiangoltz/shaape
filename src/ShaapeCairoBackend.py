import cairo
import math

from ShaapeDrawingBackend import ShaapeDrawingBackend
from ShaapeDrawable import *

class ShaapeCairoBackend(ShaapeDrawingBackend):
    
    def __init__(self):
        super(ShaapeCairoBackend, self).__init__()
        self.margin = [10, 10, 10, 10]
        
        return

    def create_canvas(self):
        self.image_size = (self._canvas_size[0], self._canvas_size[1])
        self.surface = cairo.ImageSurface (cairo.FORMAT_ARGB32, self.image_size[0] + self.margin[0] + self.margin[1], self._canvas_size[1] + self.margin[2] + self.margin[3])
        self.ctx = cairo.Context (self.surface)

        self.ctx.set_source_rgb(1, 1, 1)
        self.ctx.rectangle(0.0, 0.0, self.image_size[0] + self.margin[0] + self.margin[1], self.image_size[1] + self.margin[2] + self.margin[3])
        self.ctx.fill()

        self.ctx.translate(self.margin[0], self.margin[2])
        # self.ctx.scale(20,20)
        return

    def draw_polygon(self, polygon):

        # draw shadow
        node = polygon.get_nodes()[0]
        self.ctx.set_source_rgba(0.0, 0.0, 0.0, 0.1)
        for i in range(0, 6):
            self.ctx.save()
            self.ctx.translate(1 * i, 1 * i)
            self.apply_transform(polygon)
            self.ctx.move_to(node[0], node[1])
            for node in polygon.get_nodes():
                self.ctx.line_to(node[0], node[1])
            self.ctx.close_path()
            self.ctx.fill()
            self.ctx.restore()

        # draw fill
        self.ctx.save()
        minimum = polygon.get_min()
        maximum = polygon.get_max()
        linear_gradient = cairo.LinearGradient(minimum[0], minimum[1], maximum[0], maximum[1])
        linear_gradient.add_color_stop_rgba(0.00,  0.9, 0.9, 0.9, 1)
        linear_gradient.add_color_stop_rgba(1.00,  0.6, 0.6, 0.6, 1)
        self.apply_transform(polygon)

        self.ctx.set_source(linear_gradient)
        node = polygon.get_nodes()[0]
        self.ctx.move_to(node[0], node[1])
        for node in polygon.get_nodes():
            self.ctx.line_to(node[0], node[1])
        self.ctx.close_path()
        self.ctx.fill()
        self.ctx.restore()
        return

    def draw_frame(self, polygon):
        self.ctx.save()
        self.apply_transform(polygon)
        self.ctx.set_source_rgb(0.0, 0.0, 0.0)
        self.ctx.set_line_width(0.1)
        node = polygon.get_nodes()[0]
        self.ctx.move_to(node[0], node[1])
        for node in polygon.get_nodes():
            self.ctx.line_to(node[0], node[1])
        self.ctx.close_path()
        self.ctx.restore()
        self.ctx.set_source_rgb(0.0, 0.0, 0.0)
        self.ctx.set_line_width(2)
        self.ctx.stroke()
        return

    def draw_open_graph(self, open_graph):
        self.ctx.set_line_width(2)
        self.ctx.set_source_rgba(0, 0, 0, 0.1)
        for i in range(0,6):
            self.ctx.save()
            self.ctx.translate(1 * i, 1 * i)
            self.apply_transform(open_graph)
            graph = open_graph.get_graph()
            for edge in graph.edges():
                self.ctx.move_to(edge[0][0], edge[0][1])
                self.ctx.line_to(edge[1][0], edge[1][1])
            self.ctx.stroke()
            self.ctx.restore()

        self.ctx.set_source_rgb(0, 0, 0)
        self.ctx.save()
        self.apply_transform(open_graph)
        graph = open_graph.get_graph()
        for edge in graph.edges():
            self.ctx.move_to(edge[0][0], edge[0][1])
            self.ctx.line_to(edge[1][0], edge[1][1])
        self.ctx.restore()
        self.ctx.stroke()
        return

    def draw_text(self, text_obj):
        text = text_obj.text()
        self.ctx.select_font_face("monospace", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        xbearing, ybearing, width, height, xadvance, yadvance = self.ctx.text_extents(text)
        self.ctx.save()
        # print(
        # self.apply_transform(text_obj)
        self.ctx.set_source_rgb(0.0, 0.0, 0.0)
        self.ctx.set_font_size(text_obj.font_size() / 0.8)
        fascent, fdescent, fheight, fxadvance, fyadvance = self.ctx.font_extents()
        # fheight = fheight * text_obj.font_size()
        # fdescent = fdescent * text_obj.font_size()
        for cx, letter in enumerate(text):
            xbearing, ybearing, width, height, xadvance, yadvance = (self.ctx.text_extents(letter))
            self.ctx.move_to(text_obj.position()[0] + cx * text_obj.font_size(), text_obj.position()[1] + text_obj.font_size() - fdescent + fheight / 2)
            self.ctx.show_text(letter)
        self.ctx.move_to(text_obj.position()[0], text_obj.position()[1])
        self.ctx.restore()
        # self.ctx.stroke()
        return

    def apply_transform(self, obj):
        if isinstance(obj, ShaapeTranslatable):
            self.ctx.translate(obj.position()[0], obj.position()[1])
        if isinstance(obj, ShaapeRotatable):
            self.ctx.rotate(math.radians(obj.get_angle()))

    def export_to_file(self, filename):
        # self.ctx.paint()
        self.surface.write_to_png(filename)
        return

    def start_object(self):
        self.ctx.save()
        return

    def end_object(self):
        self.ctx.restore()
