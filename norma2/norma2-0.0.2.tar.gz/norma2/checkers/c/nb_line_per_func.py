from typing import List

from norma2.errors.norm import FunctionLineNumber, _TemplateNormError
from norma2.parser.cfile import CContextType, CFile


def _check_func(ctx, file: CFile) -> List[_TemplateNormError]:
    start_ctx = file.text_origin.count(
        "\n", 0, file.text_origin.index(ctx.matching.matching)
    )
    func = ctx.matching.matching
    if "{" in func:
        func = func[func.index("{") :]
    if "}" in func:
        func = func[: func.rindex("}")]
    if not func:
        return []
    if func.endswith("\n"):
        func = func[: func.rindex("\n")]
    splitted = func.split("\n")
    if splitted and splitted[0] == "{":
        splitted.pop(0)
    if splitted and splitted[-1] == "}":
        splitted.pop(-1)
    if not splitted:
        return []
    nb_line = len(splitted)
    if nb_line > 20:
        return [FunctionLineNumber(file.filepath, start_ctx, f"{nb_line} > 20")]
    return []


def check_nlpf(file: CFile) -> List[_TemplateNormError]:
    errs = []
    for ctx in file.parsed_context:
        if ctx.type != CContextType.FUNCTION:
            continue
        errs.extend(_check_func(ctx, file))
    return errs
