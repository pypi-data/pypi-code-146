from __future__ import annotations


class ConstraintsPreProcessor:
    """
    Pre-process constraint strings before parsing
    """

    WINVAL_ANNOTATION = '#@wv'

    def __init__(self, wdl_file: str):
        self.wdl_file = wdl_file

    def process_constraint_strings(self, ) -> list[str]:
        with open(self.wdl_file) as wf:
            lines = wf.readlines()
            return self._process_constraint_strings_from_lines(lines)

    @staticmethod
    def _process_constraint_strings_from_lines(wdl_lines: list[str]) -> list[str]:
        constraints: list[str] = []
        for line in wdl_lines:
            line = line.strip()
            if line.startswith(ConstraintsPreProcessor.WINVAL_ANNOTATION):
                constraints.append(line.replace(ConstraintsPreProcessor.WINVAL_ANNOTATION, '').strip())
        return constraints
