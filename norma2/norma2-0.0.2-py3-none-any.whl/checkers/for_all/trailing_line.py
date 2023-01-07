from typing import List

from norma2.errors.norm import LeadingTrailingLine, _TemplateNormError
from norma2.parser._file import _File


def check_line_end(file: _File) -> List[_TemplateNormError]:
    if not file.text_origin:
        return []
    if file.text_origin.endswith("\n\n"):
        return [
            LeadingTrailingLine(
                file.filepath,
                file.text_origin.count("\n"),
                "No 2 empty line at end of file",
            )
        ]
    if not file.text_origin.endswith("\n"):
        return [
            LeadingTrailingLine(
                file.filepath,
                file.text_origin.count("\n"),
                "End of file must be with a \\n",
            )
        ]
    return []
