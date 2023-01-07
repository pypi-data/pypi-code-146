from typing import List

from norma2.errors.norm import TrailingSpace, _TemplateNormError
from norma2.parser._file import _File


def check_space(file: _File) -> List[_TemplateNormError]:
    if not file.text_origin:
        return []
    errs: List[_TemplateNormError] = []
    splitted = file.text_origin.split("\n")
    for i, line in enumerate(splitted):
        if line.endswith((" ", "\t")):
            errs.append(TrailingSpace(file.filepath, i + 1, f"({line})"))
    return errs
