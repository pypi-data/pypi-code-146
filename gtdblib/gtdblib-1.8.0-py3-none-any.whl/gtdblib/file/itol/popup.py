from pathlib import Path
from typing import List

from gtdblib.file import File


class iTolPopupFile(File):
    __slots__ = ('data',)

    def __init__(self, path: Path):
        super().__init__(path)
        self.data: List[str] = list()

    def insert(self, node_id: str, title: str, content: str):
        self.data.append(f'{node_id}\t{title}\t{content}')

    def write(self):
        with self.path.open('w') as f:
            f.write('\n'.join([
                                  'POPUP_INFO',
                                  'SEPARATOR TAB',
                                  'DATA'
                              ] + self.data) + '\n')
