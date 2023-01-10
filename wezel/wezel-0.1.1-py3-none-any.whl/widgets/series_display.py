import copy
import numpy as np

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget, 
    QSplitter,
    QVBoxLayout,
    QHBoxLayout, 
)

from wezel import widgets, canvas, MainWidget


class SeriesDisplay(MainWidget):

    def __init__(self):
        super().__init__()
        self.toolBarClass = canvas.ToolBar

        # Widgets
        self.sliders = widgets.SeriesSliders()
        self.canvas = canvas.SeriesCanvas(self)

        # Connections
        self.sliders.valueChanged.connect(self.slidersChanged)
        self.canvas.arrowKeyPress.connect(lambda arrow: self.arrowKeyPress(arrow))
        self.canvas.mousePositionMoved.connect(
            lambda x, y: self.sliders.series.status.pixelValue(x,y,self.canvas.array())
        )

        # Display
        self._view = SeriesDisplayView(self)

    def setToolBarState(self):
        self.toolBar.setWidget(self.canvas)

    def setActive(self, active):
        super().setActive(active)
        if not active:
            self.canvas.saveMask()

    def closeEvent(self, event):
        self.canvas._model.saveRegions()
        
    def setSeries(self, series):
        if series.instances() == []:
            self.setError('Series ' + series.label() + ' is empty. \n\n Nothing to show here..')
            return
        self.sliders.setData(series)
        self.canvas._model._series = series
        image = self.sliders.image
        if image is None:
            return
        image.read()
        self.canvas.setArray(
            image.array(),
            image.SOPInstanceUID, 
            image.WindowCenter, 
            image.WindowWidth, 
            image.colormap,
        )
        image.clear()

    def slidersChanged(self):
        image = self.sliders.image
        if image is None:
            return
        image.read()
        self.canvas.changeArray(
            image.array(), 
            image.SOPInstanceUID, 
            image.WindowCenter, 
            image.WindowWidth, 
            image.colormap,
        )
        image.clear()
        
    def arrowKeyPress(self, key):
        image_before = self.sliders.image
        self.sliders.move(key=key)
        image_after = self.sliders.image
        if image_after != image_before:
            if image_after is None:
                return
            image_after.read()
            self.canvas.changeArray(
                image_after.array(), 
                image_after.SOPInstanceUID, 
                image_after.WindowCenter, 
                image_after.WindowWidth, 
                image_after.colormap,
            )
            image_after.clear()


class SeriesDisplayView():
    def __init__(self, controller):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(controller.canvas)
        layout.addWidget(controller.sliders)
        controller.setLayout(layout)



class SeriesDisplay4D(MainWidget):
    """
    GUI for displaying a 4D numpy array
    """

    def __init__(self): 
        super().__init__()

        self.x = None
        self.y = None

        # Toolbar
        #self.toolBarClass = canvas.ToolBar
        self.toolBarClass = SeriesDisplay4DToolBar

        # Widgets
        self.canvas = canvas.SeriesCanvas(self)
        self.viewSlider = widgets.IndexSlider()
        self.plot = widgets.PlotCurve()
        self.plotSlider = widgets.IndexSlider()

        # Connections
        self.canvas.arrowKeyPress.connect(lambda arrow: self.arrowKeyPress(arrow))
        self.canvas.mousePositionMoved.connect(lambda x, y: self.mouseMoved(x,y))
        self.viewSlider.valueChanged.connect(self.imageChanged)
        self.plotSlider.valueChanged.connect(self.plotChanged)

        # Display
        self._view = SeriesDisplay4DView(self)

    def setActive(self, active):
        super().setActive(active)
        if not active:
            self.canvas.saveMask()

    def closeEvent(self, event):
        self.canvas._model.saveRegions()

    def imageChanged(self):
        z = self.viewSlider.value()
        t = self.plotSlider.value()
        self.canvas.changeArray(
            np.squeeze(self.array[:,:,z,t]),
            self.uid[z,t], 
            self.center[z,t], 
            self.width[z,t], 
            # self.lut[z,t], 
            self.colormap[z,t],
        )
        self.setStatus()
        self.setPlot() 


    def plotChanged(self):
        self.setStatus()
        self.setPlot()        

    def arrowKeyPress(self, arrow):
        if arrow == 'left':
            self.plotSlider.move('down')
        elif arrow == 'right':
            self.plotSlider.move('up')
        elif arrow == 'up':
            self.viewSlider.move('up')
        elif arrow == 'down':
            self.viewSlider.move('down')
        self.imageChanged()

    def mouseMoved(self, x, y):
        self.x = x
        self.y = y
        self.setStatus()
        self.setPlot()

    def setSeries(self, series, sortby=['SliceLocation', 'AcquisitionTime']):
        if series.instances() == []:
            self.setError('Series ' + series.label() + ' is empty. \n\n Nothing to show here..')
            return
        self.canvas._model._series = series
        array, header = series.array(sortby, pixels_first=True)
        series.status.hide()
        self.series = series
        self.array = array[...,0].reshape(array.shape[:4])
        self.zlabel = sortby[0]
        self.tlabel = sortby[1]
        # create index arrays
        # Unnecessary read of all files
        d = self.array.shape
        self.zcoords = np.empty((d[2],d[3]))
        self.tcoords = np.empty((d[2],d[3]))

        self.uid = np.empty((d[2],d[3]), dtype=object)
        self.center = np.empty((d[2],d[3]))
        self.width = np.empty((d[2],d[3]))
        self.colormap = np.empty((d[2],d[3]), dtype=object)

        variables = sortby + ['SOPInstanceUID', 'WindowCenter', 'WindowWidth', 'colormap']
        cnt = 0
        total = d[2]*d[3]
        for z in range(d[2]):
            for t in range(d[3]):
                cnt += 1
                series.status.progress(cnt, total, 'Reading coordinates..')
                values = header[z,t,0][variables]
                self.zcoords[z,t] = values[0]
                self.tcoords[z,t] = values[1]
                self.uid[z,t] = values[2]
                self.center[z,t] = values[3]
                self.width[z,t] = values[4]
                self.colormap[z,t] = values[5]
        series.status.hide()

        self.viewSlider.setMaximum(array.shape[2]-1)
        self.plotSlider.setMaximum(array.shape[3]-1)
        self.plot.setXlabel(self.tlabel)
        self.plot.setYlabel(series.SeriesDescription)
        self.plot.setXlim([np.amin(self.tcoords), np.amax(self.tcoords)])
        self.plot.setYlim([np.amin(self.center-self.width/2), np.amax(self.center+self.width/2)])

        self.refresh()

    def refresh(self):
        self.setStatus()
        self.setCanvas()
        self.setPlot()

    def setStatus(self):
        if self.x is None:
            return
        x = self.x
        y = self.y
        z = self.viewSlider.value()
        t = self.plotSlider.value()
        if (not (0 <= x < self.array.shape[0]) or
            not (0 <= y < self.array.shape[1])):
            msg = self.zlabel + ' = ' + str(self.zcoords[z,t])
            msg += ', ' + self.tlabel + ' = ' + str(self.tcoords[z,t])
        else:
            v = self.array[x,y,z,t]
            msg = 'x = ' + str(x)
            msg += ', y = ' + str(y)
            msg += ', ' + self.zlabel + ' = ' + str(self.zcoords[z,t])
            msg += ', ' + self.tlabel + ' = ' + str(self.tcoords[z,t])
            msg += ', signal = ' + str(v)
        self.series.status.message(msg)

    def setCanvas(self):
        z = self.viewSlider.value()
        t = self.plotSlider.value()
        self.canvas.setArray(
            np.squeeze(self.array[:,:,z,t]),
            self.uid[z,t], 
            self.center[z,t], 
            self.width[z,t], 
            self.colormap[z,t],
        )

    def setPlot(self):
        if self.x is None:
            return
        x = self.x
        y = self.y
        if (not (0 <= x < self.array.shape[0]) or
            not (0 <= y < self.array.shape[1])):
            self.plot.clear()
        else:
            z = self.viewSlider.value()
            t = self.plotSlider.value()
            self.plot.setData(self.tcoords[z,:], self.array[x,y,z,:], index=t)



class SeriesDisplay4DView():

    def __init__(self, controller):

        # Create left panel for viewing images
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(controller.canvas) 
        layout.addWidget(controller.viewSlider) 
        leftPanel = QWidget() 
        leftPanel.setLayout(layout)
        
        # Create right panel for viewing curve plots
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(controller.plot) 
        layout.addWidget(controller.plotSlider) 
        rightPanel = QWidget() 
        rightPanel.setLayout(layout)
        
        # Add left and right panel to splitter
        splitter = QSplitter()
        splitter.addWidget(leftPanel)
        splitter.addWidget(rightPanel)
        splitter.setSizes(2*[controller.geometry().width()/2])
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(splitter)
        controller.setLayout(layout)


class SeriesDisplay4DToolBar(canvas.ToolBar):

    def __init__(self):
        super().__init__()
        self.window.valueChanged.connect(self.setPlotRange)
        self.actionSetDefaultColor.triggered.connect(self.setPlotRange)
        self.filters[2].windowChanged.connect(self.setPlotRange)

    def setWidget(self, widget):
        super().setWidget(widget.canvas)
        self.plot = widget.plot
        self.widget = widget

    def setPlotRange(self):
        center = self.canvas.center()
        width = self.canvas.width()
        xmin = center - width/2
        xmax = center + width/2
        self.plot.setYlim([xmin, xmax])
        self.widget.setPlot()

