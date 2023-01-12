from pathlib import Path
from typing import List

from gtdblib.file import File


class iTolCollapseFile(File):
    __slots__ = ('data',)

    def __init__(self, path: Path):
        super().__init__(path)
        self.data: List[str] = list()

    def insert(self, node_id: str):
        self.data.append(node_id)

    def write(self):

        with self.path.open('w') as f:
            f.write('\n'.join([
                'COLLAPSE',
                'DATA'
            ] + self.data) + '\n')
