from typing import List

from norma2.checkers.c import check_c
from norma2.checkers.default import check_default
from norma2.checkers.for_all import check_for_all
from norma2.checkers.makefile import check_makefile
from norma2.checkers.haskell import check_haskell
from norma2.errors.norm import _TemplateNormError
from norma2.parser.cfile import CFile
from norma2.parser.file import DefaultFile, File
from norma2.parser.hsfile import HSFile
from norma2.parser.makefile import MakeFile

choices = {
    CFile: check_c.check,
    DefaultFile: check_default.check,
    MakeFile: check_makefile.check,
    HSFile: check_haskell.check
}


def check(file: File) -> List[_TemplateNormError]:
    errs = []
    for _type, func in choices.items():
        if isinstance(file.file_obj, _type):
            cur_err = func(file.file_obj)
            errs.extend(cur_err)
    errs.extend(check_for_all.check(file.file_obj))
    return errs
