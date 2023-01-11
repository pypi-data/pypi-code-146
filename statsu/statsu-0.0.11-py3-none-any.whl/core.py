import logging
import sys
from dataclasses import dataclass
from typing import List

import pandas as pd
from PySide6.QtGui import QKeySequence
from PySide6.QtWidgets import QApplication

from statsu.actions.action_edit import ActionEdit
from statsu.actions.action_file import ActionFile
from statsu.ui.data_container import DataContainer
from statsu.ui.main_window import MainWindow
from statsu.ui.user_command import UserCommandManager

logging.basicConfig(
    format='%(asctime)s %(name)s [%(levelname)s] %(message)s',
    datefmt='%Y/%m/%d %H:%M:%S',
    level=logging.INFO
)

logger = logging.getLogger(__name__)
app = QApplication(sys.argv)

@dataclass
class DataObject:
    data_frame_origin: pd.DataFrame
    name: str = 'Data'

    def __post_init__(self):
        self.data_frame = self.data_frame_origin.copy()


@dataclass
class WindowSettings:
    in_memory_target: List[DataObject]


class WindowUnit:
    def __init__(self, in_memory_data: List[DataObject] = None) -> None:
        self.main_window = MainWindow()
        self.settings = WindowSettings(in_memory_data)

        if self.settings.in_memory_target is not None:
            for data_obj in in_memory_data:
                data_container = DataContainer(
                    data=data_obj.data_frame,
                    name=data_obj.name + ' (In Memory)',
                    data_path='_Internal'
                )
                self.main_window.add_sheet(data_container)

        self._action_file = ActionFile(self.main_window, self.settings)
        self.main_window.action_file_new.triggered.connect(self._action_file.create_new_sheet)
        self.main_window.action_file_open.triggered.connect(self._action_file.create_sheet_from_file)
        self.main_window.action_file_close.triggered.connect(self._action_file.close_window)
        self.main_window.action_file_save.triggered.connect(self._action_file.save_sheet)
        self.main_window.action_file_save_as.triggered.connect(self._action_file.save_sheet_as)
        self.main_window.action_file_new.setShortcut(QKeySequence.StandardKey.New)
        self.main_window.action_file_open.setShortcut(QKeySequence.StandardKey.Open)
        self.main_window.action_file_save.setShortcut(QKeySequence.StandardKey.Save)
        self.main_window.action_file_save_as.setShortcut(QKeySequence.StandardKey.SaveAs)
        self.main_window.action_file_close.setShortcut(QKeySequence.StandardKey.Close)

        self._action_edit = ActionEdit(self.main_window, self.settings)
        self.main_window.action_edit_undo.triggered.connect(self._action_edit.undo)
        self.main_window.action_edit_redo.triggered.connect(self._action_edit.redo)
        self.main_window.action_edit_copy.triggered.connect(self._action_edit.copy_data)
        self.main_window.action_edit_paste.triggered.connect(self._action_edit.paste_data)
        self.main_window.action_edit_cut.triggered.connect(self._action_edit.cut_data)
        self.main_window.action_edit_undo.setShortcut(QKeySequence.StandardKey.Undo)
        self.main_window.action_edit_redo.setShortcut(QKeySequence.StandardKey.Redo)
        self.main_window.action_edit_cut.setShortcut(QKeySequence.StandardKey.Cut)
        self.main_window.action_edit_copy.setShortcut(QKeySequence.StandardKey.Copy)
        self.main_window.action_edit_paste.setShortcut(QKeySequence.StandardKey.Paste)

    def show(self) -> None:
        self.main_window.show()

    def update(self) -> None:
        self.main_window.update()


def show(input_data: pd.DataFrame = None, name: str = None) -> pd.DataFrame:
    if input_data is not None:
        window = WindowUnit(
            in_memory_data=[DataObject(input_data, name=name if name is not None else 'Data')]
        )
    else:
        window = WindowUnit()

    window.show()
    app.exec()

def show_list(input_data: List[pd.DataFrame]):
    window = WindowUnit([DataObject(data) for data in input_data])
    window.show()
    app.exec()

def show_list_with_name(input_data: List[DataObject]):
    window = WindowUnit(input_data)
    window.show()
    app.exec()
        
