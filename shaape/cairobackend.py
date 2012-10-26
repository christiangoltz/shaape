import cairo
import os
import math
import numpy as np
from scipy import ndimage

from drawingbackend import ShaapeDrawingBackend
from drawable import *

class ShaapeCairoBackend(ShaapeDrawingBackend):
    
    def __init__(self):
        super(ShaapeCairoBackend, self).__init__()
        self.margin = [10, 10, 10, 10]
        self.__surfaces = []
        self.__blur_kernel = []
        self.__blur_sigma = 1
        self.__blur_function = lambda x, y: 1 / (2 * math.pi * (self.__blur_sigma**2)) * math.e**(-1 * (x * x + y * y) / 2 * (self.__blur_sigma**2))
        self.__blur_kernel_height = 3
        self.__blur_kernel_width = 3
        # generate gaussian kernel
        for y in range(0, self.__blur_kernel_height):
            self.__blur_kernel.append([])
            for x in range (0, self.__blur_kernel_width):
                y_length = y - math.floor(self.__blur_kernel_height / 2)
                x_length = x - math.floor(self.__blur_kernel_width / 2)
                self.__blur_kernel[-1].append(self.__blur_function(x_length, y_length))
        self.__blur_kernel = np.array(self.__blur_kernel)
        filter_sum = sum(sum(self.__blur_kernel))
        self.__blur_kernel = self.__blur_kernel / filter_sum
        self.__blur_kernel.shape = (self.__blur_kernel_width, self.__blur_kernel_height, 1)
        return

    def blur_surface(self):
        blurred_surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.image_size[0] + self.margin[0] + self.margin[1],  self._canvas_size[1] + self.margin[2] + self.margin[3])
        top_surface = self.__surfaces[-1]
        width = top_surface.get_width()
        height = top_surface.get_height()
        stride = top_surface.get_stride()
        src = np.frombuffer(top_surface.get_data(), np.uint8)
        src.shape = (height, width, 4)
        dst = np.frombuffer(blurred_surface.get_data(), np.uint8)
        dst.shape = (height, width, 4)
        dst = ndimage.convolve(src, self.__blur_kernel, mode='reflect')
        blurred_image = cairo.ImageSurface.create_for_data(dst, cairo.FORMAT_ARGB32, width, height, width * 4)
        self.ctx.set_source_surface(blurred_image)
        self.ctx.set_operator(cairo.OPERATOR_SOURCE)
        self.ctx.paint()

        return

    def push_surface(self):
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.image_size[0] + self.margin[0] + self.margin[1],  self._canvas_size[1] + self.margin[2] + self.margin[3])
        self.__surfaces.append(surface)
        self.ctx = cairo.Context(surface)
        self.__drawn_graph = nx.Graph()
        return

    def pop_surface(self):
        surface = self.__surfaces.pop()
        self.ctx = cairo.Context(self.__surfaces[-1])
        self.ctx.set_source_surface(surface)
        self.ctx.set_operator(cairo.OPERATOR_OVER)
        self.ctx.paint()
        return

    def create_canvas(self, filename):
        self.image_size = (self._canvas_size[0], self._canvas_size[1])
        self.push_surface()
        self.ctx.set_source_rgb(1, 1, 1)
        self.ctx.rectangle(0.0, 0.0, self.image_size[0] + self.margin[0] + self.margin[1], self.image_size[1] + self.margin[2] + self.margin[3])
        self.ctx.fill()
        self.ctx.translate(self.margin[0], self.margin[2])
        # self.ctx.scale(20,20)
        return
    
    def apply_dash(self, drawable):
        if drawable.style().fill_type() == 'dashed':
            width = drawable.style().width()
            dash_list = [ width * 4, width]
            self.ctx.set_dash(dash_list, width * 2)
        elif drawable.style().fill_type() == 'dotted':
            width = drawable.style().width()
            dash_list = [ width, width]
            self.ctx.set_dash(dash_list)
        elif drawable.style().fill_type() == 'dash-dotted':
            width = drawable.style().width()
            dash_list = [ width * 4, width, width, width]
            self.ctx.set_dash(dash_list)
        else:
            self.ctx.set_dash([])

    def apply_line(self, drawable):
        self.ctx.set_line_cap(cairo.LINE_CAP_BUTT)
        self.ctx.set_line_join (cairo.LINE_JOIN_ROUND)
        width =  drawable.style().width()
        if len(drawable.style().color()) == 3:
            self.ctx.set_source_rgb(*(drawable.style().color()))
        else:
            self.ctx.set_source_rgba(*(drawable.style().color()))

        self.apply_dash(drawable)
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
        self.ctx.save()
        self.apply_fill(polygon)
        self.apply_transform(polygon)
        nodes = polygon.nodes()
        if len(nodes) > 1 and nodes[0] != nodes[-1]:
            nodes = nodes + [nodes[0]]
        nodes = [nodes[-2]] + nodes
        self.apply_path(nodes)
                
        self.ctx.fill()
        self.ctx.restore()
        return

    def draw_polygon_shadow(self, polygon):
        self.ctx.save()
        self.apply_fill(polygon)
        self.ctx.set_source_rgba(0, 0, 0, 0.5)
        self.ctx.set_operator(cairo.OPERATOR_SOURCE)
        self.apply_transform(polygon)
        nodes = polygon.nodes()
        if len(nodes) > 1 and nodes[0] != nodes[-1]:
            nodes = nodes + [nodes[0]]
        nodes = [nodes[-2]] + nodes
        self.apply_path(nodes)
        self.ctx.fill()
        self.ctx.restore()
        return

    def draw_open_graph_shadow(self, open_graph):
        self.apply_line(open_graph)
        self.ctx.set_source_rgba(0, 0, 0, 0.5)
        self.ctx.save()
        self.apply_transform(open_graph)
        self.ctx.set_operator(cairo.OPERATOR_SOURCE)
        paths = open_graph.paths()
        if len(paths) > 0:
            for path in paths:
                if path[0] == path[-1]:
                    nodes = [path[-2]] + path 
                else:
                    nodes = [path[0]] + path + [path[-1]]
                self.apply_path(nodes)
                self.ctx.stroke()
        self.ctx.restore()
        return

    def apply_path(self, nodes):
        if nodes[0].style() == 'curve':
            line_end = nodes[1] + ((nodes[0] - nodes[1]) * 0.5)
        else: 
            line_end = nodes[0]
        self.ctx.move_to(*line_end)
        for i in range(1, len(nodes) - 1):
            if nodes[i].style() == 'miter':
                self.ctx.line_to(*nodes[i])
                line_end = nodes[i]
            elif nodes[i].style() == 'curve':
                if i > 0 and nodes[i - 1].style() == 'miter':
                    temp_end = nodes[i - 1] + ((nodes[i] - nodes[i - 1]) * 0.5)
                    self.ctx.line_to(*temp_end)
                line_end = nodes[i] + ((nodes[i + 1] - nodes[i]) * 0.5)
                cp1 = nodes[i - 1] + ((nodes[i] - nodes[i - 1]) * 0.9)
                cp2 = nodes[i + 1] + ((nodes[i] - nodes[i + 1]) * 0.9)
                self.ctx.curve_to(cp1[0], cp1[1], cp2[0], cp2[1], line_end[0], line_end[1])
                    
        return

    def draw_open_graph(self, open_graph):
        self.apply_line(open_graph)
        self.ctx.save()
        self.apply_transform(open_graph)
        self.ctx.set_operator(cairo.OPERATOR_SOURCE)
        paths = open_graph.paths()
        if len(paths) > 0:
            for path in paths:
                if path[0] == path[-1]:
                    nodes = [path[-2]] + path 
                else:
                    nodes = [path[0]] + path + [path[-1]]
                self.apply_path(nodes)
                self.ctx.stroke()
        self.ctx.restore()
        return

    def draw_text(self, text_obj):
        text = text_obj.text()
        self.ctx.select_font_face("monospace", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        xbearing, ybearing, width, height, xadvance, yadvance = self.ctx.text_extents(text)
        self.ctx.save()
        self.ctx.set_source_rgb(0.0, 0.0, 0.0)
        self.ctx.set_font_size(text_obj.font_size() / 0.7)
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
        return

    def export_to_file(self, filename):
        # self.ctx.paint()
        self.__surfaces[-1].write_to_png(filename)
        return

    def start_object(self):
        self.ctx.save()
        return

    def end_object(self):
        self.ctx.restore()
