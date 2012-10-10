import copy

class ShaapeStyle(object):
    COLORS = { 'red' : [1, 0, 0], 'green' : [0, 1, 0], 'blue' : [0, 0, 1] }
    DEFAULT_STYLE = { 'color' : [0, 0, 0, 1], 'type' : 'gradient', 'shadow' : 'on', 'width' : 1 }
    def __init__(self, apply_to_names, target_type, option_list):
        self.__names = apply_to_names
        self.__target_type = target_type
        self.__options = {}

        if type(option_list) <> list:
            option_list = [option_list]
        # find colors
        colors = filter(lambda x: x in ShaapeStyle.COLORS.keys(), option_list) 
        if len(colors) > 0:
            self.set_color(ShaapeStyle.COLORS[colors[0]])
        else:
            color_lists = [option for option in option_list if type(option) == list and len(option) in range(3,5) ]
            if len(color_lists) > 0:
                self.set_color(color_lists[0])
        # gradient                
        if 'flat' in option_list:
            self.set_type('flat')
        elif 'gradient' in option_list:
            self.set_type('gradient')

        if 'solid' in option_list:
            self.set_type('solid')
        # shadow
        if 'no-shadow' in option_list:
            self.set_shadow('off')
        elif 'shadow' in option_list:
            self.set_shadow('on')

        for option in option_list:
            if type(option) == float or type(option) == int:
                self.set_width(option)

        return

    def options(self):
        return self.__options

    def set_default(style):
        ShaapeStyle.DEFAULT_STYLE = dict(ShaapeStyle.DEFAULT_STYLE.items() + style.options().items())
        return

    def merge(self, style):
        self.__options = dict(self.__options.items() + style.options().items())
        return

    def target_type(self):
        return self.__target_type

    def names(self):
        return self.__names

    def shadow(self):
        return  dict(ShaapeStyle.DEFAULT_STYLE.items() + self.__options.items())['shadow']

    def set_target_type(self, target_type):
        self.__target_type = target_type
        return

    def color(self):
        return dict(ShaapeStyle.DEFAULT_STYLE.items() + self.__options.items())['color']

    def fill_type(self):
        return dict(ShaapeStyle.DEFAULT_STYLE.items() + self.__options.items())['type']

    def width(self):
        return  dict(ShaapeStyle.DEFAULT_STYLE.items() + self.__options.items())['width']

    def set_color(self, color):
        self.__options['color'] = color
        return

    def set_type(self, fill_type):
        self.__options['type'] = fill_type
        return

    def set_shadow(self, shadow):
        self.__options['shadow'] = shadow
        return

    def set_width(self, width):
        self.__options['width'] = width
        return
