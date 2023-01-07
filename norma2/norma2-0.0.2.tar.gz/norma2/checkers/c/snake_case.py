import os
from typing import List

from norma2.errors.norm import BadFileName, _TemplateNormError
from norma2.parser.cfile import CFile

banned = [chr(i) for i in range(ord("A"), ord("Z") + 1)]


def check_sc(file: CFile) -> List[_TemplateNormError]:
    basename = os.path.basename(file.filepath)
    for char in basename:
        if char in banned:
            return [BadFileName(file.filepath, "no upper case in file name")]
    return []
