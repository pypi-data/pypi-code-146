from typing import List

from norma2.errors.norm import CommentInFunction, Info, _TemplateNormError
from norma2.parser.cfile import CContextType, CFile
from norma2.regexs import r_text


def _check_inside_func(ctx, file: CFile) -> List[_TemplateNormError]:
    errs = []
    start_ctx = file.text_origin.count(
        "\n", 0, file.text_origin.index(ctx.matching.matching)
    )
    splitted = r_text.sub(ctx.matching.matching, "")
    if not splitted:
        return []
    splitted = splitted.split("\n")
    for i, line in enumerate(splitted):
        if "//" in line:
            errs.append(
                CommentInFunction(
                    file.filepath, i + start_ctx + 1, "no comment inside function"
                )
            )
    return errs


def check_comment(file: CFile) -> List[_TemplateNormError]:
    errs = []
    for ctx in file.parsed_context:
        if ctx.type == CContextType.FUNCTION:
            errs.extend(_check_inside_func(ctx, file))
    for i, line in enumerate(file.lines_origin):
        if line.startswith(" "):
            start = line.strip(" \t")
            if start and start.startswith(("//", "*/")):
                errs.append(
                    Info(
                        file.filepath,
                        i + 1,
                        "comment need to start at first column of line",
                    )
                )
    return errs
