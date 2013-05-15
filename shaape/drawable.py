import math
import operator
import networkx as nx
from node import *
from style import Style

class Drawable(object):
    def __init__(self, options = []):
        self.__style = Style([], '', [])
        self.__z_order = 0
        self.__options = options
        return

    def options(self):
        return self.__options

    def set_z_order(self, z_order):
        self.__z_order = z_order
        return

    def z_order(self):
        return self.__z_order

    def set_style(self, style):
        self.__style.merge(style)
        return

    def style(self):
        return self.__style

    def min(self):
        raise NotImplementedError

    def max(self):
        raise NotImplementedError
