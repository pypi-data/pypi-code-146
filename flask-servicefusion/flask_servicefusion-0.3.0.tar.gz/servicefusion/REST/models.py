

class BaseDataModel(object):
    @property
    def data(self):
        return self.__dict__
