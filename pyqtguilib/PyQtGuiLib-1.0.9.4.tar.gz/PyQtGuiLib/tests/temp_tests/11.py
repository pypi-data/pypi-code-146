# -*- coding:utf-8 -*-
# @time:2022/12/239:56
# @author:LX
# @file:draw.py
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

import math
'''
    绘图练习
'''
class Test(QWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.w,self.h = 800,600
        self.resize(self.w,self.h)
        self.m_waterOffset = 0.05
        # self.resize(200,60)


    def one(self):
        path = QPainterPath()
        path.addRect(20, 20, 60, 60)

        path.moveTo(0, 0)
        path.cubicTo(99, 0, 50, 50, 99, 99)
        path.cubicTo(0, 99, 50, 50, 0, 0)

        painter = QPainter()
        painter.begin(self)
        painter.fillRect(0, 0, 100, 100, Qt.white)
        painter.setPen(QPen(QColor(79, 106, 25), 1, Qt.SolidLine, Qt.FlatCap, Qt.MiterJoin))
        painter.setBrush(QColor(122, 163, 39));

        painter.drawPath(path)
        painter.end()

    def two(self):
        gradient = QLinearGradient(10, 10, 100, 50) # 线性渐变
        gradient.setColorAt(0.2,Qt.red)
        gradient.setColorAt(0.5,QColor(152,45,88))
        myopen = QPen()
        myopen.setColor(QColor(0, 255, 50))
        rect_ = QRectF(10, 10, 100, 50)


        path = QPainterPath()
        path.addEllipse(rect_)

        painter = QPainter()
        painter.begin(self)
        painter.setBrush(gradient)
        painter.setPen(myopen)
        painter.drawPath(path)

        painter.end()

    def three(self):
        gradient = QLinearGradient(10, 10, 100, 50)  # 线性渐变
        myopen = QPen()
        myopen.setColor(QColor(0, 255, 50))
        # 注意,在绘制的时候,程序会根据值的顺序来绘制
        polys = QPolygonF([QPointF(10, 10), QPointF(100, 10), QPointF(100, 100), QPointF(10, 100)])

        path = QPainterPath()
        path.addPolygon(polys)

        painter = QPainter()
        painter.begin(self)
        painter.setBrush(gradient)
        painter.setPen(myopen)
        painter.drawPath(path)

        painter.end()

    def four(self):
        point = QRectF(10, 10, 100, 50)
        font = QFont()
        font.setPointSize(15)

        path = QPainterPath()
        path.moveTo(4, 4)
        path.arcTo(point, 360, 180)

        painter = QPainter(self)
        painter.setPen(QPen(QColor(100, 200, 36), 1))
        painter.setBrush(QLinearGradient(50, 50, 50, 100))

        painter.drawPath(path)
        painter.end()

    def five(self):
        gradient = QLinearGradient(50, 50, 100, 200)
        myopen = QPen()
        myopen.setColor(QColor(152, 24, 88))

        path = QPainterPath()
        path.moveTo(50, 50)
        path.cubicTo(QPointF(150, 100), QPointF(50, 50), QPointF(300, 100))

        painter = QPainter(self)

        painter.setPen(myopen)
        painter.setBrush(gradient)

        painter.drawPath(path)
        painter.end()

    def paintEvent(self, e: QPaintEvent) -> None:
        # 锯齿状绘画板；
        painter = QPainter()
        painter.setRenderHint(QPainter.Antialiasing)
        painter.begin(self)

        A = self.h * self.m_waterOffset
        w = 2 * math.pi / (self.w)

        water1 = QPainterPath()
        water1.moveTo(5,self.h)

        i = 5
        while (i<self.w-5):
            w1 = A * math.sin(w*i+self.m_waterOffset)+self.h-120
            print(i,w1)
            water1.lineTo(i,w1)
            i+=1

        water1.lineTo(self.w-5,self.h)
        painter.setBrush(Qt.red)
        painter.drawPath(water1)
        painter.end()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Test()
    win.show()

    if PYQT_VERSIONS == "PyQt6":
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())
