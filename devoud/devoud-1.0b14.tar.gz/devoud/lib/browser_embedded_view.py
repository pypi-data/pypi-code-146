from PySide6.QtWidgets import QWidget
from .embedded_widget import EmbeddedWidget


class EmbeddedView(QWidget):
    title = "'Embedded Page'"
    url = None

    def __init__(self, parent):
        super().__init__(parent)
        self.setObjectName('embedded_view')
        self.embedded = True

    def load(self, url):
        self.parent().load(url)

    def reload(self):
        self.parent().load(self.url)

    def forward(self):
        pass

    def back(self):
        pass
