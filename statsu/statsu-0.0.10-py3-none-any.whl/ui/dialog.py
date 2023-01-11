from typing import Optional
from PySide6.QtWidgets import QDialog, QWidget
from statsu.ui.design.open_csv_dialog import Ui_OpenCSVDialog

class OpenCSVDialog(QDialog, Ui_OpenCSVDialog):
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.selected_splitter = ','

        self.radio_comma.toggled.connect(self.select_comma)
        self.radio_semicolon.toggled.connect(self.select_semi_colon)
        self.radio_space.toggled.connect(self.select_space)
        self.radio_tab.toggled.connect(self.select_tab)
        self.radio_other.toggled.connect(self.select_other)
        self.textbox_custom_splitter.textChanged.connect(self.input_splitter)

    def select_comma(self):
        if self.radio_comma.isChecked():
            self.selected_splitter = ','
            self.textbox_custom_splitter.setEnabled(False)

    def select_semi_colon(self):
        if self.radio_semicolon.isChecked():
            self.selected_splitter = ';'
            self.textbox_custom_splitter.setEnabled(False)

    def select_space(self):
        if self.radio_space.isChecked():
            self.selected_splitter = ' '
            self.textbox_custom_splitter.setEnabled(False)

    def select_tab(self):
        if self.radio_tab.isChecked():
            self.selected_splitter = '\t'
            self.textbox_custom_splitter.setEnabled(False)

    def select_other(self):
        if self.radio_other.isChecked():
            self.textbox_custom_splitter.setEnabled(True)
        
    def input_splitter(self):
        self.selected_splitter = self.textbox_custom_splitter.text()

    def get_header_type(self):
        if self.combo_header_type.currentIndex() == 0:
            return 'infer'
        elif self.combo_header_type.currentIndex() == 1:
            return 0
        else:
            return None
    
