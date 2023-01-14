from abc import ABC, abstractmethod


class Updatable(ABC):
    @abstractmethod
    def notify(self, message):
        pass

    @abstractmethod
    def get_updatable_id(self) -> str:
        pass
