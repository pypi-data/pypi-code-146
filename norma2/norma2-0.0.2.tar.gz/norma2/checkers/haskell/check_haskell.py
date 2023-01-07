from typing import List

from norma2.checkers.haskell.header import check_header
from norma2.errors.norm import _TemplateNormError
from norma2.parser.hsfile import HSFile

checkerss = [
    check_header,
]


def check(file: HSFile) -> List[_TemplateNormError]:
    errs: List[_TemplateNormError] = []
    for checker in checkerss:
        errs.extend(checker(file))
    return errs
