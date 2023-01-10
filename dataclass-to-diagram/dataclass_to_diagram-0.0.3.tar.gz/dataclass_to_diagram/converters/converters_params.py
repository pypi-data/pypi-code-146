"""Параметры конвертеров, которые в перспективе можно задавать через консоль."""

from dataclasses import dataclass


@dataclass
class ConvertersParams(object):
    """Параметры конвертеров."""

    kroki_url: str = "https://kroki.io"
