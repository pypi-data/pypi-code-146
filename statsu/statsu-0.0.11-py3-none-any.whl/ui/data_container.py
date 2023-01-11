from dataclasses import dataclass
import logging
import math
from typing import Any, List, Optional, Tuple, Union
import numpy as np

import pandas as pd
from PySide6.QtGui import QContextMenuEvent
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt


from statsu.data.data_model import PandasModel, ChangeValuesInRectCommand, ChangeValuesIndexCommand
from statsu.ui.design.data_container import Ui_DataContainer
from statsu.ui.user_command import UserCommandManager

logger = logging.getLogger(__name__)

class DataContainer(QWidget, Ui_DataContainer):
    def __init__(
            self,
            data: pd.DataFrame = None,
            name: str = 'Sheet',
            data_path: Optional[str] = None,
            parent: Optional[QWidget] = None
        ) -> None:
        super().__init__(parent)
        self.setupUi(self)

        self.command_manager: UserCommandManager = None

        if data is None:
            data = pd.DataFrame()
        self.raw_data = data
        self.name = name
        self.data_path = data_path

        # 구현된 PandasModel의 필터 기능을 활용하여 긴 데이터는 페이지로 분할
        self.model = PandasModel(data, parent=self)
        self.data_view.setModel(self.model)

    def contextMenuEvent(self, event: QContextMenuEvent) -> None:
        return super().contextMenuEvent(event)

    def set_command_manager(self, manager: UserCommandManager):
        self.command_manager = manager
        self.model.command_manager = manager

    def get_current_selections(self):
        return Selections(self, self.data_view.selectedIndexes())

@dataclass
class RectRange:
    row_top: int
    col_left: int
    height: int
    width: int

    def get_top_left(self) -> Tuple[int, int]:
        return (self.row_top, self.col_left)

    def get_bottom_right(self) -> Tuple[int, int]:
        row = self.row_top + self.height - 1
        col = self.col_left + self.width - 1

        return (row, col)
    
    def get_empty_2d_list(self):
        return [[''] * self.width for _ in range(self.height)]

class Selections:
    def __init__(
            self,
            target: DataContainer,
            selected_indexes: Optional[List[QModelIndex]] = None,
            selected_range: Optional[RectRange] = None
        ) -> None:
        self.target = target
        self.selected_indexes: List[QModelIndex] = []
        self.rect_range = selected_range

        if selected_indexes is not None:
            min_idx = [math.inf, math.inf]
            max_idx = [-1, -1]

            for qm_idx in selected_indexes:
                min_idx[0] = min(min_idx[0], qm_idx.row())
                min_idx[1] = min(min_idx[1], qm_idx.column())
                max_idx[0] = max(max_idx[0], qm_idx.row())
                max_idx[1] = max(max_idx[1], qm_idx.column())

                self.selected_indexes.append(qm_idx)

            self.rect_range = RectRange(
                min_idx[0], 
                min_idx[1], 
                max_idx[0] - min_idx[0] + 1,
                max_idx[1] - min_idx[1] + 1
            )
    
    def get_rect_range_data(self):
        result: List[List[Any]] = self.rect_range.get_empty_2d_list()

        if len(self.selected_indexes) > 0:
            for selection in self.selected_indexes:
                result[selection.row() - self.rect_range.row_top][selection.column() - self.rect_range.col_left] = selection.data(Qt.DisplayRole)
        
        return result
    
    def clear_data(self):
        if len(self.selected_indexes) > 0:
            # for selection in self.selected_indexes:
            #     self.target.raw_data.iloc[selection.row(), selection.column()] = ''
            self.target.command_manager.execute_command(ChangeValuesIndexCommand(
                self.target.raw_data,
                self.selected_indexes,
                ''
            ))
        else:
            tl = self.rect_range.get_top_left()
            br = self.rect_range.get_bottom_right()
            self.target.command_manager.execute_command(ChangeValuesInRectCommand(
                self.target.raw_data,
                tl[0], (br[0] + 1),
                tl[1], (br[1] + 1),
                '',
            ))
            # self.target.raw_data.iloc[tl[0]:(br[0] + 1), tl[1]:(br[1] + 1)] = ''

