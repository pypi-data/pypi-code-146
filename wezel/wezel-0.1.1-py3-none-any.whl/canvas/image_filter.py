import numpy as np

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QAction, QMenu, QActionGroup
from PyQt5.QtGui import QPixmap, QCursor, QIcon

from wezel import canvas, icons


class ImageWindow(canvas.FilterItem):
    windowChanged = pyqtSignal(object, float, float, bool)

    """Change contrast
    """
    def __init__(self): 
        super().__init__()
        pixMap = QPixmap(icons.color)
        self.cursor = QCursor(pixMap, hotX=4, hotY=0)
        self.icon = QIcon(pixMap)
        self.toolTip = 'Select color scale window..'
        self.text = 'Window' 
        self._min = None
        self._max = None
        self.setActionPick()

    def window(self, dx, dy):
        """Change intensity and contrast"""

        cnvs = self.scene().parent()
        item = cnvs.imageItem
        if self._min is None:
            self._min = np.amin(item._array)
            self._max = np.amax(item._array)
       
        # Move 1024 to change the center over the full range
        # Speed is faster further away from the center of the range
        center = item._center 
        v0 = (self._max-self._min)/1024
        a0 = 1.0/256
        vy = v0 + a0*abs((center - (self._min+(self._max-self._min)/2.0)))
        center = center + vy * dy

        # Changing the width is faster at larger widths
        width = item._width
        v0 = (self._max-self._min)/512
        a0 = 1.0/64
        vx = v0 + a0*width
        width = width - vx * dx
        width = width if width>1 else 1

        cnvs.setWindow(center, width)
        self.windowChanged.emit(item._array, center, width, True)

    def mouseMoveEvent(self, event):
        self.x = int(event.pos().x())
        self.y = int(event.pos().y())
        button = event.buttons()
        if button == Qt.LeftButton:
            d = event.screenPos() - event.lastScreenPos()
            self.window(d.x(), d.y())

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.x0 = None
            self.y0 = None 

    def contextMenu(self):
        return self.actionPick.menu()

    def menuOptions(self):
        menu = QMenu()
        menu.setIcon(QIcon(icons.spectrum))
        menu.setTitle('Set colormap..')
        menu.triggered.connect(lambda action: self.setColorMap(action.cmap))
        actionGroup = QActionGroup(menu)
        default = 'Greyscale'
        self.addActionSetColormap(menu, actionGroup, default, default)
        self.addSeparator(menu)
        COLORMAPS = canvas.COLORMAPS
        for group in range(5):
            for cmap in COLORMAPS[group][1]:
                self.addActionSetColormap(menu, actionGroup, cmap, default)
            self.addSeparator(menu)
        for cmap in COLORMAPS[5][1]:
            self.addActionSetColormap(menu, actionGroup, cmap, default)
        return menu

    def setColorMap(self, cmap):
        self.pick()
        cnvs = self.scene().parent()
        cnvs.setColormap(cmap)

    def getColorMap(self):
        menu = self.actionPick.menu()
        for action in menu.actions():
            if not action.isSeparator():
                if action.isChecked():
                    return action.cmap      

    def setChecked(self, cmap):
        menu = self.actionPick.menu()
        for action in menu.actions():
            if not action.isSeparator():
                checked = action.cmap == cmap
                action.setChecked(checked)
    
    def addActionSetColormap(self, menu, actionGroup, cmap, current):
        action = QAction(cmap)
        action.setCheckable(True)
        action.setChecked(cmap == current)
        action.cmap = cmap
        actionGroup.addAction(action)
        menu.addAction(action)
