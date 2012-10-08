import copy

class ShaapeStyle(object):
    COLORS = { 'red' : [1, 0, 0], 'green' : [0, 1, 0], 'blue' : [0, 0, 1] }
    DEFAULT_FILL = { 'color' : [0.9, 0.9, 0.9], 'gradient' : 'on' }
    DEFAULT_SHADOW = 'on'
    def __init__(self, names, options):
        self.__names = names
        self.__fill = {}
        self.__shadow = None
        if type(options) == dict:
            option_set = set(options.keys())
            if 'fill' in option_set:
                if type(options['fill']) <> list:
                    options['fill'] = [options['fill']]
                # find colors
                colors = filter(lambda x: x in ShaapeStyle.COLORS.keys(), options['fill']) 
                if len(colors) > 0:
                    self.__fill['color'] = ShaapeStyle.COLORS[colors[0]]
                else:
                    color_lists = [option for option in options['fill'] if len(option) in range(3,5) ]
                    if len(color_lists) > 0:
                        self.__fill['color'] = color_lists[0]

                # find gradient
            if 'shadow' in option_set:
                if options['shadow'] == True:
                    self.__shadow = 'on'
                elif options['shadow'] == False:
                    self.__shadow = 'off'
        return

    def merge(self, style):
        self.__fill = dict(self.__fill.items() + style.fill().items())
        if self.__shadow == None:
            self.__shadow = style.shadow()

    def names(self):
        return self.__names

    def fill(self):
        return  dict(ShaapeStyle.DEFAULT_FILL.items() + self.__fill.items())

    def shadow(self):
        if self.__shadow == None:
            return ShaapeStyle.DEFAULT_SHADOW
        else:
            return self.__shadow

    def set_color(self, color):
        self.__fill['color'] = color
        return
