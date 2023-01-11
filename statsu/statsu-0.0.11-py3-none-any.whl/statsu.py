import logging
import sys
from typing import List, Tuple

import pandas as pd
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog
from PySide6.QtCore import Qt

from statsu.data.file_manager import load_dataframe_from_file
from statsu.ui.data_container import DataContainer
from statsu.ui.design.main_window import Ui_MainWindow

logging.basicConfig(
    format='%(asctime)s %(name)s [%(levelname)s] %(message)s',
    datefmt='%Y/%m/%d %H:%M:%S',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

app = QApplication(sys.argv)


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)

        self.action_file_new.triggered.connect(self.create_new)
        self.action_file_open.triggered.connect(self.load_sheet)
        self.action_file_close.triggered.connect(self.close)
        self.action_edit_copy.triggered.connect(self.copy_data)
        self.action_edit_paste.triggered.connect(self.paste_data)

    def add_sheet(self, sheet: DataContainer):
        idx = self.main_data_tab_widget.addTab(sheet, sheet.name)
        self.main_data_tab_widget.setCurrentIndex(idx)

    def get_current_data_container(self) -> DataContainer:
        return self.main_data_tab_widget.currentWidget()

    def create_new(self):
        sheet_name = f'Sheet {self.main_data_tab_widget.count()}'
        sheet = DataContainer(name=sheet_name)
        self.add_sheet(sheet)

    def load_sheet(self):
        file_path: Tuple[str, str] = QFileDialog.getOpenFileName(
            self, 'Import file', './')
        if file_path[0] != '':
            raw: pd.DataFrame = load_dataframe_from_file(file_path[0])
            if raw is not None:
                container = DataContainer(data=raw)
                self.add_sheet(container)
                print(container.raw_data)

    def copy_data(self):
        selections = self.get_current_data_container().data_view.selectedIndexes()
        selections.sort()

        result: List[List] = []
        prev_selection = None

        for selection in selections:
            # logger.info(f'Row: {selection.row()}, Col: {selection.column()} => {selection.data(Qt.DisplayRole)}')
            if prev_selection is None or prev_selection.row() != selection.row():
                result.append([])

            result[-1].append(selection.data(Qt.DisplayRole))
            prev_selection = selection

        result_text = '\r\n'.join(['\t'.join(item) for item in result])
        QApplication.clipboard().setText(result_text)

    def paste_data(self):
        container = self.get_current_data_container()
        selections = container.data_view.selectedIndexes()
        if len(selections) <= 0:
            return
        selections.sort()

        data = QApplication.clipboard().text()
        data = [row.split('\t') for row in data.split('\r\n')]

        y1 = selections[0].column()
        y2 = y1 + len(data[0])
        x1 = selections[0].row()
        x2 = x1 + len(data)
        arr = pd.array(data)
        container.raw_data.iloc[x1:x2, y1:y2] = arr
        container.data_view.model().layoutChanged.emit()
        # 제대로 안됨...수정할 것


def show(data: pd.DataFrame = None, name: str = 'Data'):
    window = MainWindow()

    if data is not None:
        data_container = DataContainer(data)
        data_container.name = name
        window.add_sheet(data_container)

    window.show()

    app.exec()
