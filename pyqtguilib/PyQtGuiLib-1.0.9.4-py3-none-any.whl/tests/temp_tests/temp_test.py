# -*- coding:utf-8 -*-
# @time:2022/12/3012:41
# @author:LX
# @file:temp_test.py
# @software:PyCharm

from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    QApplication,
    sys,
    QWidget,
    QListWidget,
    QListWidgetItem,
    QComboBox,
    QPaintEvent,
    QPushButton,
    QMouseEvent,
    QAction,
)

class Test(QComboBox):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)


        self.btn = QPushButton("我是下拉框",self)
        self.btn.move(50,50)


        for i in range(5):
            self.addItem("选项{}".format(i))
            # self.addItem(item)
            # item = QListWidgetItem()
            # item.setText("选项{}".format(i))
            # self.addItem(item)


    def mousePressEvent(self, e:QMouseEvent) -> None:
        super().mousePressEvent(e)

    def paintEvent(self, e: QPaintEvent) -> None:
        pass
        # super().paintEvent(e)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Test()
    win.show()

    if PYQT_VERSIONS == "PyQt6":
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())