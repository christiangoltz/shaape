from drawable import Drawable

class Parser(object):
    def __init__(self):
        self._parsed_data = []
        self._objects = []
        return

    def run(self, raw_data, objects):
        raise NotImplementedError

    def parsed_data(self):
        return self._parsed_data

    def drawable_objects(self):
        return [obj for obj in self._objects if isinstance(obj, Drawable)]

    def objects(self):
        return self._objects
