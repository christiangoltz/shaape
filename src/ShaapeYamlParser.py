import yaml
from ShaapeParser import ShaapeParser

class ShaapeYamlParser(ShaapeParser):
    def __init__(self):
        super(ShaapeYamlParser, self).__init__()
        return
    def run(self, raw_data, drawable_objects):
        options_start = 0
        # print(raw_data)
        for i in range(0, len(raw_data)):
            if raw_data[i].find('options:') == 0:
                options_start = i
                break
        options = yaml.load(''.join(raw_data[options_start+1:-1]))
        for (key,value) in options.items():
            drawable_objects.append(ShaapeStyle(key, value))
        self._drawable_objects = drawable_objects
        self._parsed_data = raw_data[0:options_start]
        return
