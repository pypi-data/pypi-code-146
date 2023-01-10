
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

from PyQt5.QtWidgets import QWidget, QVBoxLayout

class PlotCurve(QWidget):

    def __init__(self):
        super().__init__()

        self.figure = plt.figure()
        self.figure.set_visible(True)
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.xLabel = 'x-label'
        self.yLabel = 'y-label'
        self.xLim = None
        self.yLim = None
       
        self.subPlot = self.figure.add_subplot(111)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def setXlim(self, xLim):
        self.xLim = xLim

    def setYlim(self, yLim):
        self.yLim = yLim

    def setXlabel(self, label):
        self.xLabel = label

    def setYlabel(self, label):
        self.yLabel = label

    def clear(self):
        self.subPlot.clear()
        self.canvas.draw()

    def setData(self, x, y, index=None):
        self.subPlot.clear()
        self.subPlot.tick_params(
            axis='both', 
            which='major', 
            labelsize=10)
        if self.xLim is not None:
            self.subPlot.set_xlim(self.xLim)
        if self.yLim is not None:
            self.subPlot.set_ylim(self.yLim)
        self.subPlot.set_xlabel(
            self.xLabel, loc='center', 
            va='top', fontsize=10)
        self.subPlot.set_ylabel(
            self.yLabel, loc='center', 
            fontsize=10)
        self.subPlot.grid()
        self.subPlot.plot(x, y)
        if index is not None:
            self.subPlot.plot(x[index], y[index], 'bo')
        self.canvas.draw()
