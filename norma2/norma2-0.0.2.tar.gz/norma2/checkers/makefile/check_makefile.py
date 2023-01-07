from typing import List

from norma2.errors.norm import _TemplateNormError
from norma2.parser.makefile import MakeFile


def check(file: MakeFile) -> List[_TemplateNormError]:
    return []
