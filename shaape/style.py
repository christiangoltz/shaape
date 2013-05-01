import copy
from font import Font

class Style(object):
    COLORS = { 'red' : [1, 0, 0], 'green' : [0, 1, 0], 'blue' : [0, 0, 1], 'empty' : [0, 0, 0, 0] }
    DEFAULT_STYLE = { 'color' : [[0, 0, 0, 1]], 'type' : 'solid', 'shadow' : 'on', 'width' : 1, 'font' : Font() }
    KEYWORDS = ['shadow', 'dash-dotted', 'dashed', 'dotted', 'solid', 'no-shadow']

    def __init__(self, name_pattern = '', target_type = '', option_list = [], priority = -1):
        self.__name_pattern = name_pattern
        self.__options = {}
        self.__priority = priority
        self.set_target_type(target_type)
        self.set_options(option_list)
        return

    def priority(self):
        return self.__priority

    def options(self):
        return self.__options

    def set_options(self, option_list):
        # find colors
        colors = filter(lambda x: x in Style.COLORS.keys(), option_list) 
        for color in colors:
            self.add_color(Style.COLORS[color])
        color_lists = [option for option in option_list if type(option) == list and len(option) in range(3,5) ]
        if len(color_lists) > 0:
            for color in color_lists:
                self.add_color(color)

        if 'solid' in option_list:
            self.set_type('solid')
        elif 'dashed' in option_list:
            self.set_type('dashed')
        elif 'dash-dotted' in option_list:
            self.set_type('dash-dotted')
        elif 'dotted' in option_list:
            self.set_type('dotted')
        # shadow
        if 'no-shadow' in option_list:
            self.set_shadow('off')
        elif 'shadow' in option_list:
            self.set_shadow('on')

        for option in option_list:
            if type(option) == float or type(option) == int:
                if self.__target_type == 'text':
                    self.font().set_size(option)
                else:
                    self.set_width(option)
            if type(option) == str and not option in self.KEYWORDS + self.COLORS.keys():
                if self.__target_type == 'text':
                    self.font().set_name(option)

    def merge(self, style):
        self.__options = dict(self.__options.items() + style.options().items())
        self.__priority = style.priority()
        return

    def target_type(self):
        return self.__target_type

    def name_pattern(self):
        return self.__name_pattern

    def set_name_pattern(self, name_pattern):
        self.__name_pattern = name_pattern

    def shadow(self):
        return  dict(Style.DEFAULT_STYLE.items() + self.__options.items())['shadow']

    def set_target_type(self, target_type):
        self.__target_type = target_type
        if self.__target_type == 'text':
            self.set_font(Font())
        return

    def color(self):
        return dict(Style.DEFAULT_STYLE.items() + self.__options.items())['color']

    def fill_type(self):
        return dict(Style.DEFAULT_STYLE.items() + self.__options.items())['type']

    def font(self):
        return dict(Style.DEFAULT_STYLE.items() + self.__options.items())['font']

    def width(self):
        return dict(Style.DEFAULT_STYLE.items() + self.__options.items())['width']

    def add_color(self, color):
        if len(color) == 3 or len(color) == 4:
            if not 'color' in self.__options.keys():
                self.__options['color'] = []
            self.__options['color'].append(color)
        else:
            raise ValueError
        return

    def set_color(self, color):
        if len(color) == 3 or len(color) == 4:
            self.__options['color'] = [color]
        else:
            raise ValueError
        return

    def set_type(self, fill_type):
        self.__options['type'] = fill_type
        return

    def set_font(self, font):
        self.__options['font'] = font
        return

    def set_shadow(self, shadow):
        self.__options['shadow'] = shadow
        return

    def set_width(self, width):
        if width <= 0:
            raise ValueError
        self.__options['width'] = width
        return

    def __cmp__(self, other):
        if not isinstance(other, Style):
            return -1
        else:
            return cmp((self.__name_pattern, self.__target_type, self.__options),(other.name_pattern(), other.target_type(), other.options()))

    def __repr__(self):
        return "(name_pattern: " + str(self.__name_pattern) + ", target_type:" + self.__target_type + ", options:" + str(self.__options) + ", prio:" + str(self.priority()) + ")"
