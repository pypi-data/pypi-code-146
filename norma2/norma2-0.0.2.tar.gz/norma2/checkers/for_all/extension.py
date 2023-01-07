import fnmatch
from typing import List

from norma2.errors.norm import BadFileExtension, _TemplateNormError
from norma2.parser._file import _File


def check_ext(file: _File) -> List[_TemplateNormError]:
    for glob in file.config.file_extension_banned:
        if fnmatch.fnmatch(file.filepath, glob):
            return [
                BadFileExtension(filepath=file.filepath, msg=f"not accepted: {glob}")
            ]
    return []
