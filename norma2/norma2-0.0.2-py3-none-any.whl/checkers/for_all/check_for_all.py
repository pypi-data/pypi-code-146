from typing import List

from norma2.checkers.for_all.columns import check_nbcol
from norma2.checkers.for_all.extension import check_ext
from norma2.checkers.for_all.leading_line import check_line_start
from norma2.checkers.for_all.trailing_line import check_line_end
from norma2.checkers.for_all.trailing_space import check_space
from norma2.errors.norm import _TemplateNormError
from norma2.parser._file import _File

checkerss = [
    check_line_start,
    check_space,
    check_line_end,
    check_nbcol,
    check_ext,
]


def check(file: _File) -> List[_TemplateNormError]:
    errs: List[_TemplateNormError] = []
    for checker in checkerss:
        errs.extend(checker(file))
    return errs
