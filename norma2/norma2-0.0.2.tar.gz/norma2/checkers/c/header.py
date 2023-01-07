from typing import List

from norma2.errors.norm import FileHeader, _TemplateNormError
from norma2.parser.cfile import CFile


def check_header(file: CFile) -> List[_TemplateNormError]:
    lines = file.lines_origin[:]
    if len(lines) < 6:
        return [FileHeader(file.filepath, 0, "No header..")]
    if lines[0] != "/*":
        return [FileHeader(file.filepath, 1, "No header..")]
    if not lines[1].startswith("** EPITECH PROJECT, "):
        return [
            FileHeader(file.filepath, 2, "line must starts with `** EPITECH PROJECT, `")
        ]
    if len(lines[2]) < 4 or not lines[2].startswith("** "):
        return [FileHeader(file.filepath, 3, "line must starts with `** `")]
    if lines[3] != "** File description:":
        return [FileHeader(file.filepath, 4, "line must be `** File description:`")]
    i = 4
    while i < len(lines) and lines[i] != "*/":
        if len(lines[i]) < 4 or not lines[i].startswith("** "):
            return [FileHeader(file.filepath, i + 1, "line must starts with `** `")]
        i += 1
    if i >= len(lines):
        return [FileHeader(file.filepath, i + 1, "File with only header ?")]
    if lines[i] != "*/":
        return [FileHeader(file.filepath, i + 1, "line must be `*/`")]
    return []
