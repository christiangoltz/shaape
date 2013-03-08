from node import Node
from opengraph import OpenGraph
from polygon import Polygon
from rightarrow import RightArrow
from leftarrow import LeftArrow
from uparrow import UpArrow
from downarrow import DownArrow
from parser import Parser
from drawable import *
from graphalgorithms import angle
import networkx

class ArrowParser(Parser):
    def __init__(self):
        super(ArrowParser, self).__init__()
        self._arrows = {}
        self._arrows['>'] = RightArrow
        self._arrows['<'] = LeftArrow
        self._arrows['^'] = UpArrow
        self._arrows['v'] = DownArrow
        return

    def run(self, raw_data, drawable_objects):
        arrows = []
        for y in range(0, len(raw_data)):
            for x in range(0, len(raw_data[0])): 
                if raw_data[y][x] in self._arrows.keys():
                    arrow = self._arrows[raw_data[y][x]]((x + 0.5, y + 0.5))
                    arrows.append(arrow)

        # snap arrows to objects near them
        graph = None
        try:
            graph = next(obj for obj in drawable_objects if type(obj) == nx.Graph)
        except StopIteration:
            pass
        if graph != None:
            for arrow in arrows:
                for obj in drawable_objects:
                    connector = Node(*(arrow.connector()))
                    # instance has to be an graph, arrows are never connected to polygons directly
                    if isinstance(obj, OpenGraph):
                        if obj.has_node(connector):
                            arrow.add_connected_object(obj)
                    else:
                        pass
            for arrow in arrows:
                tip = Node(*(arrow.tip()))
                nodes_in_front = [node for node in graph.nodes() if (node == tip) or angle(arrow.direction(), node - tip) <= 90]
                if nodes_in_front:
                    nearest_node = min(nodes_in_front, key=lambda node: (node - tip.position()).length())
                    diff = nearest_node - tip
                    if diff.length() <= 0.5:
                        connector = Node(*(arrow.connector()))
                        path = [connector, connector + diff]
                        for obj in arrow.connected_objects():
                            # instance is always an graph, arrows are never connected to polygons directly
                            obj.add_path(path)
                        arrow.translate(diff)
                tip = Node(*(arrow.tip()))
                for obj in drawable_objects:
                    if isinstance(obj, OpenGraph):
                        if obj.has_node(tip):
                            arrow.add_pointed_object(obj)
                    elif isinstance(obj, Polygon):
                        if obj.frame().has_node(tip):
                            arrow.add_pointed_object(obj.frame())
                    else:
                        pass

        self._objects = drawable_objects + arrows
        drawable_objects += arrows
        self._parsed_data = raw_data
        return
