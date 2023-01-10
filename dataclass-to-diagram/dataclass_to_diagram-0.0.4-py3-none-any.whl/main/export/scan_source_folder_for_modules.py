"""Сканируем файлы в папке и создаем список потенциальных модулей."""

import logging
import os
from pathlib import Path

from .module_info import ModuleInfo

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


def scan_source_folder_for_modules(
    path_source: Path,
    path_target: Path,
) -> list[ModuleInfo]:
    """Сканируем файлы в папке и создаем список потенциальных модулей."""
    log.info("Начинаем сканировать исходную папку и искать модули")
    modules: list[ModuleInfo] = []
    for dirpath, _, filenames in os.walk(path_source):
        path = Path(dirpath)
        if path.name == "__pycache__":
            continue
        log.debug("Сканирование папки: {0}".format(path))
        for module in filenames:
            if module[-3:] != ".py":
                continue
            if module == "main.py":
                continue
            log.debug("Найден модуль: {0}".format(module))
            modules.append(
                ModuleInfo(
                    path_module=path,
                    filename=module[:-3],
                    path_source=path_source,
                    path_target=path_target,
                ),
            )
    log.info("Найдено модулей: {0}".format(len(modules)))
    return modules
