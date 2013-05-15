from parser import Parser
from polygon import Polygon
from opengraph import OpenGraph
from text import Text
from arrow import Arrow
from graphalgorithms import line_segments_distance
from graphalgorithms import line_segment_point_distance

class NameParser(Parser):
    def __init__(self):
        super(NameParser, self).__init__()
        return

    def run(self, raw_data, objects):
        self._parsed_data = raw_data
        self._objects = objects
        polygons = filter(lambda x: isinstance(x, Polygon), objects)
        graphs = filter(lambda x: isinstance(x, OpenGraph), objects)
        texts = filter(lambda x: isinstance(x, Text), objects)
        arrows = filter(lambda x: isinstance(x, Arrow), polygons)
        
        for text in texts:
            text.add_name(text.text())
            position = (text.position()[0] + 0.5, text.position()[1] + 0.5)
            polygons_containing_this_text = [polygon for polygon in polygons if polygon.contains(position)]
            if polygons_containing_this_text:
                polygon = max(polygons_containing_this_text,key = lambda p: p.z_order())
                text.set_z_order(polygon.z_order() + 1)
                polygon.add_name(text.text())
            else:
                for graph in graphs:
                    for edge in graph.edges():
                        if line_segments_distance((edge[0].position(), edge[1].position()), (text.letter_position(0), text.letter_position(len(text.text()) - 1))) <= 1:
                            graph.add_name(text.text())
                for arrow in arrows:
                    if line_segment_point_distance(arrow.tip(), (text.letter_position(0), text.letter_position(len(text.text()) - 1))) <= 1:
                        for obj in arrow.connected_objects():
                            obj.add_name(text.text())
        return
