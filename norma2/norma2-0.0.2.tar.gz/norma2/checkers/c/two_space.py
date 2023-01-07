from typing import List

from norma2.errors.norm import BadSpace, _TemplateNormError
from norma2.parser.cfile import CFile

separator = (
    [chr(k) for k in range(ord("a"), ord("z") + 1)]
    + [chr(k) for k in range(ord("A"), ord("Z") + 1)]
    + [chr(k) for k in range(ord("0"), ord("9") + 1)]
)


def _check_line(file: CFile, line: str, line_nb: int):
    if line.endswith("\\"):
        return []
    e = 0
    while e < len(line) and line[e] not in separator:
        e += 1
    if "  " in line[e:] and "#define " not in line[e:]:
        return [
            BadSpace(
                file.filepath,
                line_nb,
                "two space next each other (maybe you need to remove one)",
            )
        ]
    return []


def check_ts(file: CFile) -> List[_TemplateNormError]:
    errs = []
    is_in_comment = False
    lines = file.text_origin_without_text.split("\n")
    for i, line in enumerate(lines):
        line = line if "//" not in line else line[: line.index("//")]
        line = line if "/*" not in line else line[: line.index("/*")]
        if is_in_comment:
            is_in_comment = "*/" not in line
        else:
            errs_1 = _check_line(file, line, i + 1)
            errs.extend(errs_1)
    return errs
