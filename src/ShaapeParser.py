class ShaapeParser(object):
    def __init__(self):
        self._parsed_data = []
        self._drawable_objects = []
        return

    def run(self, raw_data, drawable_objects):
        self._parsed_data = raw_data
        self._drawable_objects = drawable_objects
        return

    def parsed_data(self):
        return self._parsed_data

    def drawable_objects(self):
        return self._drawable_objects
