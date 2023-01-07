from typing import List

from norma2.errors.norm import TooManyConditionBranch, _TemplateNormError
from norma2.parser.cfile import CContextType, CFile


def _check_func(
    ctx, file: CFile, nested_level: int, start_ctx: int
) -> List[_TemplateNormError]:
    errs = []
    start_ctx = file.text_origin.index(ctx.matching.matching, start_ctx)
    if nested_level > 3:
        line_nb = file.text_origin.count("\n", 0, start_ctx) + 1
        return [
            TooManyConditionBranch(file.filepath, line_nb, "Too many Branch")
        ]  # noqa: E501
    for ctx1 in ctx.childs:
        errs.extend(_check_func(ctx1, file, nested_level + 1, start_ctx))
    return errs


def check_nb(file: CFile) -> List[_TemplateNormError]:
    errs = []
    for ctx in file.parsed_context:
        if ctx.type != CContextType.FUNCTION:
            continue
        start_ctx = file.text_origin.index(ctx.matching.matching)
        errs.extend(_check_func(ctx, file, 0, start_ctx))
    return errs
