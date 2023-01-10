from ..base_exporter import BaseExporter

from .c4_to_puml import c4_to_puml


class Exporter(BaseExporter):
    @property
    def file_extension(self) -> str:
        return ".c4.puml"

    def export(self) -> str:
        return c4_to_puml(self._model)
