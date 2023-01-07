from typing import List

from norma2.config.config_class import Config
from norma2.errors.norm import _TemplateNormError
from norma2.parser._file import _File
from norma2.parser.cfile import CFile
from norma2.parser.hsfile import HSFile
from norma2.parser.makefile import MakeFile


class DefaultFile(_File):
    def __init__(self, filepath: str, config: Config) -> None:
        super().__init__(filepath, config)

    def init(self):
        self.is_init = True

    def check_norm(self) -> List[_TemplateNormError]:
        return []


class File:
    def __init__(self, filepath: str, config: Config):
        self.file_obj: _File
        if filepath.endswith((".c", ".h")):
            self.file_obj = CFile(filepath, config)
        elif filepath.endswith("Makefile"):
            self.file_obj = MakeFile(filepath, config)
        elif filepath.endswith(".hs"):
            self.file_obj = HSFile(filepath, config)
        else:
            self.file_obj = DefaultFile(filepath, config)

    def init(self):
        self.file_obj.init()

    def check_norm(self) -> List[_TemplateNormError]:
        return self.file_obj.check_norm()
