import operator
import networkx as nx

from ShaapeStyle import ShaapeStyle

class ShaapeScalable(object):
    def __init__(self):
        pass

    def scale(self, scale):
        pass

class ShaapeNamed(object):
    def __init__(self):
        self.__names = []
        return
    
    def names(self):
        return self.__names

    def add_name(self, name):
        self.__names.append(name)
        return

class ShaapeDrawable(object):
    def __init__(self):
        self.__style = ShaapeStyle([], '', [])
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

class ShaapeBackground(ShaapeDrawable, ShaapeScalable):
    def __init__(self, size):
        self.__size = size
        return
    
    def size(self):
        return self.__size

    def scale(self, scale):
        self.__size = (self.__size[0] * scale[0], self.__size[1] * scale[1])

class ShaapeRotatable(object):
    def __init__(self, angle = 0):
        self.angle = angle

    def set_angle(self, angle):
        self.angle = angle

    def get_angle(self):
        return self.angle

class ShaapeTranslatable(object):
    def __init__(self, position = (0, 0)):
        self.__position = position

    def set_position(self, position):
        self.__position = position

    def position(self):
        return self.__position

    def scale(self, scale):
        self.__position = (self.__position[0] * scale[0], self.__position[1] * scale[1])
        return


class ShaapePolygon(ShaapeDrawable, ShaapeNamed, ShaapeScalable):
    def __init__(self, node_list):
        ShaapeDrawable.__init__(self)
        ShaapeNamed.__init__(self)
        self.__node_list = node_list
        cycle_graph = nx.Graph()
        cycle_graph.add_cycle(node_list)
        self.__frame = ShaapeOpenGraph(cycle_graph)
        self.style().set_target_type('fill')
        self.__frame.style().set_target_type('frame')
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
            self.__node_list[n] = (node[0] * scale[0], node[1] * scale[1])
        self.__frame.scale(scale)

    def frame(self):
        return self.__frame

class ShaapeText(ShaapeDrawable, ShaapeTranslatable, ShaapeScalable):
    def __init__(self, text, position):
        ShaapeDrawable.__init__(self)
        ShaapeTranslatable.__init__(self, position)
        self.__text = text
        self.__font_size = 1
        return

    def text(self):
        return self.__text

    def font_size(self):
        return self.__font_size

    def scale(self, scale):
        ShaapeTranslatable.scale(self, scale)
        self.__font_size = self.__font_size * scale[0]
        return

class ShaapeOpenGraph(ShaapeDrawable, ShaapeScalable):
    def __init__(self, graph):
        ShaapeDrawable.__init__(self)
        self.style().set_target_type('line')
        self.__graph = graph
        for node in self.__graph.nodes():
            if self.__graph.degree(node) == 0:
                self.__graph.remove_node(node)
        return

    def graph(self):
        return self.__graph

    def max(self):
        return (max([n[0] for n in self.__graph.nodes()]), max([n[1] for n in self.__graph.nodes()]))

    def scale(self, scale):
        old_nodes = self.__graph.nodes()
        new_nodes = {}
        for node in old_nodes:
            new_nodes[node] = (node[0] * scale[0], node[1] * scale[1])
        self.__graph = nx.relabel_nodes(self.__graph, new_nodes)
        return

class ShaapeArrow(ShaapePolygon, ShaapeTranslatable):
    def __init__(self, position):
        ShaapePolygon.__init__(self, [(-0.5, 0.2), (0.4, 0), (-0.5, -0.2)])
        ShaapeTranslatable.__init__(self, position)
        self.style().set_color([0, 0, 0, 1])
        self.style().set_type('flat')
        self.frame().style().set_width(0)

    def scale(self, scale):
        ShaapeTranslatable.scale(self, scale)
        ShaapePolygon.scale(self, scale)
        return

class ShaapeRightArrow(ShaapeArrow, ShaapeRotatable):
    def __init__(self, position):
        ShaapeArrow.__init__(self, position)
        ShaapeRotatable.__init__(self, 0)

class ShaapeDownArrow(ShaapeArrow, ShaapeRotatable):
    def __init__(self, position):
        ShaapeArrow.__init__(self, (position[0], position[1] - 0.4))
        ShaapeRotatable.__init__(self, 90)

class ShaapeLeftArrow(ShaapeArrow, ShaapeRotatable):
    def __init__(self, position):
        ShaapeArrow.__init__(self, position)
        ShaapeRotatable.__init__(self, 180)

class ShaapeUpArrow(ShaapeArrow, ShaapeRotatable):
    def __init__(self, position):
        ShaapeArrow.__init__(self, (position[0], position[1] + 0.3))
        ShaapeRotatable.__init__(self, 270)

