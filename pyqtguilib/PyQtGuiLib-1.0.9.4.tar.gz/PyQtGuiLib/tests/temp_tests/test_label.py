# -*- coding:utf-8 -*-
# @time:2022/12/3013:58
# @author:LX
# @file:test_label.py
# @software:PyCharm
from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    QApplication,
    sys,
    QWidget,
    QLabel,
    QPaintEvent,
    QMouseEvent,
    QKeyEvent,
    Qt
)


class Test(QLabel):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(200,200)
        self.__text = ""
        self.setText("我是 标签")
        self.setAlignment(Qt.AlignCenter)


    def keyPressEvent(self, ev: QKeyEvent) -> None:
        self.__text +=ev.text()
        self.setText(self.__text)
        super().keyPressEvent(ev)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Test()
    win.show()

    if PYQT_VERSIONS == "PyQt6":
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())