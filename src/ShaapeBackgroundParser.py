from ShaapeParser import ShaapeParser
from ShaapeDrawable import ShaapeBackground

class ShaapeBackgroundParser(ShaapeParser):
    def __init__(self):
        super(ShaapeBackgroundParser, self).__init__()
        return

    def run(self, raw_data, drawable_objects):
        max_len = len(max(raw_data, key=len))
        raw_data = [line + (max_len - len(line)) * ' ' for line in raw_data]
        canvas_size = [len(raw_data[0]), len(raw_data)]
        self._drawable_objects.append(ShaapeBackground(canvas_size))
        self._parsed_data = raw_data
        return
