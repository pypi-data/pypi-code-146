from .devoud_data import *


class FindWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setObjectName('find_widget')
        self.setFixedHeight(50)
        self.setLayout(QHBoxLayout())

        self.page_view = self.parent().view

        self.find_line_edit = QLineEdit(self)
        self.find_line_edit.setObjectName('find_widget_edit')
        self.find_line_edit.setClearButtonEnabled(True)
        self.find_line_edit.setPlaceholderText("Найти на странице...")
        self.find_line_edit.textChanged.connect(self.find_text)
        self.layout().addWidget(self.find_line_edit)

        self.case_sensitive_checkbox = QCheckBox('Учитывать регистр')
        self.case_sensitive_checkbox.stateChanged.connect(self.find_text)
        self.layout().addWidget(self.case_sensitive_checkbox)

        self.previous_button = QPushButton(self)
        self.previous_button.setObjectName('find_widget_previous_button')
        self.previous_button.clicked.connect(lambda: self.find_text(True))
        self.layout().addWidget(self.previous_button)

        self.next_button = QPushButton(self)
        self.next_button.setObjectName('find_widget_next_button')
        self.next_button.clicked.connect(self.find_text)
        self.layout().addWidget(self.next_button)

        self.hide_button = QPushButton(self)
        self.hide_button.setObjectName('find_widget_hide_button')
        self.hide_button.setText('Закрыть')
        self.hide_button.setShortcut(QKeySequence(Qt.Key_Escape))
        self.hide_button.clicked.connect(self.hide_find)
        self.layout().addWidget(self.hide_button)

    def find_focus(self):
        self.find_line_edit.setFocus()

    def find_text(self, backward=False):
        text = self.find_line_edit.text().strip()
        flags = QWebEnginePage.FindFlags()
        if self.case_sensitive_checkbox.isChecked():
            flags |= QWebEnginePage.FindCaseSensitively
        if backward:
            flags |= QWebEnginePage.FindBackward
        self.page_view.findText(text, flags)

    def hide_find(self):
        self.page_view.findText('')
        self.hide()
