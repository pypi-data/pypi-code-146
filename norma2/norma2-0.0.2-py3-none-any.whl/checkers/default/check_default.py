from typing import List

from norma2.errors.norm import _TemplateNormError
from norma2.parser.file import DefaultFile


def check(file: DefaultFile) -> List[_TemplateNormError]:
    return []
