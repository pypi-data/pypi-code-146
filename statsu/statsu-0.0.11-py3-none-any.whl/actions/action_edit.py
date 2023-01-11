import logging
import math
from typing import List, Optional

import pandas as pd
from PySide6.QtCore import QModelIndex, Qt
from PySide6.QtWidgets import QApplication, QMainWindow

from statsu.actions.action_base import ActionBase
from statsu.data.data_model import ChangeValuesInRectCommand
from statsu.ui.data_container import Selections

logger = logging.getLogger(__name__)

class ActionEdit(ActionBase):
    def undo(self):
        self.main_window.command_manager.undo_command()
        self.main_window.get_current_data_container().model.refresh_layout()

    def redo(self):
        self.main_window.command_manager.redo_command()
        self.main_window.get_current_data_container().model.refresh_layout()

    def cut_data(self):
        container = self.main_window.get_current_data_container()
        selections = container.get_current_selections()

        self.copy_data(selections=selections)

        selections.clear_data()

        container.model.refresh_layout()

    def copy_data(self, *args, selections: Optional[Selections] = None):
        if selections is None:
            selections = self.main_window.get_current_data_container().get_current_selections()

        result: List[List[str]] = selections.get_rect_range_data()
        result_text = '\r\n'.join(['\t'.join(item) for item in result])

        QApplication.clipboard().setText(result_text)

    def paste_data(self):
        container = self.main_window.get_current_data_container()
        min_y, min_x = container.get_current_selections().rect_range.get_top_left()

        data_text = QApplication.clipboard().text()
        data = [row.split('\t') for row in data_text.split('\r\n')]

        origin = container.raw_data.iloc[min_y:min_y + len(data), min_x:min_x + len(data[0])]

        for idx, (_, row) in enumerate(origin.iterrows()):
            for n in range(len(data[idx])):
                if data[idx][n] == '':
                    data[idx][n] = row.iloc[n]

        self.main_window.command_manager.execute_command(
            ChangeValuesInRectCommand(container.raw_data,
                                min_y, min_y + len(data),
                                min_x, min_x + len(data[0]),
                                data,
                                desc='Paste values'))
        self.main_window.get_current_data_container().model.refresh_layout()