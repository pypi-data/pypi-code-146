"""Экспорт модели ERD в файл .dbml."""

from .database import database_to_dbml
from ..base_exporter import BaseExporter


class Exporter(BaseExporter):
    """Экспорт модели ERD в файл .dbml."""

    @property
    def file_extension(self) -> str:
        """Расширение файла для экспортированной модели."""
        return ".erd.dbml"

    def export(self) -> str:
        """Экспорт модели."""
        return database_to_dbml(self._model)  # type: ignore
