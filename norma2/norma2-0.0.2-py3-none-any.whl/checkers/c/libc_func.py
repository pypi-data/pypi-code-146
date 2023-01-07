import re
from typing import List

from norma2.errors.norm import Info, _TemplateNormError
from norma2.parser.cfile import CFile


def _check_libc_func(file: CFile, line: str, line_nb: int) -> List[_TemplateNormError]:
    errs = []
    for func in file.config.libc_banned_func:
        if re.search(rf"\W{func}\(", line):
            errs.append(Info(file.filepath, line_nb, f"Banned function: {func}"))
    return errs


def check_lf(file: CFile) -> List[_TemplateNormError]:
    errs = []
    splitted = file.text_origin_without_text.split("\n")
    for i, line in enumerate(splitted):
        line = line if "//" not in line else line[: line.index("//")]
        errs.extend(_check_libc_func(file, line, i + 1))
    return errs
