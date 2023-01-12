import abc


class Helpable(abc.ABC):
    @abc.abstractmethod
    def format_help(self, max_cols: int) -> str:
        pass
