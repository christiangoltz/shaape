from ShaapeParser import ShaapeParser

class ShaapeNameParser(ShaapeParser):
    def __init__(self):
        super(ShaapeNameParser, self).__init__()
        return

    def run(self, raw_data, drawable_objects):
        self._parsed_data = raw_data
        self._drawable_objects = drawable_objects
        return
