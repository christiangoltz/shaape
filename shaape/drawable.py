import math
import operator
import networkx as nx
from node import *
from style import Style

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
        raise NotImplementedError

    def max(self):
        raise NotImplementedError
