from typing import List

from norma2.errors.norm import LeadingTrailingLine, _TemplateNormError
from norma2.parser._file import _File


def check_line_start(file: _File) -> List[_TemplateNormError]:
    if not file.text_origin:
        return []
    if file.text_origin.startswith("\n"):
        return [LeadingTrailingLine(file.filepath, 1, "No empty line at start of file")]
    return []
