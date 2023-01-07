from typing import List

from norma2.config.config_class import Config
from norma2.parser._file import _File
from norma2.errors.norm import _TemplateNormError

class HSFile(_File):
    def __init__(self, filepath: str, config: Config) -> None:
        super().__init__(filepath, config)

    def init(self):
        if not self.text_origin:
            return
        self.lines_origin = self.text_origin.split("\n")
        self.is_init = True

    def check_norm(self) -> List[_TemplateNormError]:
        return []
