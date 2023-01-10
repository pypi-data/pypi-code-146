"""Конвертирование диаграмм баз данных с помощью dbml-renderer."""

import logging
from pathlib import Path
from typing import Final

from dataclass_to_diagram.shared.run_process_async import run_process_async

from .base_converter import BaseConverter

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


COMMAND: Final[str] = "dbml-renderer -i {input} -o {output}"


class DbmlConverter(BaseConverter):
    """Конвертирование dbml."""

    async def convert(self, filepath: Path) -> None:
        """Конвертирование."""
        converted_path = filepath.with_suffix("").with_suffix(".svg")
        await run_process_async(
            COMMAND.format(input=filepath, output=converted_path),
        )
        self._log_convert_completed(converted_path)
