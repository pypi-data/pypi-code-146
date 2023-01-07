from typing import List

from norma2.checkers.c.comma import check_comma
from norma2.checkers.c.comment import check_comment
from norma2.checkers.c.header import check_header
from norma2.checkers.c.indent import check_indent
from norma2.checkers.c.libc_func import check_lf
from norma2.checkers.c.nb_function_per_file import check_nfpf
from norma2.checkers.c.nb_line_per_func import check_nlpf
from norma2.checkers.c.nb_params import check_np
from norma2.checkers.c.nested_branch import check_nb
from norma2.checkers.c.operator import check_op
from norma2.checkers.c.parenthesis import check_parenthesis
from norma2.checkers.c.preprocessor import check_preprocessor
from norma2.checkers.c.snake_case import check_sc
from norma2.checkers.c.statements import check_statements
from norma2.checkers.c.subscriptor import check_subscriptor
from norma2.checkers.c.tabulation import check_tab
from norma2.checkers.c.two_space import check_ts
from norma2.errors.norm import _TemplateNormError
from norma2.parser.cfile import CFile

checkerss = [
    check_nfpf,
    check_tab,
    check_comma,
    check_comment,
    check_nlpf,
    check_header,
    check_indent,
    check_lf,
    check_np,
    check_nb,
    check_op,
    check_parenthesis,
    check_preprocessor,
    check_sc,
    check_statements,
    check_subscriptor,
    check_ts,
]


def check(file: CFile) -> List[_TemplateNormError]:
    err = []
    for check in checkerss:
        cur_err = check(file)
        err.extend(cur_err)
    return err
