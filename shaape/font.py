class Font(object):
    DEFAULT_NAME = 'Monospace 10'

    def __init__(self):
        self.__name = self.DEFAULT_NAME

    def name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name
