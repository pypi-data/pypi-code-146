from pathlib import Path
from typing import List, Literal

from gtdblib.file import File


class iTolDatasetColorStripFile(File):
    __slots__ = ('data',)

    def __init__(
            self,
            path: Path,
            label: str,
            color: str,
            color_branches: bool = False,
            strip_width: int = 25,
            margin: int = 0,
            border_width: int = 0,
            border_color: str = '#0000ff',
            complete_border: bool = False,
            show_internal: bool = False,
            show_strip_labels: bool = True,
            strip_label_position: Literal['top', 'center', 'bottom'] = 'center',
            strip_label_size_factor: float = 1,
            strip_label_rotation: float = 0,
            strip_label_shift: int = 0,
            strip_label_color: str = '#000000',
            strip_label_outline: float = 0.5,
            show_labels: bool = False,
            size_factor: float = 1,
            label_rotation: float = 0,
            label_shift: float = 0,
    ):
        """
        """
        super().__init__(path)
        self.data: List[str] = [
            'DATASET_COLORSTRIP',
            'SEPARATOR TAB',
            f'DATASET_LABEL\t{label}',
            f'COLOR\t{color}',
            f'COLOR_BRANCHES\t{int(color_branches)}',
            f'STRIP_WIDTH\t{strip_width}',
            f'MARGIN\t{margin}',
            f'BORDER_WIDTH\t{border_width}',
            f'BORDER_COLOR\t{border_color}',
            f'COMPLETE_BORDER\t{int(complete_border)}',
            f'SHOW_INTERNAL\t{int(show_internal)}',
            f'SHOW_STRIP_LABELS\t{int(show_strip_labels)}',
            f'STRIP_LABEL_POSITION\t{strip_label_position}',
            f'STRIP_LABEL_SIZE_FACTOR\t{strip_label_size_factor}',
            f'STRIP_LABEL_ROTATION\t{strip_label_rotation}',
            f'STRIP_LABEL_SHIFT\t{strip_label_shift}',
            f'STRIP_LABEL_COLOR\t{strip_label_color}',
            f'STRIP_LABEL_OUTLINE\t{strip_label_outline}',
            f'SHOW_LABELS\t{int(show_labels)}',
            f'SIZE_FACTOR\t{size_factor}',
            f'LABEL_ROTATION\t{label_rotation}',
            f'LABEL_SHIFT\t{label_shift}',
            'DATA'
        ]

    def insert(self, node_id: str, color: str, label: str, ):
        self.data.append(f'{node_id}\t{color}\t{label}')

    def write(self):
        with self.path.open('w') as f:
            f.write('\n'.join(self.data) + '\n')
