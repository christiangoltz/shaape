from ShaapeParser import ShaapeParser
from ShaapeDrawable import ShaapeText
import re

class ShaapeTextParser(ShaapeParser):
    def __init__(self):
        super(ShaapeTextParser, self).__init__()
        self._non_text_objects = '-|+\\/'
        return

    def run(self, raw_data, drawable_objects):
        quoted_string_pattern = re.compile('\'([^\']+)\'')
        unquoted_string_pattern = re.compile('([\w]{2,})')
        line_number = 0
        for line in raw_data:
            matches = quoted_string_pattern.finditer(line)
            for match in matches:
                span = match.span()
                line = line[:span[0]] + ''.join([' ' for n in range(span[0], span[1])]) + line[span[1] :]
                drawable_objects.append(ShaapeText(match.group(1), (span[0] + 1, line_number))) 
            matches = unquoted_string_pattern.finditer(line)
            for match in matches:
                span = match.span()
                line = line[:span[0]] + ''.join([' ' for n in range(span[0], span[1])]) + line[span[1] :]
                drawable_objects.append(ShaapeText(match.group(1), (span[0], line_number))) 
            raw_data[line_number] = line
            line_number = line_number + 1
                
        self._parsed_data = raw_data
        self._drawable_objects = drawable_objects
        return
