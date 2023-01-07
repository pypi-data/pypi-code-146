import re
from typing import List

from norma2.errors.norm import BadSpace, _TemplateNormError
from norma2.parser.cfile import CFile


def check_comma(file: CFile) -> List[_TemplateNormError]:
    errs = []
    text = file.text_origin_without_text.split("\n")
    for i, line in enumerate(text):
        ll = line if "//" not in line else line[: line.index("//")]
        ll = re.sub("'(.)'", "''", ll)
        m = re.search(r",\S", ll)
        if m:
            errs.append(
                BadSpace(
                    file.filepath, i + 1, f"bad space for comma: `{ll[m.start():]}`"
                )
            )
    return errs
