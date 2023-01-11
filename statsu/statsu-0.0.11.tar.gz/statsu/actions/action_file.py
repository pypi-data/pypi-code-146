import logging
from typing import Tuple

import pandas as pd
from PySide6.QtWidgets import QFileDialog

from statsu.data.file_manager import load_dataframe_from_file, save_data_to_file
from statsu.actions.action_base import ActionBase
from statsu.ui.data_container import DataContainer

logger = logging.getLogger(__name__)


class ActionFile(ActionBase):

    def create_new_sheet(self):
        sheet_name = f'Sheet {self.main_window.main_data_tab_widget.count()}'
        sheet = DataContainer(name=sheet_name)
        self.main_window.add_sheet(sheet)

    def create_sheet_from_file(self):
        file_path: Tuple[str, str] = QFileDialog.getOpenFileName(
            parent=self.main_window, 
            caption='Export file', 
            dir='./'
        )

        if file_path[0] != '':
            raw: pd.DataFrame = load_dataframe_from_file(file_path[0])
            if raw is not None:
                container = DataContainer(
                    data=raw,
                    data_path=file_path[0],
                    name=file_path[0].split('.')[-2].split('/')[-1])
                self.main_window.add_sheet(container)

    def save_sheet(self):
        target = self.main_window.get_current_data_container()
        if target.data_path == '_Internal':
            self.window_settings.in_memory_target = target.raw_data
        elif target is not None:
            is_successed = save_data_to_file(
                self.main_window.get_current_data_container(),
                target.data_path,
                target.data_path.split('.')[-1])
            if is_successed == False:
                raise Exception('Save failed: path may have problem')
        else:
            self.save_sheet_as()

    def save_sheet_as(self):
        file_path: Tuple[str, str] = QFileDialog.getSaveFileName(
            parent=self.main_window,
            caption='Export file',
            dir='./',
            filter='Excel File (*.xlsx);;CSV File (*.csv)',
            selectedFilter='Excel File (*.xlsx)'
        )

        if file_path[0] != '':
            target = self.main_window.get_current_data_container()

            if file_path[1] == 'Excel File (*.xlsx)':
                path_str = file_path[0] if file_path[0][-5:] == '.xlsx' else file_path[0] + '.xlsx'
                save_data_to_file(target, path_str, 'xlsx')
            elif file_path[1] == 'CSV File (*.csv)':
                path_str = file_path[0] if file_path[0][-4:] == '.csv' else file_path[0] + '.csv'
                save_data_to_file(target, path_str, 'csv')
            else:
                raise Exception('Unknown file type')

            raw: pd.DataFrame = target.raw_data.copy()
            container = DataContainer(
                data=raw,
                data_path=file_path[0],
                name=file_path[0].split('.')[-2].split('/')[-1])
            self.main_window.add_sheet(container)

    def close_window(self):
        self.main_window.close()
