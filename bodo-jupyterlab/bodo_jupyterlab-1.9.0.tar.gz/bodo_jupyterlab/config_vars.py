from .config import AUTO_ATTACH, CATALOG_MODE


def should_auto_attach():
    return AUTO_ATTACH


def enable_catalog_mode():
    return CATALOG_MODE
