"""Базовый класс для экспорта модели в текстовое представление."""

import abc

from dataclass_to_diagram.models import BaseModel


class BaseExporter(abc.ABC):
    """Базовый класс для экспорта модели в текстовое представление."""

    def __init__(self, model: BaseModel) -> None:
        """Базовый класс для экспорта модели в текстовое представление."""
        self._model = model

    @abc.abstractproperty
    def file_extension(self) -> str:
        """Расширение файла для экспортированной модели."""
        raise NotImplementedError

    @abc.abstractmethod
    def export(self) -> str:
        """Экспорт модели."""
        raise NotImplementedError
