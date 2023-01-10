import logging
from importlib import import_module
from pathlib import Path
from types import ModuleType

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class ModuleInfo(object):
    """Модуль для импорта."""

    def __init__(
        self,
        path_module: Path,
        filename: str,
        path_source: Path,
        path_target: Path,
    ) -> None:
        """Create ModuleInfo."""
        self.__path_module = path_module
        self.__filename = filename
        self.__path_source = path_source
        self.__path_target = path_target
        self.__imported_module: ModuleType | None = None

    @property
    def imported(self) -> ModuleType | None:
        """Возвращает импортированный модуль."""
        return self.__imported_module

    @property
    def path_module(self) -> Path:
        """Возвращает путь до исходной папки с модулем."""
        return self.__path_module

    @property
    def path_inside_target(self) -> Path:
        """Возвращает путь до целевой папки с изображениями."""
        path_module: str = str(
            self.__path_module.relative_to(self.__path_source),
        )
        return self.__path_target.absolute() / path_module

    def try_import(self: "ModuleInfo") -> None:
        """Попытка импортировать модуль."""
        prefix = self.__path_to_import_prefix()
        if prefix == "":
            module_name = self.__filename
        else:
            module_name = prefix + "." + self.__filename
        log.info("Попытка импорта %s", module_name)
        self.__imported_module = import_module(module_name)

    def __path_to_import_prefix(self: "ModuleInfo") -> str:
        """Путь до модуля в префикс для импорта модуля."""
        return str(self.__path_module.relative_to(".")).replace("/", ".")
