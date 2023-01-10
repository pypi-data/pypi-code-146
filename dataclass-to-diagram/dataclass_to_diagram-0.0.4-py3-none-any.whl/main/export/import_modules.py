import logging

from .module_info import ModuleInfo

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


def import_modules(potential_modules: list[ModuleInfo]) -> list[ModuleInfo]:
    """Импортирование модулей."""
    log.info("Пробуем импортировать модули")
    imported: list[ModuleInfo] = []
    for mod in potential_modules:
        try:
            mod.try_import()
        except ImportError:
            continue
        log.debug(
            "Успешно импортирован модуль: {0}".format(mod.imported),
        )
        imported.append(mod)
    log.info("Импортировано модулей: {0}".format(len(imported)))
    return imported
