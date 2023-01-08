from PySide6.QtCore import QModelIndex
from PySide6.QtWidgets import QFileSystemModel


def path_from_index(index: QModelIndex, model: QFileSystemModel = None):
    path = []
    while index.isValid():
        if model:
            path.insert(0, model.data(index))
        else:
            path.insert(0, index.data())
        index = index.parent()
    return path


def key_from_value(value, dictionary):
    return next(key for key, val in dictionary.items() if val == value)


def readable_size(size: int):
    """Converts size given in bytes into human-readable string."""
    if not size >> 10:
        return str(size) + ' B'
    elif not size >> 20:
        return str(round(size / 0x400, 2)) + ' kB'
    elif not size >> 30:
        return str(round(size / 0x100000, 2)) + ' MB'
    else:
        return str(round(size / 0x40000000, 2)) + ' GB'
