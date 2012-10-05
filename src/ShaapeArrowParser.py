from ShaapeParser import ShaapeParser
from ShaapeDrawable import *

class ShaapeArrowParser(ShaapeParser):
    def __init__(self):
        super(ShaapeArrowParser, self).__init__()
        self._arrows = {}
        self._arrows['>'] = ShaapeRightArrow
        self._arrows['<'] = ShaapeLeftArrow
        self._arrows['^'] = ShaapeUpArrow
        self._arrows['v'] = ShaapeDownArrow
        return

    def run(self, raw_data, drawable_objects):
        for y in range(0, len(raw_data)):
            for x in range(0, len(raw_data[0])): 
                if raw_data[y][x] in self._arrows.keys():
                    arrow = self._arrows[raw_data[y][x]](((x + 0.5), (y + 0.5)))
                    drawable_objects.append(arrow)
        self._drawable_objects = drawable_objects
        self._parsed_data = raw_data
        return
