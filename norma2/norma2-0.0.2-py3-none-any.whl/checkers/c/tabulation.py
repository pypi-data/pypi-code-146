from typing import List

from norma2.errors.norm import BadIndentation, Info, _TemplateNormError
from norma2.parser.cfile import CFile


def check_tab(file: CFile) -> List[_TemplateNormError]:
    errs = []
    lines = file.text_origin_without_text.split("\n")
    for i, line in enumerate(lines):
        if line.startswith("\t"):
            errs.append(
                BadIndentation(
                    file.filepath,
                    i + 1,
                    "must indent using space instead of tabulation",
                )
            )
        elif "\t" in line:
            errs.append(
                Info(
                    file.filepath,
                    i + 1,
                    "please use space instead of \\t in your code",
                )
            )
    return errs
