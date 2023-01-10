r"""Sprite.

Для генерации перечислений на основе списка файлов:

- клонировать репозиторий с библиотекой
https://github.com/tupadr3/plantuml-icon-font-sprites.git

- в папке с файлами библиотеки создать файл _generate.py:
-------------------------------------------------------------------------------

import os

OUT_FILENAME = "_enum.txt"
SCRIPT_FILENAME = "_generate.py"

sprites: set[str] = set()
for _, _, filenames in os.walk(os.getcwd()):
    for filename in filenames:
        if filename in [OUT_FILENAME, SCRIPT_FILENAME]:
            continue
        sprite = filename.split(".")[0]
        if sprite[0].isdigit():
            sprite = "_" + sprite
        sprites.add(sprite)

with open(OUT_FILENAME, "w", encoding="utf-8") as stream:
    for sprite in sorted(sprites):
        line = f'    {sprite.lower()} = "{sprite}"\n'
        stream.write(line)

-------------------------------------------------------------------------------
- запустить командой python3 _generate.py
- содержимое файла _enum.txt вставить в перечиление
"""


from .devicons import Devicons
from .devicons2 import Devicons2
from .font_awesome_5 import FontAwesome5

__all__ = [
    "Devicons",
    "Devicons2",
    "FontAwesome5",
]
