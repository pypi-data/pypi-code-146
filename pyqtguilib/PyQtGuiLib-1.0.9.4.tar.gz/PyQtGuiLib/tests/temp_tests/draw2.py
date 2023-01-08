# -*- coding:utf-8 -*-
# @time:2023/1/55:01
# @author:LX
# @file:draw2.py
# @software:PyCharm
from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    sys,
    QApplication,
    QWidget,
    Signal,
    Qt,
    QFont,
    QColor,
    QPen,
    QPainter,
    QPaintEvent,
    QFontMetricsF,
    QSize,
    QResizeEvent,
    QPropertyAnimation,
    QPoint,
    QThread,
    QPushButton,
    QPainterPath,
    QLinearGradient,
    QRectF,
    QPolygonF,
    QPointF,
    QGridLayout,
    QPalette,
)
from PyQt5.QtWidgets import QStyleOptionFocusRect,QStyle,QPushButton,QStyleFactory
'''
    绘图练习2
'''


class Test1(QWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(800,600)


    def paintEvent(self, e: QPaintEvent) -> None:
        painter = QPainter(self)

        option = QStyleOptionFocusRect()
        option.initFrom(self)
        # option.backgroundColor=self.palette().color(QPalette.Background)
        option.backgroundColor=QColor(0,255,0)

        self.style().drawPrimitive(QStyle.PE_FrameFocusRect,option,painter,self)

        painter.end()

class Test(QWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(800,600)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Test()
    win.show()

    if PYQT_VERSIONS == "PyQt6":
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())
