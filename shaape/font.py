class Font(object):
    def __init__(self, name = 'Monospace 10'):
        self.__name = name

    def name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name
