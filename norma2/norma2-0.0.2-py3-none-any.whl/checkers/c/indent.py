from typing import List

from norma2.errors.norm import BadIndentation, _TemplateNormError
from norma2.parser.cfile import CFile


def check_indent(file: CFile) -> List[_TemplateNormError]:
    errs = []
    for i, line in enumerate(file.lines_origin):
        len_space = 0
        while line and len_space < len(line) and line[len_space] == " ":
            len_space += 1
        if len_space % 4 != 0:
            errs.append(
                BadIndentation(
                    file.filepath, i + 1, "Indentation must be a multiple of 4"
                )
            )
    return errs
