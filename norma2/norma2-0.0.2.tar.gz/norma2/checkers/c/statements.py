from typing import List

from norma2.errors.norm import ManyStatementOnLine, _TemplateNormError
from norma2.parser.cfile import CFile

banned = [chr(i) for i in range(ord("A"), ord("Z") + 1)]


def check_statements(file: CFile) -> List[_TemplateNormError]:
    errs = []
    for i, line in enumerate(file.text_origin_without_text.split("\n")):
        line = line if "//" not in line else line[: line.index("//")]
        nb = line.count(";")
        if nb > 1 and "for" not in line:
            errs.append(
                ManyStatementOnLine(
                    file.filepath, i + 1, "only one statement on line authorized"
                )
            )
    return errs
