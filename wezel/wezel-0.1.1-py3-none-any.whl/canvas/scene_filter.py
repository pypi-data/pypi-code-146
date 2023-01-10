from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtWidgets import QGraphicsObject, QGraphicsItem, QAction, QMenu, QPushButton
from PyQt5.QtGui import QPixmap, QCursor, QIcon, QColor, QPen, QTransform

from wezel import canvas, icons

class PanFilter(canvas.FilterItem):
    """Panning the scene
    """
    def __init__(self): 
        super().__init__()
        pixMap = QPixmap(icons.hand_point_090)
        self.cursor = QCursor(pixMap, hotX=4, hotY=0)
        self.icon = QIcon(pixMap)
        self.toolTip = 'Pan'
        self.text = 'Pan'
        self.setActionPick()

    def mouseMoveEvent(self, event):
        self.x = int(event.pos().x())
        self.y = int(event.pos().y())
        button = event.buttons()
        if button == Qt.LeftButton:
            distance = event.screenPos() - event.lastScreenPos()
            self.pan(distance)

    def pan(self, distance):
        cnvs = self.scene().parent()
        hBar = cnvs.horizontalScrollBar()
        vBar = cnvs.verticalScrollBar()
        hBar.setValue(hBar.value() - distance.x())
        vBar.setValue(vBar.value() - distance.y())




class ZoomFilter(canvas.FilterItem):
    """Provides zoom/pan/windowing functionality for a MaskOverlay.
    """
    def __init__(self): 
        super().__init__()
        pixMap = QPixmap(icons.magnifier)
        self.cursor = QCursor(pixMap, hotX=10, hotY=4)
        self.icon = QIcon(pixMap)
        self.toolTip = 'Zoom'
        self.text = 'Zoom'
        self.x0 = None
        self.y0 = None
        self.setActionPick()

    def paint(self, painter, option, widget):
        if self.x0 is not None:
            width = self.x - self.x0
            height = self.y - self.y0
            pen = QPen()
            pen.setColor(QColor(Qt.white))
            pen.setWidth(0)
            painter.setPen(pen)
            painter.drawRect(self.x0, self.y0, width, height)

    def mousePressEvent(self, event):
        self.x = int(event.pos().x())
        self.y = int(event.pos().y())
        button = event.button()
        if button == Qt.LeftButton:
            self.x0 = self.x
            self.y0 = self.y 

    def mouseMoveEvent(self, event):
        self.x = int(event.pos().x())
        self.y = int(event.pos().y())
        button = event.buttons()
        if button == Qt.LeftButton:
            self.update()  

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.x0 is not None:
                width = self.x - self.x0
                height = self.y - self.y0
                cnvs = self.scene().parent()
                cnvs.fitInView(self.x0, self.y0, width, height, Qt.KeepAspectRatio)
        self.x0 = None
        self.y0 = None  
