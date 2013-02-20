from parser import Parser
from background import Background

class BackgroundParser(Parser):
    def __init__(self):
        super(BackgroundParser, self).__init__()
        return

    def run(self, raw_data, objects):
        self._parsed_data = []
        self._objects = objects
        if raw_data != []:
            max_len = len(max(raw_data, key=len))
            for line in raw_data:
                if line[-1] == '\n':
                    line = line[:-1]
                self._parsed_data.append(line + (max_len - len(line)) * ' ' + '\n')
            canvas_size = (len(self._parsed_data[0]) - 1, len(self._parsed_data))
            self._objects = objects
            self._objects.append(Background(canvas_size))
        return
