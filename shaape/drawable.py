import copy
from operator import itemgetter
import math
import operator
import networkx as nx
from node import *

from style import Style

def reduce_path(nodes):
    new_nodes = []
    new_nodes = nodes[0:2]
    for i in range(2, len(nodes)):
        previous_edge = nodes[i - 1] - nodes[i - 2]
        current_edge = nodes[i] - nodes[i - 1]
        if new_nodes[-1].fusable() == True and has_same_direction(previous_edge, current_edge):
            new_nodes[-1] = nodes[i]
        else:
            new_nodes.append(nodes[i])
    if len(new_nodes) > 2 and new_nodes[0] == new_nodes[-1]:
        first_edge = new_nodes[1] - new_nodes[0]
        last_edge = new_nodes[-1] - new_nodes[-2]
        if has_same_direction(first_edge, last_edge):
            del new_nodes[-1]
            new_nodes[0] = new_nodes[-1]
    return new_nodes

def has_same_direction(v1, v2):
    if v2[0] == 0 and v1[0] == 0:
        return True
    elif v2[0] == 0:
        return False
    if v2[1] == 0 and v1[1] == 0:
        return True
    elif v2[1] == 0:
        return False

    diff_x = v1[0] / v2[0]
    diff_y = v1[1] / v2[1]

    if diff_x == diff_y or ((-1 * diff_x) == (-1 * diff_y)):
        return True
    else:
        return False

class Scalable(object):
    def __init__(self):
        pass

    def scale(self, scale):
        return NotImplemented

class Named(object):
    def __init__(self):
        self.__names = []
        return
    
    def names(self):
        return self.__names

    def add_name(self, name):
        self.__names.append(name)
        return

class Drawable(object):
    def __init__(self):
        self.__style = Style([], '', [])
        return

    def set_style(self, style):
        self.__style.merge(style)
        return

    def style(self):
        return self.__style

    def min(self):
        return (0,0)

    def max(self):
        return (0,0)

class Background(Drawable, Scalable):
    def __init__(self, size):
        self.__size = size
        return
    
    def size(self):
        return self.__size

    def scale(self, scale):
        self.__size = (self.__size[0] * scale[0], self.__size[1] * scale[1])

class Rotatable(object):
    def __init__(self, angle = 0):
        self.angle = angle

    def set_angle(self, angle):
        self.angle = angle

    def get_angle(self):
        return self.angle

class Translatable(object):
    def __init__(self, position = (0, 0)):
        self.__position = position

    def set_position(self, position):
        self.__position = position

    def position(self):
        return self.__position

    def scale(self, scale):
        self.__position = (self.__position[0] * scale[0], self.__position[1] * scale[1])
        return


class Polygon(Drawable, Named, Scalable):
    def __init__(self, node_list):
        Drawable.__init__(self)
        Named.__init__(self)
        self.__node_list = node_list
        cycle_graph = nx.Graph()
        cycle_graph.add_cycle(node_list)
        self.__frame = OpenGraph(cycle_graph)
        self.style().set_target_type('fill')
        self.__frame.style().set_target_type('frame')
        self.__node_list = reduce_path(self.__node_list)
        return


    def contains(self, point):
        # point inside polygon
        n = len(self.__node_list)
        inside = False
        x,y = point
        p1x,p1y = self.__node_list[0]
        for i in range(n+1):
            p2x,p2y = self.__node_list[i % n]
            if y > min(p1y,p2y):
                if y <= max(p1y,p2y):
                    if x <= max(p1x,p2x):
                        if p1y != p2y:
                            xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x,p1y = p2x,p2y
        return inside

    def nodes(self):
        return self.__node_list

    def max(self):
        return (max([n[0] for n in self.__node_list]), max([n[1] for n in self.__node_list]))

    def min(self):
        return (min([n[0] for n in self.__node_list]), min([n[1] for n in self.__node_list]))

    def scale(self, scale):
        for n in range(0, len(self.__node_list)):
            node = self.__node_list[n]
            self.__node_list[n] = node * scale
        self.__frame.scale(scale)

    def frame(self):
        return self.__frame

class Text(Drawable, Translatable, Scalable):
    def __init__(self, text, position):
        Drawable.__init__(self)
        Translatable.__init__(self, position)
        self.__text = text
        self.__font_size = 1
        return

    def text(self):
        return self.__text

    def font_size(self):
        return self.__font_size

    def scale(self, scale):
        Translatable.scale(self, scale)
        self.__font_size = self.__font_size * scale[0]
        return

class OpenGraph(Drawable, Scalable):
    def __init__(self, graph):
        Drawable.__init__(self)
        self.style().set_target_type('line')
        self.__graph = nx.Graph(graph)
        for node in self.__graph.nodes():
            if self.__graph.degree(node) == 0:
                self.__graph.remove_node(node)
        self.__generate_paths()
        return

    def graph(self):
        return self.__graph

    def max(self):
        return (max([n[0] for n in self.__graph.nodes()]), max([n[1] for n in self.__graph.nodes()]))

    def scale(self, scale):
        old_nodes = self.__graph.nodes()
        new_nodes = {}
        for node in old_nodes:
            new_nodes[node] = node * scale
        self.__graph = nx.relabel_nodes(self.__graph, new_nodes)
        for path in self.__paths:
            for i in range(0, len(path)):
                path[i] = path[i] * scale
        return


    def __generate_paths(self):
        nodes = [node for node in self.__graph.nodes() if self.__graph.degree(node) == 1]
        if nodes == []:
            nodes = [node for node in self.__graph.nodes() if node.fusable() == False]
        if nodes == []:
            nodes = self.__graph.nodes()
        min_node = sorted(nodes, key=itemgetter(0, 1))[0] 
        path_gen = nx.dfs_labeled_edges(self.__graph, min_node)
        path = []
        paths = []
        self.__paths = []
        last_dir = ''
        for start, end, direction_dir in path_gen:
            direction = direction_dir['dir']
            if direction == 'forward':
                if len(path) == 0 or path[-1] <> start:
                    path.append(start)
                last_dir = direction
            elif direction == 'reverse':
                if last_dir <> 'reverse':
                    if len(path) > 0:
                        copy_path = copy.copy(path)
                        copy_path.append(end)
                        if len(path) > 2 and (self.__graph.has_edge(copy_path[0], copy_path[-1]) or self.__graph.has_edge(copy_path[-1], copy_path[0])):
                            copy_path.append(copy_path[0])
                        paths.append(copy_path)
                if len(path) > 0:
                    path.pop()
                last_dir = direction
        
        for path in paths:
            self.__paths.append(reduce_path(path))
        
        return        

    def paths(self):
        return self.__paths

class Arrow(Polygon, Translatable):
    def __init__(self, position):
        Polygon.__init__(self, [Node(-0.5, 0.2), Node(0.4, 0), Node(-0.5, -0.2)])
        Translatable.__init__(self, position)
        self.style().set_color([0, 0, 0, 1])
        self.style().set_type('flat')
        self.frame().style().set_width(0)

    def scale(self, scale):
        Translatable.scale(self, scale)
        Polygon.scale(self, scale)
        return

class RightArrow(Arrow, Rotatable):
    def __init__(self, position):
        Arrow.__init__(self, position)
        Rotatable.__init__(self, 0)

class DownArrow(Arrow, Rotatable):
    def __init__(self, position):
        Arrow.__init__(self, (position[0], position[1] - 0.4))
        Rotatable.__init__(self, 90)

class LeftArrow(Arrow, Rotatable):
    def __init__(self, position):
        Arrow.__init__(self, position)
        Rotatable.__init__(self, 180)

class UpArrow(Arrow, Rotatable):
    def __init__(self, position):
        Arrow.__init__(self, (position[0], position[1] + 0.3))
        Rotatable.__init__(self, 270)

