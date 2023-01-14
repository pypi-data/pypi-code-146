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
        # self.resize(800,600)
        self.resize(200,60)
        self.layout = QGridLayout(self)
        #背景填充灰色
        self.setAutoFillBackground(True)
        p  = QPalette()
        p.setColor(QPalette.Background,Qt.gray)
        self.setPalette(p)
        #设置进度条颜色
        self.bg_color = QColor(255, 0, 0)
        #设置界面刷新时间
        self.startTimer(80)
        self.m_waterOffset = 0.05
        self.m_offset = 50
        self.m_borderwidth = 10
        #进度条进度范围0-100
        self.per_num = 50


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
        # 获取窗口的宽度和高度
        width, height = self.width(), self.height()
        percentage = 1 - self.per_num / 100
        # 水波走向：正弦函数 y = A(wx+l) + k
        # w 表示 周期，值越大密度越大
        w = 2 * math.pi / (width)
        # A 表示振幅 ，理解为水波的上下振幅
        A = height * self.m_waterOffset
        # k 表示 y 的偏移量，可理解为进度
        k = height * percentage

        water1 = QPainterPath()
        water2 = QPainterPath()
        # 起始点
        water1.moveTo(5, height)
        water2.moveTo(5, height)
        self.m_offset += 0.6

        if (self.m_offset > (width / 2)):
            self.m_offset = 0
        i = 5
        while (i < width - 5):
            waterY1 = A * math.sin(w * i + self.m_offset) + k
            waterY2 = A * math.sin(w * i + self.m_offset + width / 2 * w) + k
            print(i,waterY1)
            water1.lineTo(i, waterY1)
            # water2.lineTo(i, waterY2)
            i += 1

        # water1.lineTo(width - 5, height)
        # water2.lineTo(width - 5, height)
        totalpath = QPainterPath()
        totalpath.addRect(QRectF(5, 5, self.width() - 10, self.height() - 10))
        painter.setBrush(Qt.gray)
        painter.drawRect(self.rect())
        painter.save()

        painter.setPen(Qt.NoPen)

        # 设置水波的透明度
        watercolor1 = QColor(self.bg_color)
        watercolor1.setAlpha(100)
        watercolor2 = QColor(self.bg_color)
        watercolor2.setAlpha(150)

        path = totalpath.intersected(water1)
        painter.setBrush(watercolor1)
        painter.drawPath(path)

        # path = totalpath.intersected(water2)
        # painter.setBrush(watercolor2)
        # painter.drawPath(path)
        # painter.restore()

        '''绘制字体'''
        m_font = QFont()
        m_font.setFamily('Microsoft YaHei')
        m_font.setPixelSize(int(self.width() / 10))
        painter.setPen(Qt.white)
        painter.setFont(m_font)
        painter.drawText(self.rect(), Qt.AlignCenter, "{}%".format(self.per_num))
        painter.end()

    # def timerEvent(self, event):
    #
    #     self.per_num +=1
    #     if self.per_num ==101:
    #         self.per_num = 0
    #     self.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Test()
    win.show()

    if PYQT_VERSIONS == "PyQt6":
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())
