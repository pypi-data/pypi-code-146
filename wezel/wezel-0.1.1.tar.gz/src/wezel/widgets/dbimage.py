import timeit
import numpy as np
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import (QToolBar,
    QAction, QComboBox, QPushButton, QLabel, 
    QWidget, QDoubleSpinBox, QHBoxLayout, QVBoxLayout)
from PyQt5.QtGui import QIcon, QPixmap

from wezel import widgets, icons

listColors =  ['gray', 'cividis',  'magma', 'plasma', 'viridis', 
    'Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
    'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
    'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn',
    'binary', 'gist_yarg', 'gist_gray', 'bone', 'pink',
    'spring', 'summer', 'autumn', 'winter', 'cool', 'Wistia',
    'hot', 'afmhot', 'gist_heat', 'copper',
    'PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu',
    'RdYlBu', 'RdYlGn', 'Spectral', 'coolwarm', 'bwr', 'seismic',
    'twilight', 'twilight_shifted', 'hsv',
    'flag', 'prism', 'ocean', 'gist_earth', 'terrain', 'gist_stern',
    'gnuplot', 'gnuplot2', 'CMRmap', 'cubehelix', 'brg', 'turbo',
    'gist_rainbow', 'rainbow', 'jet', 'nipy_spectral', 'gist_ncar']

QComboBoxStyleSheet = """

QComboBox::drop-down 
{
    border: 0px; /* This seems to replace the whole arrow of the combo box */
}
QComboBox:down-arrow 
{
    image: url("icons/fugue_icons/spectrum.png");
    width: 14px;
    height: 14px;
}
"""


class ImageWindow(QWidget):
    """Widget to set and manage color and window settings of a Series"""

    valueChanged = pyqtSignal(list)  # emitted when the color settings are changed by the widget

    def __init__(self, layout=True):
        super().__init__()
        self._setWidgets(layout)
        self._setConnections()
        if layout:
            self._setLayout()

    def _setWidgets(self, layout):
        self.mode = LockUnlockWidget(toolTip = 'Lock image settings')
        self.brightness = ImageBrightness(layout=layout)
        self.contrast = ImageContrast(layout=layout)

    def _setConnections(self):
        self.brightness.valueChanged.connect(self._valueChanged)
        self.contrast.valueChanged.connect(self._valueChanged)

    def _setLayout(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        #layout.addWidget(self.mode)
        layout.addWidget(self.brightness)
        layout.addWidget(self.contrast)
        #self.setStyleSheet("background-color: white")
        self.setLayout(layout)

    def _valueChanged(self):
        self.valueChanged.emit(self.getValue())

    def setData(self, array, center, width, set=None):
        min = np.amin(array)
        max = np.amax(array)
        if set is None:
            set = not self.mode.isLocked
        self.brightness.setData(min, max, center, set)
        self.contrast.setData(min, max, width, set)

    def getValue(self):
        return [
            self.brightness.getValue(),
            self.contrast.getValue(),
        ]

    def setValue(self, WindowCenter=None, WindowWidth=None):
        self.brightness.setValue(WindowCenter)
        self.contrast.setValue(WindowWidth)


class ImageContrast(QWidget):

    valueChanged = pyqtSignal(float)

    def __init__(self, layout=True):
        super().__init__()

        self.label = QLabel()
        self.label.setPixmap(QPixmap(icons.contrast))
        #self.label.setFixedSize(24, 24)
        self.spinBox = QDoubleSpinBox()
        self.spinBox.valueChanged.connect(self.spinBoxValueChanged)
        self.spinBox.setToolTip("Adjust Contrast")
        self.spinBox.setMinimum(0)
        self.spinBox.setMaximum(1000000000.00)
        self.spinBox.setWrapping(False)
        self.spinBox.setFixedWidth(115)
        if layout:
            self.layout = QHBoxLayout()
            self.layout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            self.layout.setContentsMargins(0,0,0,0)
            self.layout.setSpacing(2)
            self.layout.addWidget(self.spinBox)
            self.layout.addWidget(self.label)
            #self.setMaximumWidth(120)
            self.setLayout(self.layout)

    def setData(self, min, max, width, set=True):
        self.spinBox.blockSignals(True)
        if width is None: 
            self.spinBox.setValue(1)  
            self.spinBox.setSingleStep(0.1)
        else:
            if set:  # adjust spinbox value to image contrast
                self.spinBox.setValue(width)
        self.setSpinBoxStepSize(min, max)
        self.spinBox.blockSignals(False)

    def getValue(self):
        return self.spinBox.value()

    def setValue(self, value):
        self.spinBox.blockSignals(True)
        self.spinBox.setValue(value)
        self.spinBox.blockSignals(False)

    def setSpinBoxStepSize(self, min, max):
        if min is None:
            return
        width = max-min
        spinBoxStep = float(width / 10)
        self.spinBox.setSingleStep(spinBoxStep)

    def spinBoxValueChanged(self):
        """Update Window Width of the image."""
        width = self.spinBox.value()   
        self.valueChanged.emit(width)


class ImageBrightness(QWidget):

    valueChanged = pyqtSignal(float)

    def __init__(self, layout=True):
        super().__init__() 
        self.label = QLabel()
        self.label.setPixmap(QPixmap(icons.brightness))
        #self.label.setFixedSize(24, 24)
        self.spinBox = QDoubleSpinBox()
        self.spinBox.valueChanged.connect(self.spinBoxValueChanged)
        self.spinBox.setToolTip("Adjust Brightness")
        self.spinBox.setMinimum(-1000000000.00)
        self.spinBox.setMaximum(+1000000000.00)
        self.spinBox.setWrapping(False)
        self.spinBox.setFixedWidth(115)
        if layout:
            self.layout = QHBoxLayout()
            self.layout.setAlignment(Qt.AlignLeft  | Qt.AlignVCenter)
            self.layout.setContentsMargins(0,0,0,0)
            self.layout.setSpacing(2)
            self.layout.addWidget(self.spinBox)
            self.layout.addWidget(self.label)
            #self.setMaximumWidth(120)
            self.setLayout(self.layout)

    def setData(self, min, max, center, set=True):
        self.spinBox.blockSignals(True)
        if min is None: 
            self.spinBox.setValue(1)  
            self.spinBox.setSingleStep(0.1)
        else:
            if set:  # adjust spinbox value to image contrast
                self.spinBox.setValue(center)
        self.setSpinBoxStepSize(min, max)
        self.spinBox.blockSignals(False)

    def getValue(self):
        return self.spinBox.value()

    def setValue(self, center):
        self.spinBox.blockSignals(True)
        self.spinBox.setValue(center)
        self.spinBox.blockSignals(False)

    def setSpinBoxStepSize(self, min, max):
        if min is None:
            return
        center = (max+min)/2
        spinBoxStep = float(center / 10)
        self.spinBox.setSingleStep(spinBoxStep)

    def spinBoxValueChanged(self):
        center = self.spinBox.value()
        self.valueChanged.emit(center)



class LockUnlockWidget(QToolBar):

    toggled = pyqtSignal()

    def __init__(self, toolTip = 'Lock state'):
        super().__init__()
        self.isLocked = True
        self.icon_lock = QIcon(icons.lock) 
        self.icon_lock_unlock = QIcon(icons.lock_unlock) 
        self.mode = QAction()
        self.mode.setIcon(self.icon_lock)
        self.mode.setToolTip(toolTip)
        self.mode.triggered.connect(self.toggle) 
        self.addAction(self.mode)

    def toggle(self):
        if self.isLocked == True:
            self.mode.setIcon(self.icon_lock_unlock)
            self.isLocked = False
        elif self.isLocked == False:
            self.mode.setIcon(self.icon_lock)
            self.isLocked = True  
        self.toggled.emit()



class DeleteImageButton(QPushButton):

    buttonClicked = pyqtSignal()

    def __init__(self, image=None):
        super().__init__()
        self.setFixedSize(24, 24)
        self.setIcon(QIcon(icons.bin_metal))
        self.setToolTip('Delete image')
        self.clicked.connect(self.delete) 
        self.setData(image)

    def delete(self):
        if self.image is None:
            return
        self.image.remove()
        self.buttonClicked.emit()

    def setData(self, image):
        self.image = image


class ExportImageButton(QPushButton):

    def __init__(self, image=None):
        super().__init__()
 
        self.setFixedSize(24, 24)
        self.setIcon(QIcon(icons.blue_document_export))
        self.setToolTip('Export as .png')
        self.clicked.connect(self.export)
        self.setData(image)

    def setData(self, image):
        self.image = image

    def export(self):
        """Export as png."""
        if self.image is None: 
            return
        path = self.image.dialog.directory("Where do you want to export the data?")
        self.image.export_as_png(path)


class RestoreImageButton(QPushButton):

    buttonClicked = pyqtSignal()

    def __init__(self, image=None):
        super().__init__()
        self.setFixedSize(24, 24)
        self.setIcon(QIcon(icons.arrow_curve_180_left))
        self.setToolTip('Undo changes')
        self.clicked.connect(self.restore) 
        self.setData(image)

    def setData(self, image):
        self.image = image

    def restore(self):
        if self.image is None: 
            return
        self.image.restore()
        self.buttonClicked.emit()


class SaveImageButton(QPushButton):

    buttonClicked = pyqtSignal()

    def __init__(self, image=None):
        super().__init__()

        self.setFixedSize(24, 24)
        self.setIcon(QIcon(icons.disk))
        self.setToolTip('Save changes')
        self.clicked.connect(self.save) 

        self.setData(image)

    def save(self):
 
        if self.image is None:
            return
        self.image.save()
        self.buttonClicked.emit()

    def setData(self, image):
        self.image = image

