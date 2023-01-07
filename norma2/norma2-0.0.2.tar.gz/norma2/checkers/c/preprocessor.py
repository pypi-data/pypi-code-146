from typing import List

from norma2.errors.norm import Info, PreprocessorIndent, _TemplateNormError
from norma2.parser.cfile import CFile


def check_preprocessor(file: CFile) -> List[_TemplateNormError]:
    errs = []
    indent = 0
    for i, line in enumerate(file.lines_origin):
        text = " ".join(line.split())
        if text.startswith("#if"):
            indent += 4
        elif text.startswith("#endif"):
            indent -= 4
        elif text.startswith("#") and not line.startswith(" " * indent):
            errs.append(
                PreprocessorIndent(
                    file.filepath, i + 1, f"# need {indent} space before"
                )
            )
        if indent < 0:
            errs.append(Info(file.filepath, i + 1, "need an #if before an #endif"))
            indent = 0
        if text.startswith("#define") and file.filepath.endswith(".c"):
            errs.append(Info(file.filepath, i + 1, "no #define in .c file"))
        text_without_comment = text if "//" not in text else text[: text.index("//")]
        if text.startswith("#include") and text_without_comment.endswith(
            (".c>", '.c"')
        ):
            errs.append(Info(file.filepath, i + 1, "don't include .c file"))
    return errs
