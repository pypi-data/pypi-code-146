from pathlib import Path

from .interfaces import Words
from .words import ConfigWords
from .words import FileWords


def sort_words(files: list[Path]) -> bool:
    affected = False
    json_files: list[Words] = [ConfigWords(), *[FileWords(path) for path in files]]
    for json_file in json_files:
        dictionary = json_file.get()
        sorted_dictionary = sorted(set(dictionary))
        if dictionary != sorted_dictionary:
            json_file.set(sorted_dictionary)
            affected = True
    return affected
