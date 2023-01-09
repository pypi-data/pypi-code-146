from abc import abstractmethod


class IIndexFormatter:

    @abstractmethod
    def getIndex(self) -> str:
        raise NotImplementedError
