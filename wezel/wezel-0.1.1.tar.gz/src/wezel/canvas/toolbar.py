import numpy as np

from PyQt5.QtWidgets import (
    QWidget, QGridLayout, 
    QToolBar, QAction, QMenu,
    QActionGroup, QFrame)
from PyQt5.QtGui import QIcon

from wezel import canvas, icons, widgets


def defaultFilters():
    return [
        canvas.PanFilter(),
        canvas.ZoomFilter(),
        canvas.ImageWindow(),
        canvas.MaskThreshold(),
        canvas.MaskBrush(mode='paint'),
        canvas.MaskPaintByNumbers(mode='paint'),
        canvas.MaskRegionGrowing(mode='paint'),
        canvas.MaskBrush(mode='erase'),
        canvas.MaskPaintByNumbers(mode='erase'),
        canvas.MaskRegionGrowing(mode='erase'),
        canvas.MaskPenSet(mode='draw'),
        canvas.MaskPenSet(mode='cut'),
        canvas.MaskPenSet(mode='catch'),
        canvas.MaskDilate(),
        canvas.MaskShrink(),
        canvas.MaskKidneyEdgeDetection(),
    ]


class ToolBar(QWidget):

    def __init__(self, parent=None, filters=None):
        super().__init__(parent)

        self.canvas = None
        if filters is not None:
            self.filters = filters
        else:
            self.filters = defaultFilters()

        # Define UI elements
        self.regionList = widgets.RegionList(layout=None)
        self.window = widgets.ImageWindow(layout=False)
        self.actionFitItem = QAction(QIcon(icons.magnifier_zoom_fit), 'Fit in view', self)
        self.menuZoomToScale = self.menuZoomTo()
        self.actionZoomTo = QAction(QIcon(icons.magnifier_zoom_actual), 'Zoom to..', self)
        self.actionZoomTo.setMenu(self.menuZoomToScale)
        self.actionFitItemAndZoom = QAction(QIcon(icons.magnifier_zoom_fit), 'Fit in view', self)
        self.actionFitItemAndZoom.setMenu(self.menuZoomToScale)
        self.actionZoomIn = QAction(QIcon(icons.magnifier_zoom_in), 'Zoom in..', self)
        self.actionZoomOut = QAction(QIcon(icons.magnifier_zoom_out), 'Zoom out..', self)
        self.actionOpacity = ActionOpacity()
        self.actionSetDefaultColor = QAction(QIcon(icons.contrast_low), 'Greyscale', self)
        self.actionSetDefaultColor.setToolTip('Set to default greyscale')
        self.actionUndo = QAction(QIcon(icons.arrow_curve_180_left), 'Undo..', self)
        self.actionUndo.setEnabled(False)
        self.actionRedo = QAction(QIcon(icons.arrow_curve), 'Redo..', self)
        self.actionRedo.setEnabled(False)
        self.actionErase = QAction(QIcon(icons.cross_script), 'Erase..', self)
        self.actionErase.setEnabled(False)
        
        # Connect signals to slots
        self.window.valueChanged.connect(lambda v: self.canvas.setWindow(v[0], v[1]))
        self.actionFitItem.triggered.connect(lambda: self.canvas.fitItem())
        self.actionFitItemAndZoom.triggered.connect(lambda: self.canvas.fitItem())
        self.actionZoomIn.triggered.connect(lambda: self.canvas.scale(2.0, 2.0))
        self.actionZoomOut.triggered.connect(lambda: self.canvas.scale(0.5, 0.5))
        self.actionOpacity.triggered.connect(self.toggleOpacity)
        self.actionOpacity.menu().triggered.connect(lambda action: self.canvas.maskItem.setOpacity(action.opacity))
        self.actionSetDefaultColor.triggered.connect(self.setDefaultColor)
        self.actionUndo.triggered.connect(self.undo)
        self.actionRedo.triggered.connect(self.redo)
        self.actionErase.triggered.connect(self.erase)
        self.filters[2].windowChanged.connect(
            lambda array, center, width, set: self.window.setData(array, center, width, set=set)
        )

        # Add filters to action group so only one can be selected
        self.group = QActionGroup(self)
        self.group.triggered.connect(
            lambda action: self.canvas.setFilter(action.filter))
        for filter in self.filters:
            self.group.addAction(filter.actionPick)

        # Set default filter
        self.filters[0].actionPick.setChecked(True)
        self.setEnabled(False)

        self._view = ToolBarView(self)

    def setWidget(self, canvas):
        if canvas == self.canvas:
            return
        self.setEnabled(True)
        self.setEditMaskEnabled(False)
        self.canvas = canvas
        self.canvas.toolBar = self
        self.canvas.setFilter(self.group.checkedAction().filter)
        self.regionList.setCanvas(canvas)
        self.window.setData(canvas.array(), canvas.center(), canvas.width(), set=True)
        mask = canvas.mask()
        if mask is not None:
            canvas.setMask(
                mask, 
                color=canvas._model.color(), 
                opacity=self.actionOpacity.opacity())
                #opacity=self.opacity())

    def toggleOpacity(self):
        if self.canvas.maskItem is None:
            return
        if self.canvas.maskItem.opacity() <= 0.25:
            opacity = 0.75
        else: 
            opacity = 0.25
        self.canvas.maskItem.setOpacity(opacity)
        self.actionOpacity.setOpacity(opacity)
        
    def maskChanged(self):
        self.setEditMaskEnabled()
    
    def newRegion(self):
        self.setEditMaskEnabled()
        self.regionList.setView()

    def setArray(self, array, center, width, colormap):
        self.setEditMaskEnabled()
        if self.window.mode.isLocked:
            v = self.window.getValue()
            cmap = self.filters[2].getColorMap()
            self.canvas.setWindow(v[0], v[1])
            self.canvas.setColormap(cmap)
        else:
            self.window.setData(array, center, width)
            self.filters[2].setChecked(colormap)

    def setEditMaskEnabled(self, enable=None):
        if enable is None:
            item = self.canvas.maskItem
            undoEnable = item._current!=0 and item._current is not None
            redoEnable = item._current!=len(item._bin)-1 and item._current is not None
            if item.bin() is None:
                eraseEnable = False
            else:
                eraseEnable = item.bin().any()
        else:
            undoEnable = enable
            redoEnable = enable
            eraseEnable = enable
        self.actionUndo.setEnabled(undoEnable)
        self.actionRedo.setEnabled(redoEnable)
        self.actionErase.setEnabled(eraseEnable)

    def undo(self):
        item = self.canvas.maskItem
        item.undo()
        self.canvas.saveMask()
        self.setEditMaskEnabled()

    def redo(self):
        item = self.canvas.maskItem
        item.redo()
        self.canvas.saveMask()
        self.setEditMaskEnabled()

    def erase(self):
        item = self.canvas.maskItem
        item.erase()
        self.canvas.saveMask()
        self.setEditMaskEnabled()

    def setDefaultColor(self):
        self.canvas.setWindow()
        self.canvas.setColormap()
        self.window.setData(self.canvas.array(), self.canvas.center(), self.canvas.width(), set=True)
        self.filters[2].setChecked('Greyscale')

    def menuZoomTo(self, parent=None):
        menu = QMenu(parent)
        menu.setIcon(QIcon(icons.magnifier_zoom_actual))
        menu.setTitle('Zoom to..')
        zoomTo010 = QAction('10%', menu)
        zoomTo025 = QAction('25%', menu)
        zoomTo050 = QAction('50%', menu)
        zoomTo100 = QAction('100%', menu)
        zoomTo200 = QAction('200%', menu)
        zoomTo400 = QAction('400%', menu)
        zoomTo1000 = QAction('1000%', menu)
        zoomTo010.triggered.connect(lambda: self.canvas.zoomTo(0.10)) 
        zoomTo025.triggered.connect(lambda: self.canvas.zoomTo(0.25))
        zoomTo050.triggered.connect(lambda: self.canvas.zoomTo(0.5))
        zoomTo100.triggered.connect(lambda: self.canvas.zoomTo(1))
        zoomTo200.triggered.connect(lambda: self.canvas.zoomTo(2))
        zoomTo400.triggered.connect(lambda: self.canvas.zoomTo(4))
        zoomTo1000.triggered.connect(lambda: self.canvas.zoomTo(10))
        menu.addAction(zoomTo010)
        menu.addAction(zoomTo025)
        menu.addAction(zoomTo050)
        menu.addAction(zoomTo100)
        menu.addAction(zoomTo200)
        menu.addAction(zoomTo400)
        menu.addAction(zoomTo1000)
        return menu


class ToolBarView():
    def __init__(self, toolBar):

        grid = QGridLayout()
        grid.setHorizontalSpacing(0)
        grid.setVerticalSpacing(4)

        row = 0
        nrows = 2
        frame = self._getWidgetDisplay(toolBar)
        grid.addWidget(frame,row,0,nrows,3)

        row += nrows
        nrows = 3
        frame = self._getWidgetColor(toolBar)
        grid.addWidget(frame,row,0,nrows,3)

        row += nrows
        nrows = 2
        frame = self._getWidgetRegion(toolBar)
        grid.addWidget(frame,row,0,nrows,3)

        row += nrows
        nrows = 6
        frame = self._getWidgetDraw(toolBar)
        grid.addWidget(frame,row,0,nrows,3)

        toolBar.setLayout(grid)


    def _getWidgetDisplay(self, toolBar):
        frame = QFrame()
        frame.setFrameStyle(QFrame.Panel | QFrame.Raised)
        framegrid = QGridLayout()
        framegrid.setHorizontalSpacing(0)
        framegrid.setVerticalSpacing(0)
        w = QToolBar()
        w.addAction(toolBar.actionZoomIn)
        framegrid.addWidget(w,0,0)
        w = QToolBar()
        w.addAction(toolBar.actionZoomOut)
        framegrid.addWidget(w,0,1)
        w = QToolBar()
        w.addAction(toolBar.actionFitItemAndZoom)
        framegrid.addWidget(w,0,2)
        w = QToolBar()
        w.addAction(toolBar.filters[1].actionPick)
        framegrid.addWidget(w,1,0)
        w = QToolBar()
        w.addAction(toolBar.filters[0].actionPick)
        framegrid.addWidget(w,1,1)
        w = QToolBar()
        w.addAction(toolBar.actionOpacity)
        framegrid.addWidget(w,1,2)    
        frame.setLayout(framegrid)
        return frame

    def _getWidgetColor(self, toolBar):
        frame = QFrame()
        frame.setFrameStyle(QFrame.Panel | QFrame.Raised)
        framegrid = QGridLayout()
        framegrid.setHorizontalSpacing(0)
        framegrid.setVerticalSpacing(0)
        w = QToolBar()
        w.addWidget(toolBar.window.mode)
        framegrid.addWidget(w,0,0)
        w = QToolBar()
        w.addAction(toolBar.actionSetDefaultColor)
        framegrid.addWidget(w,0,1)
        w = QToolBar()
        w.addAction(toolBar.filters[2].actionPick)
        framegrid.addWidget(w,0,2)
        framegrid.addWidget(toolBar.window.brightness.spinBox, 1, 0, 1, 3)
        framegrid.addWidget(toolBar.window.contrast.spinBox, 2, 0, 1, 3)
        frame.setLayout(framegrid)
        return frame
    
    def _getWidgetRegion(self, toolBar):
        frame = QFrame()
        frame.setFrameStyle(QFrame.Panel | QFrame.Raised)
        framegrid = QGridLayout()
        framegrid.setHorizontalSpacing(0)
        framegrid.setVerticalSpacing(0)
        framegrid.addWidget(toolBar.regionList.comboBox,0,0,1,3)
        w = QToolBar()
        w.addAction(toolBar.regionList.btnLoad)
        framegrid.addWidget(w,1,0)
        w = QToolBar()
        w.addAction(toolBar.regionList.btnNew)
        framegrid.addWidget(w,1,1)
        w = QToolBar()
        w.addAction(toolBar.regionList.btnDelete)
        framegrid.addWidget(w,1,2)
        frame.setLayout(framegrid)
        return frame
    
    def _getWidgetDraw(self, toolBar):
        frame = QFrame()
        frame.setFrameStyle(QFrame.Panel | QFrame.Raised)
        framegrid = QGridLayout()
        framegrid.setHorizontalSpacing(0)
        framegrid.setVerticalSpacing(0)
        w = QToolBar()
        w.addAction(toolBar.actionUndo)
        framegrid.addWidget(w,0,0)
        w = QToolBar()
        w.addAction(toolBar.actionRedo)
        framegrid.addWidget(w,0,1)
        w = QToolBar()
        w.addAction(toolBar.actionErase)
        framegrid.addWidget(w,0,2) 
        w = QToolBar()
        w.addAction(toolBar.filters[10].actionPick)
        framegrid.addWidget(w,1,0)
        w = QToolBar()
        w.addAction(toolBar.filters[11].actionPick)
        framegrid.addWidget(w,1,1)
        w = QToolBar()
        w.addAction(toolBar.filters[12].actionPick)
        framegrid.addWidget(w,1,2)
        w = QToolBar()
        w.addAction(toolBar.filters[4].actionPick)
        framegrid.addWidget(w,2,0)
        w = QToolBar()
        w.addAction(toolBar.filters[5].actionPick)
        framegrid.addWidget(w,2,1)
        w = QToolBar()
        w.addAction(toolBar.filters[6].actionPick)
        framegrid.addWidget(w,2,2)
        w = QToolBar()
        w.addAction(toolBar.filters[7].actionPick)
        framegrid.addWidget(w,3,0)
        w = QToolBar()
        w.addAction(toolBar.filters[8].actionPick)
        framegrid.addWidget(w,3,1)
        w = QToolBar()
        w.addAction(toolBar.filters[9].actionPick)
        framegrid.addWidget(w,3,2)               
        w = QToolBar()
        w.addAction(toolBar.filters[3].actionPick)
        framegrid.addWidget(w,4,0)
        w = QToolBar()
        w.addAction(toolBar.filters[13].actionPick)
        framegrid.addWidget(w,4,1)
        w = QToolBar()
        w.addAction(toolBar.filters[14].actionPick)
        framegrid.addWidget(w,4,2)
        w = QToolBar()
        w.addAction(toolBar.filters[15].actionPick)
        framegrid.addWidget(w,5,0)
        frame.setLayout(framegrid)
        return frame


class ActionOpacity(QAction):
    def __init__(self):
        super().__init__()
        #self.toolBar = toolBar
        menu = QMenu()
        menu.setIcon(QIcon(icons.layer_transparent))
        # self.menu.triggered.connect(lambda action: toolBar.canvas.maskItem.setOpacity(action.opacity))
        actionGroup = QActionGroup(menu)
        settings = {
            '100%': 0.0,
            '90%': 0.10,
            '75%': 0.25,
            '50%': 0.50,
            '25%': 0.75,
            '10%': 0.90,
            '0%': 1.0,
        }
        for text, value in settings.items():
            action = QAction(text)
            action.opacity = value
            action.setCheckable(True) 
            action.setChecked(action.opacity == 0.75) # default opacity
            actionGroup.addAction(action)
            menu.addAction(action)
        icon = QIcon(icons.layer_transparent)
        self.setText('Transparency')
        self.setIcon(icon)
        self.setMenu(menu)
        #self.triggered.connect(self.toggleOpacity)

    # def toggleOpacity(self):
    #     if self.toolBar.canvas.maskItem is None:
    #         return
    #     if self.toolBar.canvas.maskItem.opacity() <= 0.25:
    #         opacity = 0.75
    #     else: 
    #         opacity = 0.25
    #     self.toolBar.canvas.maskItem.setOpacity(opacity)
    #     self.setOpacity(opacity)

    def opacity(self):
        menu = self.menu()
        for action in menu.actions():
            if action.isChecked():
                return action.opacity

    def setOpacity(self, opacity):
        menu = self.menu()
        for action in menu.actions():
            checked = action.opacity == opacity
            action.setChecked(checked)
        
    