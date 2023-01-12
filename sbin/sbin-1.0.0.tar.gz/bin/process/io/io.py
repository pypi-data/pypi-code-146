import abc


class Io(abc.ABC):
    @abc.abstractmethod
    def text(self, message: str) -> None:
        pass

    @abc.abstractmethod
    def title(self, message: str) -> None:
        pass

    @abc.abstractmethod
    def success(self, message: str) -> None:
        pass

    @abc.abstractmethod
    def error(self, message: str) -> None:
        pass

    @abc.abstractmethod
    def warning(self, message: str) -> None:
        pass
