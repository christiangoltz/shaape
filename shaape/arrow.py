from polygon import Polygon
from named import Named
from node import Node
from translatable import Translatable

class Arrow(Polygon, Translatable, Named):
    def __init__(self, position = (0, 0), node_list = []):
        Polygon.__init__(self, node_list)
        Translatable.__init__(self, position)
        Named.__init__(self)
        self.__connected_objects = []
        self.__pointed_objects = []
        self.add_name('_arrow_')

    def scale(self, scale):
        Translatable.scale(self, scale)
        Polygon.scale(self, scale)
        return

    def direction(self):
        raise NotImplementedError

    def add_connected_object(self, obj):
        self.__connected_objects.append(obj)

    def connected_objects(self):
        return self.__connected_objects

    def add_pointed_object(self, obj):
        self.__pointed_objects.append(obj)

    def pointed_objects(self):
        return self.__pointed_objects
