from typing import List

from norma2.errors.norm import BadSpace, _TemplateNormError
from norma2.parser.cfile import CFile

banned = [chr(i) for i in range(ord("A"), ord("Z") + 1)]


def check_subscriptor(file: CFile) -> List[_TemplateNormError]:
    errs = []
    for i, line in enumerate(file.text_origin_without_text.split("\n")):
        line = line if "//" not in line else line[: line.index("//")]
        if "[ " in line or " ]" in line:
            errs.append(BadSpace(file.filepath, i + 1, "no space after [ or before ]"))
    return errs
