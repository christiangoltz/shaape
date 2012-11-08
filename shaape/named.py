class Named(object):
    def __init__(self):
        self.__names = []
        return
    
    def names(self):
        return self.__names

    def add_name(self, name):
        self.__names.append(name)
        return
