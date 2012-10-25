import yaml
from ShaapeParser import ShaapeParser
from ShaapeStyle import ShaapeStyle

class ShaapeYamlParser(ShaapeParser):
    def __init__(self):
        super(ShaapeYamlParser, self).__init__()
        return
    def run(self, raw_data, drawable_objects):
        options_start = -1
        for i in range(0, len(raw_data)):
            if raw_data[i].find('options:') == 0:
                options_start = i
                break
        if options_start > -1:
            raw_data.append('\n')
            options = yaml.load(''.join(raw_data[options_start+1:-1]))
            for (key,value) in options.items():
                names = yaml.load("[" + key + "]")
                for (target_type, option) in value.items():
                    drawable_objects.append(ShaapeStyle(names, target_type, option))
            self._parsed_data = raw_data[0:options_start]
        else:
            self._parsed_data = raw_data
        self._drawable_objects = drawable_objects
        return
