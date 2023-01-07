from typing import List

from norma2.errors.norm import FunctionParametersNumber, _TemplateNormError
from norma2.parser.cfile import CContextType, CFile


def _check_func(ctx, file: CFile) -> List[_TemplateNormError]:
    start_ctx = file.text_origin.count(
        "\n", 0, file.text_origin.index(ctx.matching.matching)
    )
    line = ctx.matching.matching
    line = line if "{" not in line else line[: line.index("{")]
    nb_params = line.count(",")
    if nb_params > 4:
        return [FunctionParametersNumber(file.filepath, start_ctx, f"{nb_params} > 4")]
    return []


def check_np(file: CFile) -> List[_TemplateNormError]:
    errs = []
    for ctx in file.parsed_context:
        if ctx.type != CContextType.FUNCTION:
            continue
        errs.extend(_check_func(ctx, file))
    return errs
