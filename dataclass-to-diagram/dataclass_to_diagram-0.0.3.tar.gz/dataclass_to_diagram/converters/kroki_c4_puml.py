import logging
from pathlib import Path

from dataclass_to_diagram.exceptions import ConverterError

from .base_converter import BaseConverter
from .kroki_request import kroki_request, OutputFormat

log = logging.getLogger(__name__)


class KrokiC4Converter(BaseConverter):
    """Конвертирование диаграмм C4 с помощью kroki.io."""

    async def convert(self, filepath: Path) -> None:
        """Конвертирование."""
        diagram_source: str = self._read_file(filepath)
        output_formats: list[OutputFormat] = ["png", "svg"]
        for output_format in output_formats:
            converted_path = filepath.with_suffix("").with_suffix(
                suffix=".{0}".format(output_format),
            )
            await self._convert_and_save(
                converted_path=converted_path,
                diagram_source=diagram_source,
                output_format=output_format,
            )

    def _read_file(self, filepath: Path) -> str:
        with open(filepath) as stream:
            diagram_source = stream.read()
        return diagram_source

    async def _convert_and_save(
        self,
        converted_path: Path,
        diagram_source: str,
        output_format: OutputFormat,
    ) -> None:
        try:
            response = await kroki_request(
                diagram_source=diagram_source,
                diagram_type="plantuml",
                output_format=output_format,
                kroki_url=self._converters_params.kroki_url,
            )
        except ConverterError:
            return
        with open(converted_path, "wb") as stream:
            stream.write(response)
        self._log_convert_completed(converted_path)
