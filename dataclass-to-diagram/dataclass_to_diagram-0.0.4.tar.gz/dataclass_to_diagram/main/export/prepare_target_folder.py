"""Подготовить целевую папку."""

import logging
import os
import shutil
from pathlib import Path

log = logging.getLogger(__name__)


def __ignore_files(directory: str, files: list[str]) -> list[str]:
    """Игнорировать файлы при копировании дерева папок."""
    return [
        file for file in files if os.path.isfile(os.path.join(directory, file))
    ]


def prepare_target_folder(path_source: Path, path_target: Path) -> None:
    """Подготовить целевую папку."""
    log.debug("Удаляем целевую папку")
    shutil.rmtree(path=path_target, ignore_errors=True)
    log.debug("Копируем структуру папок из исходной")
    shutil.copytree(
        src=path_source,
        dst=path_target,
        ignore=__ignore_files,
    )
    # создаем файл пояснения
    with open(
        "{0}/__this_folder_is_automatically_generated__".format(path_target),
        "w",
    ) as desc_file:
        desc_file.write("")
