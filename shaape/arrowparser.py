from rightarrow import RightArrow
from leftarrow import LeftArrow
from uparrow import UpArrow
from downarrow import DownArrow
from parser import Parser
from drawable import *

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
        for y in range(0, len(raw_data)):
            for x in range(0, len(raw_data[0])): 
                if raw_data[y][x] in self._arrows.keys():
                    arrow = self._arrows[raw_data[y][x]](((x + 0.5), (y + 0.5)))
                    drawable_objects.append(arrow)
        self._drawable_objects = drawable_objects
        self._parsed_data = raw_data
        return
