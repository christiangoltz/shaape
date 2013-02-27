from parser import Parser
from text import Text
import re

class TextParser(Parser):
    def __init__(self):
        super(TextParser, self).__init__()
        self._non_text_objects = '-|+\\/'
        return

    def run(self, raw_data, objects):
        quoted_string_pattern = re.compile('\'([^\']+)\'', re.UNICODE)
        unquoted_string_pattern = re.compile('(([\w]{2,})|([^\Wv]))', re.UNICODE)
        line_number = 0
        for line in raw_data:
            matches = quoted_string_pattern.finditer(line)
            for match in matches:
                span = match.span()
                line = line[:span[0]] + ''.join([' ' for n in range(span[0], span[1])]) + line[span[1] :]
                objects.append(Text(match.group(1), (span[0] + 1, line_number))) 
            matches = unquoted_string_pattern.finditer(line)
            for match in matches:
                span = match.span()
                line = line[:span[0]] + ''.join([' ' for n in range(span[0], span[1])]) + line[span[1] :]
                text = Text(match.group(1), (span[0], line_number))
                objects.append(text) 
            raw_data[line_number] = line
            line_number = line_number + 1
                
        self._parsed_data = raw_data
        self._objects = objects
        return
