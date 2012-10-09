import copy

class ShaapeStyle(object):
    COLORS = { 'red' : [1, 0, 0], 'green' : [0, 1, 0], 'blue' : [0, 0, 1] }
    DEFAULT_FILL = { 'color' : [0.9, 0.9, 0.9, 1], 'type' : 'gradient' }
    DEFAULT_LINE = { 'width' : 1, 'color' : [0,0,0,1], 'type': 'solid' }
    DEFAULT_SHADOW = 'on'
    def __init__(self, names, options):
        self.__names = names
        self.__fill = {}
        self.__line = {}
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
                
                for option in options['fill']:
                    if option == 'flat':
                        self.set_fill_type('flat')
                    elif options == 'gradient':
                        self.set_fill_type('gradient')
                
            if 'line' in option_set:
                if type(options['line']) <> list:
                    options['line'] = [options['line']]
                # find colors
                colors = filter(lambda x: x in ShaapeStyle.COLORS.keys(), options['line']) 
                if len(colors) > 0:
                    self.__line['color'] = ShaapeStyle.COLORS[colors[0]]
                else:
                    color_lists = [option for option in options['line'] if type(option) == list and len(option) in range(3,5) ]
                    if len(color_lists) > 0:
                        self.__line['color'] = color_lists[0]
                
                for option in options['line']:
                    if type(option) == float or type(option) == int:
                        self.set_line_width(option)

                # find gradient
            if 'shadow' in option_set:
                if options['shadow'] == True:
                    self.__shadow = 'on'
                elif options['shadow'] == False:
                    self.__shadow = 'off'
        return

    def set_default(style):
        ShaapeStyle.DEFAULT_FILL = style.fill()
        ShaapeStyle.DEFAULT_LINE = style.line()
        ShaapeStyle.DEFAULT_SHADOW = style.shadow()
        return

    def merge(self, style):
        self.__fill = dict(self.__fill.items() + style.fill().items())
        self.__line = dict(self.__line.items() + style.line().items())
        if self.__shadow == None:
            self.__shadow = style.shadow()

    def names(self):
        return self.__names

    def fill(self):
        return  dict(ShaapeStyle.DEFAULT_FILL.items() + self.__fill.items())

    def line(self):
        return  dict(ShaapeStyle.DEFAULT_LINE.items() + self.__line.items())

    def shadow(self):
        if self.__shadow == None:
            return ShaapeStyle.DEFAULT_SHADOW
        else:
            return self.__shadow

    def set_fill_color(self, color):
        self.__fill['color'] = color
        return

    def set_fill_type(self, fill_type):
        self.__fill['type'] = fill_type
        return

    def set_line_width(self, width):
        self.__line['width'] = width
        return
