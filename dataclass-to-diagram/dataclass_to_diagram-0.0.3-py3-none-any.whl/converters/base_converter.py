"""Базовый конвертер."""

import abc
import logging
from pathlib import Path

from .converters_params import ConvertersParams

log = logging.getLogger(__name__)


class BaseConverter(abc.ABC):
    """Базовый конвертер."""

    def __init__(self, converters_params: ConvertersParams) -> None:
        """Базовый конвертер."""
        self._converters_params = converters_params

    @abc.abstractmethod
    async def convert(self, filepath: Path) -> None:
        """Конвертирование."""

    def _log_convert_completed(self, filepath: Path) -> None:
        log.info("Конвертирование выполнено, создан файл: {0}".format(filepath))
