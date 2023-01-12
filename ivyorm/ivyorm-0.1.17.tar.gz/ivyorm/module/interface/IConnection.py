import abc

class Base(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def _field(self, value):
        pass

    @abc.abstractmethod
    def _order(self, value):
        pass

    @abc.abstractmethod
    def _action(self, value):
        pass

    @abc.abstractmethod
    def _where(self, value):
        pass

    @abc.abstractmethod
    def _table(self, value):
        pass

    @abc.abstractmethod
    def _pagination(self, value):
        pass
