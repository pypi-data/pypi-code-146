from pathlib import Path
from typing import List, Literal

from gtdblib.file import File


class iTolDatasetTextFile(File):
    __slots__ = ('data',)

    def __init__(
            self,
            path: Path,
            label: str,
            color: str,
            margin: int = 0,
            show_internal: bool = False,
            label_rotation: float = 0,
            labels_below: bool = True,
            vertical_shift: int = 0,
            straight_labels: bool = False,
            align_to_tree: bool = False,
            size_factor: float = 1,
            external_label_shift: int = 0,
            show_labels: bool = False,
            label_size_factor: float = 1,
            label_shift: int = 0,
    ):
        """
        :param label: Used in the legend table.
        :param color: Used in the legend table.
        :param margin: left margin, used to increase/decrease the spacing to the next dataset. Can be negative, causing datasets to overlap. Used only for text labels which are displayed on the outside
        :param show_internal: applies to external text labels only; if set, text labels associated to internal nodes will be displayed even if these nodes are not collapsed. It could cause overlapping in the dataset display.
        :param label_rotation: Rotate all labels by the specified angle
        :param labels_below: By default, internal labels will be placed above the branches. If LABELS_BELOW is set to 1, labels will be below the branches
        :param vertical_shift: Shift internal labels vertically by this amount of pixels (positive or negative)
        :param straight_labels: If set to 1, tree rotation will not influence the individual label rotation
        :param align_to_tree: applies to external text labels only; If set to 1, labels will be displayed in arcs aligned to the tree (in circular mode) or vertically (in normal mode). All rotation parameters (global or individual) will be ignored.
        :param size_factor: font size factor; For external text labels, default font size will be slightly less than the available space between leaves, but you can set a multiplication factor here to increase/decrease it (values from 0 to 1 will decrease it, values above 1 will increase it)
        :param external_label_shift: add extra horizontal shift to the external labels. Useful in unrooted display mode to shift text labels further away from the node labels.
        :param show_labels: display or hide the dataset label above the external labels column
        :param label_size_factor: dataset label size factor
        :param label_shift: dataset label shift in pixels (positive or negative)
        """
        super().__init__(path)
        self.data: List[str] = [
            'DATASET_TEXT',
            'SEPARATOR TAB',
            f'DATASET_LABEL\t{label}',
            f'COLOR\t{color}',
            f'MARGIN\t{margin}',
            f'SHOW_INTERNAL\t{int(show_internal)}',
            f'LABEL_ROTATION\t{label_rotation}',
            f'LABELS_BELOW\t{int(labels_below)}',
            f'VERTICAL_SHIFT\t{vertical_shift}',
            f'STRAIGHT_LABELS\t{int(straight_labels)}',
            f'ALIGN_TO_TREE\t{int(align_to_tree)}',
            f'SIZE_FACTOR\t{size_factor}',
            f'EXTERNAL_LABEL_SHIFT\t{external_label_shift}',
            f'SHOW_LABELS\t{int(show_labels)}',
            f'LABEL_SIZE_FACTOR\t{label_size_factor}',
            f'LABEL_SHIFT\t{label_shift}',
            'DATA'
        ]

    def insert(
            self,
            node_id: str,
            label: str,
            position: float,
            color: str,
            style: Literal['normal', 'bold', 'italic', 'bold-italic'],
            size_factor: float,
            rotation: float
    ):
        """

        #position defines the position of the text label on the tree:
#  -1 = external label
#  a number between 0 and 1 = internal label positioned at the specified valu
e along the node branch (for example, position 0 is exactly at
the start of node branch, position 0.5 is in the middle, and position 1 is at the end)

'normal',''bold','italic' or 'bold-italic'
        """
        # #ID,label,position,color,style,size_factor,rotation

        if not (position == -1 or (0 <= position <= 1)):
            raise ValueError(f'Invalid position: {position}')
        self.data.append(f'{node_id}\t{label}\t{position}\t{color}\t{style}\t{size_factor}\t{rotation}')

    def write(self):
        with self.path.open('w') as f:
            f.write('\n'.join(self.data) + '\n')
