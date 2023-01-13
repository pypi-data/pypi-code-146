# -*- coding:utf-8 -*-
# @time:2023/1/36:13
# @author:LX
# @file:test_QAbstractScrollArea.py
# @software:PyCharm

from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    sys,
    QApplication,
    QAbstractScrollArea,
    QWidget,
    Qt,
    QLineEdit,
    QPainter,
    QPaintEvent,
    QResizeEvent,
)

class Test(QLineEdit):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        # self.resize(300,300)

        # self.t = QWidget()
        # self.t.setStyleSheet("background-color:red;")

        # self.addScrollBarWidget(self.t, Qt.AlignmentFlag)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Test()
    win.show()

    if PYQT_VERSIONS == "PyQt6":
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())