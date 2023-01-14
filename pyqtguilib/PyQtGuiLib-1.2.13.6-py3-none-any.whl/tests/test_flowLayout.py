# -*- coding:utf-8 -*-
# @time:2023/1/1313:44
# @author:LX
# @file:test_flowLayout.py
# @software:PyCharm
from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    QApplication,
    sys,
    QWidget,
    QScrollArea,
    QPushButton,
    qt
)

from PyQtGuiLib.core import FlowLayout
from PyQtGuiLib.styles import ButtonStyle

'''
    测试用例的标准模板,该代码用于复制
'''
from PyQt5.QtWidgets import QMenuBar,QMenu

class TestFlowLayout(QScrollArea):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(600,600)

        self.core = QWidget()
        self.setWidgetResizable(True)

        self.setWidget(self.core)

        self.flow = FlowLayout(self)

        # self.setVerticalScrollBarPolicy(qt.ScrollBarAlwaysOn)
        # self.setHorizontalScrollBarPolicy(qt.ScrollBarAlwaysOn)

        for i in range(20):
            btn = QPushButton("test_{}".format(i))
            btn.setFixedSize(120,60)
            self.flow.addWidget(btn)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = TestFlowLayout()
    win.show()

    if PYQT_VERSIONS in ["PyQt6","PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())