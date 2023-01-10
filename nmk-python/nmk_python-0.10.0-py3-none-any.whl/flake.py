import sys
from typing import List

from nmk.model.builder import NmkTaskBuilder
from nmk.utils import run_with_logs


class FlakeBuilder(NmkTaskBuilder):
    def build(self, src_folders: List[str]):
        # Delegate to flake8
        run_with_logs([sys.executable, "-m", "flake8"] + src_folders, self.logger)

        # Touch output file
        self.main_output.touch()
