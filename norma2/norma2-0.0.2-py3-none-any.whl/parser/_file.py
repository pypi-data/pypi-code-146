import os
from pathlib import Path
from typing import List

from norma2.config.config_class import Config
from norma2.errors.norm import _TemplateNormError


class _File:
    def __init__(self, filepath: str, config: Config) -> None:
        if not os.path.isfile(filepath):
            raise os.error(f"Invalid filepath: {filepath}")
        self.filepath = filepath
        try:
            self.text_origin = Path(self.filepath).read_text()
        except Exception:
            self.text_origin = ""
        self.lines_origin = []
        self.parsed_context = []
        self.config = config
        self.is_init = False

    def init(self):
        pass

    def check_norm(self) -> List[_TemplateNormError]:
        return []
