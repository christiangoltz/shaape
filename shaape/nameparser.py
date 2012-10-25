from ShaapeParser import ShaapeParser
from ShaapeDrawable import ShaapePolygon
from ShaapeDrawable import ShaapeText

class ShaapeNameParser(ShaapeParser):
    def __init__(self):
        super(ShaapeNameParser, self).__init__()
        return

    def run(self, raw_data, drawable_objects):
        self._parsed_data = raw_data
        self._drawable_objects = drawable_objects
        polygons = filter(lambda x: isinstance(x, ShaapePolygon), drawable_objects)
        texts = filter(lambda x: isinstance(x, ShaapeText), drawable_objects)
        
        for polygon in polygons:
            for text in texts:
                position = (text.position()[0] + 0.5, text.position()[1] + 0.5)
                if polygon.contains(position) == True:
                    polygon.add_name(text.text())
        return
