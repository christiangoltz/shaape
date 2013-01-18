from parser import Parser
from text import Text
from named import Named
from drawable import Drawable
from arrow import Arrow
from polygon import Polygon
from opengraph import OpenGraph
from style import Style
import re

class StyleParser(Parser):
    def __init__(self):
        super(StyleParser, self).__init__()
        return

    def run(self, raw_data, drawable_objects):
        styles = filter(lambda x: isinstance(x, Style), drawable_objects)
        styles = sorted(styles, key = lambda x: x.priority())
        named_drawables = filter(lambda x: isinstance(x, Drawable) and isinstance(x, Named), drawable_objects)
        
        default_style = {
            'fill' : Style([], 'fill', [[0.9 ,0.9, 0.9], 'gradient']),
            'frame' : Style([], 'frame', [[0, 0, 0], 'solid', 2]),
            'line' : Style([], 'fill', [[0, 0, 0, 1], 'solid', 2]),
            'arrow' : Style([], 'fill', [[0, 0, 0], 'flat']),
            'text' : Style([], 'text', [[0, 0, 0], 'solid', 2])}

        for obj in drawable_objects:
            if isinstance(obj, Drawable):
                if isinstance(obj, Arrow):
                    obj.set_style(default_style['arrow'])
                elif isinstance(obj, Polygon):
                    obj.set_style(default_style['fill'])
                    obj.frame().set_style(default_style['frame'])
                elif isinstance(obj, OpenGraph):
                    obj.set_style(default_style['line'])
                elif isinstance(obj, Text):
                    obj.set_style(default_style['text'])


        for style in styles:
            name_pattern = re.compile(style.name_pattern())
            for obj in named_drawables:
                for name in obj.names():
                    if name_pattern.match(name):
                        if style.target_type() == 'frame' and isinstance(obj, Polygon):
                            target_obj = obj.frame()
                        elif style.target_type() == 'text' and isinstance(obj, Text):
                            target_obj = obj
                        elif style.target_type() == 'fill':
                            target_obj = obj
                        else:
                            target_obj = None
                        if target_obj != None:
                            if style.priority() > target_obj.style().priority():
                                target_obj.set_style(style)

        self._parsed_data = raw_data
        self._drawable_objects = drawable_objects
        return
