from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    sys,
    QApplication,
    QWidget,
    QThread,
    Signal,
    QPoint,
    QFont,
    QColor,
    QPen,
    QPainter,
    QPaintEvent,
    QFontMetricsF,
    QSize,
    QResizeEvent,
    QMainWindow
)



class TestPullOverWidget(QMainWindow):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(500,500)


    def paintEvent(self, event:QPaintEvent) -> None:
        painter = QPainter()
        painter.begin(self)

        for i in range(self.width()):
            for j in range(self.height()):
                painter.drawPoint(QPoint(i,j))

        # painter.setBrush(QColor(105, 255, 152))
        # painter.drawRect(10,30,100,100)
        #
        # painter.drawArc(150,30,100,100,0,360*16)
        # painter.setOpacity(0.5)
        # painter.setPen(QColor(105, 255, 152))
        # painter.drawEllipse(150,30,100,100)
        painter.end()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = TestPullOverWidget()
    win.show()

    if PYQT_VERSIONS == "PyQt6":
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())
