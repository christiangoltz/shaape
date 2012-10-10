import cairo
import os
import math

from ShaapeDrawingBackend import ShaapeDrawingBackend
from ShaapeDrawable import *

class ShaapeCairoBackend(ShaapeDrawingBackend):
    
    def __init__(self):
        super(ShaapeCairoBackend, self).__init__()
        self.margin = [10, 10, 10, 10]
        
        return

    def create_canvas(self, filename):
        self.image_size = (self._canvas_size[0], self._canvas_size[1])
        if os.path.splitext(filename)[1] <> '.svg':
            filename = None
        self.surface = cairo.SVGSurface (filename, self.image_size[0] + self.margin[0] + self.margin[1], self._canvas_size[1] + self.margin[2] + self.margin[3])
        self.ctx = cairo.Context (self.surface)

        # self.ctx.set_source_rgb(1, 1, 1)
        # self.ctx.rectangle(0.0, 0.0, self.image_size[0] + self.margin[0] + self.margin[1], self.image_size[1] + self.margin[2] + self.margin[3])
        # self.ctx.fill()

        self.ctx.translate(self.margin[0], self.margin[2])
        # self.ctx.scale(20,20)
        return
    def apply_line(self, drawable):
        self.ctx.set_line_cap(cairo.LINE_CAP_BUTT)
        self.ctx.set_line_join (cairo.LINE_JOIN_ROUND)
        width =  drawable.style().width()
        if len(drawable.style().color()) == 3:
            self.ctx.set_source_rgb(*(drawable.style().color()))
        else:
            self.ctx.set_source_rgba(*(drawable.style().color()))
        self.ctx.set_line_width(width)
        return

    def apply_fill(self, drawable):
        minimum = drawable.min()
        maximum = drawable.max()
        color =  drawable.style().color()
        if drawable.style().fill_type() == 'gradient':
            linear_gradient = cairo.LinearGradient(minimum[0], minimum[1], maximum[0], maximum[1])
            if len(color) == 4:
                linear_gradient.add_color_stop_rgba(0, 1,1,1,color[3])
                color = map(lambda x: 0.6 * x, color[0:3]) + [color[3]]
                linear_gradient.add_color_stop_rgba(1, *color)
            elif len(color) == 3:
                linear_gradient.add_color_stop_rgb(0, 1,1,1)
                color = map(lambda x: 0.6 * x, color[0:3])
                linear_gradient.add_color_stop_rgb(1, *color)
            self.ctx.set_source(linear_gradient)
        else:
            if len(color) == 4:
                self.ctx.set_source_rgba(*color)
            elif len(color) == 3:
                self.ctx.set_source_rgb(*color)
    
    def draw_polygon(self, polygon):
        # draw fill
        self.ctx.save()
        self.apply_fill(polygon)
            
        self.apply_transform(polygon)

        node = polygon.nodes()[0]
        self.ctx.move_to(node[0], node[1])
        for node in polygon.nodes():
            self.ctx.line_to(node[0], node[1])
        self.ctx.close_path()
        self.ctx.fill()
        self.ctx.restore()
        return

    def draw_polygon_shadow(self, polygon):
        # draw shadow
        self.ctx.save()
        if polygon.style().shadow() == 'on':
            node = polygon.nodes()[0]
            self.ctx.set_source_rgba(0.0, 0.0, 0.0, 0.1)
            for i in range(0, 6):
                self.ctx.save()
                self.ctx.translate(1 * i, 1 * i)
                self.apply_transform(polygon)
                self.ctx.move_to(node[0], node[1])
                for node in polygon.nodes():
                    self.ctx.line_to(node[0], node[1])
                self.ctx.close_path()
                self.ctx.fill()
                self.ctx.restore()

        self.ctx.restore()
        return

    def draw_open_graph_shadow(self, open_graph):
        if open_graph.style().shadow() == 'on':
            self.apply_line(open_graph)
            self.ctx.set_source_rgba(0, 0, 0, 0.1)
            for i in range(0,6):
                self.ctx.save()
                self.ctx.translate(1 * i, 1 * i)
                self.apply_transform(open_graph)
                graph = open_graph.graph()
                for edge in graph.edges():
                    self.ctx.move_to(edge[0][0], edge[0][1])
                    self.ctx.line_to(edge[1][0], edge[1][1])
                self.ctx.stroke()
                self.ctx.restore()
        return


    def draw_open_graph(self, open_graph):

        self.apply_line(open_graph)
        self.ctx.save()
        self.apply_transform(open_graph)
        graph = open_graph.graph()
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
            self.ctx.move_to(text_obj.position()[0] + cx * (text_obj.font_size()), text_obj.position()[1] + text_obj.font_size() - fdescent + fheight / 2)
            self.ctx.show_text(letter)
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
        if os.path.splitext(filename)[1] == '.png':
            self.surface.write_to_png(filename)
        elif os.path.splitext(filename)[1] == '.svg':
            pass
        return

    def start_object(self):
        self.ctx.save()
        return

    def end_object(self):
        self.ctx.restore()
