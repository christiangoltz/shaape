from sets import Set

class Named(object):
    def __init__(self):
        self.__names = Set([''])
        return
    
    def names(self):
        return self.__names

    def add_name(self, name):
        self.__names.add(name)
        return

    def add_names(self, names):
        self.__names = self.__names.union(names)
