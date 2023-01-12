from pathlib import Path
from typing import List, Optional

from gtdblib.file import File


class iTolTreeColorsFile(File):
    __slots__ = ('data',)

    def __init__(self, path: Path):
        super().__init__(path)
        self.data: List[str] = list()

    def insert_range(
            self, node_id: str, color: str, label: str):
        """defines a colored range (colored background for labels/clade)"""
        self.data.append('\t'.join([node_id, 'range', color, label]))

    def insert_clade(
            self,
            node_id: str,
            color: str,
            branch_style: str,  # Literal['normal', 'dashed']
            scale_factor: float):
        """defines color/style for all branches in a clade"""
        self.data.append('\t'.join([node_id, 'clade', color, branch_style, str(scale_factor)]))

    def insert_branch(
            self,
            node_id: str,
            color: str,
            branch_style: str,  # Literal['normal', 'dashed']
            scale_factor: float):
        """defines color/style for a single branch"""
        self.data.append('\t'.join([node_id, 'branch', color, branch_style, str(scale_factor)]))

    def insert_label(
            self,
            node_id: str,
            color: str,
            font_style: Optional[str] = None,  # Literal['normal', 'bold', 'italic', 'bold-italic']
            scale_factor: Optional[float] = None,
    ):
        """defines font color/style for the leaf label"""
        row = [node_id, 'label', color]
        if font_style is not None:
            row.append(font_style)
        if scale_factor is not None:
            row.append(str(scale_factor))
        self.data.append('\t'.join(row))

    def insert_label_background(self, node_id: str, color: str):
        """defines the leaf label background color"""
        self.data.append('\t'.join([node_id, 'label_background', color]))

    def write(self):
        with self.path.open('w') as f:
            f.write('\n'.join([
                                  'TREE_COLORS',
                                  'SEPARATOR TAB',
                                  'DATA'
                              ] + self.data) + '\n')
