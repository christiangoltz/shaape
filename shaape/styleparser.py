from ShaapeParser import ShaapeParser
from ShaapeDrawable import *
from ShaapeStyle import ShaapeStyle

class ShaapeStyleParser(ShaapeParser):
    def __init__(self):
        super(ShaapeStyleParser, self).__init__()
        return

    def run(self, raw_data, drawable_objects):
        
        styles = filter(lambda x: isinstance(x, ShaapeStyle), drawable_objects)
        named_drawables = filter(lambda x: isinstance(x, ShaapeDrawable) and isinstance(x, ShaapeNamed), drawable_objects)
        
        default_style = {
            'fill' : ShaapeStyle([], 'fill', [[0.9 ,0.9, 0.9], 'gradient']),
            'frame' : ShaapeStyle([], 'frame', [[0, 0, 0], 'solid']),
            'line' : ShaapeStyle([], 'line', [[0, 0, 0], 'solid']),
            'arrow' : ShaapeStyle([], 'fill', [[0, 0, 0], 'flat']),}

        for style in styles:
            if '_default_' in style.names():
                 default_style[style.target_type()] = style
        for obj in drawable_objects:
            if isinstance(obj, ShaapeDrawable):
                if isinstance(obj, ShaapeArrow):
                    obj.set_style(default_style['arrow'])
                elif isinstance(obj, ShaapePolygon):
                    obj.set_style(default_style['fill'])
                    obj.frame().set_style(default_style['frame'])
                elif isinstance(obj, ShaapeOpenGraph):
                    obj.set_style(default_style['line'])

            
               

        for style in styles:
            if '_arrows_' in style.names():
                for obj in named_drawables:
                    if style.target_type() == 'fill' and isinstance(obj, ShaapeArrow):
                        obj.set_style(style)

            style_names = style.names()
            for obj in named_drawables:
                if not isinstance(obj, ShaapeArrow):
                    if len(set(style_names) & set(obj.names())) > 0:
                        if style.target_type() == 'fill' and isinstance(obj, ShaapePolygon):
                            obj.set_style(style)
                        elif style.target_type() == 'frame' and isinstance(obj, ShaapePolygon):
                            print(obj)
                            obj.frame().set_style(style)
                        elif style.target_type() == 'line' and isinstance(obj, ShaapeOpenGraph):
                            obj.set_style(style)

        self._parsed_data = raw_data
        self._drawable_objects = drawable_objects
        return
