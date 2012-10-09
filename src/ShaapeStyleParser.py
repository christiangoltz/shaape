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


        for style in styles:
            if '_default_' in style.names():
                ShaapeStyle.set_default(style)
            style_names = style.names()
            for obj in named_drawables:
                if len(set(style_names) & set(obj.names())) > 0:
                    obj.set_style(style)

        self._parsed_data = raw_data
        self._drawable_objects = drawable_objects
        return
