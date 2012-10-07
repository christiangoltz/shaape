import operator
import networkx as nx

class ShaapeDrawable(object):
    def __init__(self):
        return

class ShaapeBackground(ShaapeDrawable):
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


class ShaapePolygon(ShaapeDrawable):
    def __init__(self, node_list):
        self.__node_list = node_list
        return

    def get_nodes(self):
        return self.__node_list

    def get_max(self):
        return (max([n[0] for n in self.__node_list]), max([n[1] for n in self.__node_list]))

    def get_min(self):
        return (min([n[0] for n in self.__node_list]), min([n[1] for n in self.__node_list]))

    def scale(self, scale):
        for n in range(0, len(self.__node_list)):
            node = self.__node_list[n]
            self.__node_list[n] = (node[0] * scale[0], node[1] * scale[1])

class ShaapeText(ShaapeDrawable, ShaapeTranslatable):
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

class ShaapeOpenGraph(ShaapeDrawable):
    def __init__(self, graph):
        self.__graph = graph
        for node in self.__graph.nodes():
            if self.__graph.degree(node) == 0:
                self.__graph.remove_node(node)
        return

    def get_graph(self):
        return self.__graph

    def get_max(self):
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
        ShaapePolygon.__init__(self, [(0, 0.1), (0.4, 0), (0, -0.1)])
        ShaapeTranslatable.__init__(self, position)

    def scale(self, scale):
        ShaapeTranslatable.scale(self, scale)
        ShaapePolygon.scale(self, scale)
        return

class ShaapeRightArrow(ShaapeArrow, ShaapeRotatable):
    def __init__(self, position):
        ShaapeArrow.__init__(self, position)
        ShaapeRotatable.__init__(self, 0)

    # def scale(self, scale):
        # ShaapeTranslatable.scale(self, scale)
        # return

class ShaapeDownArrow(ShaapeArrow, ShaapeRotatable):
    def __init__(self, position):
        ShaapeArrow.__init__(self, position)
        ShaapeRotatable.__init__(self, 90)

class ShaapeLeftArrow(ShaapeArrow, ShaapeRotatable):
    def __init__(self, position):
        ShaapeArrow.__init__(self, position)
        ShaapeRotatable.__init__(self, 180)

class ShaapeUpArrow(ShaapeArrow, ShaapeRotatable):
    def __init__(self, position):
        ShaapeArrow.__init__(self, position)
        ShaapeRotatable.__init__(self, 270)

