from ..base_exporter import BaseExporter
from .diagram_to_puml import diagram_to_puml


class Exporter(BaseExporter):
    """Экспорт модели ERD в файл .dbml."""

    @property
    def file_extension(self) -> str:
        """Расширение файла для экспортированной модели."""
        return ".state.puml"

    def export(self) -> str:
        """Экспорт модели."""
        return diagram_to_puml(self._model)
