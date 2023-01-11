from csv import DictReader
from csv import DictWriter
from pathlib import Path

from .item import Item


def read_items(fileish, itemclass=Item):
    reader = DictReader(fileish, itemclass.schema, delimiter="|")
    return [itemclass.create(i) for i in reader if i]


def write_items(fileish, *items):
    schema = items[0].schema
    writer = DictWriter(fileish, schema, delimiter="|")
    for item in items:
        values = dict([(f, getattr(item, f)) for f in schema])
        writer.writerow(values)


class File:

    def __init__(self, path):
        self._path = path

    def read(self, itemclass=Item):
        if self._path.is_file():
            with open(self._path) as datafile:
                return read_items(datafile, itemclass)
        return []

    def save(self, *items):
        if items:
            with open(self._path, 'w') as datafile:
                write_items(datafile, *items)
        else:
            Path(self._path).write_text('')
