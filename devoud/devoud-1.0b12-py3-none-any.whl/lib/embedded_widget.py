from .devoud_data import *


class EmbeddedWidget(QWidget):
    def __init__(self, title: str = ''):
        super().__init__()
        self.title = title
        self.setObjectName('embedded_widget')
        self.layout = QGridLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(12, 0, 12, 0)

        self.title_widget = QWidget(self)
        self.title_widget.setObjectName('embedded_widget_title')
        self.title_widget.setFixedHeight(32)
        self.title_layout = QHBoxLayout(self.title_widget)
        self.title_layout.setContentsMargins(6, 0, 10, 0)
        self.title_label = QLabel(self, text=self.title)
        self.title_label.setObjectName('embedded_widget_title_text')
        self.title_layout.addWidget(self.title_label)
        self.layout.addWidget(self.title_widget)

        self.content = QWidget(self)
        self.content.setObjectName('embedded_widget_content')
        self.content_layout = QGridLayout(self.content)
        self.layout.addWidget(self.content)
