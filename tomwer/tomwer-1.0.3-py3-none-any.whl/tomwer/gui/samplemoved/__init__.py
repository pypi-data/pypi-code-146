# /*##########################################################################
# Copyright (C) 2017 European Synchrotron Radiation Facility
#
# This file is part of the PyMca X-ray Fluorescence Toolkit developed at
# the ESRF by the Software group.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
#############################################################################*/
"""Some widget construction to check if a sample moved"""

__author__ = ["H. Payno"]
__license__ = "MIT"
__date__ = "19/03/2018"


from collections import OrderedDict
import weakref
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.gui.samplemoved.selectiontable import AngleSelectionTable
from tomoscan.esrf.scan.utils import get_data
from silx.gui import qt
import silx.io.utils
import silx.io.url
import logging

from tomwer.gui.settings import Y_AXIS_DOWNWARD

_logger = logging.getLogger(__name__)
try:
    from silx.gui.plot.CompareImages import CompareImages
except ImportError:
    _logger.warning("silx >0.7 should be installed to access the SampleMovedWidget")


class SampleMovedWidget(qt.QMainWindow):
    """
    Widget used to display two images with different color channel.
    The goal is to see if the sample has moved during acquisition.
    """

    CONFIGURATIONS = OrderedDict(
        [
            ("0-0(1)", (("0", "0.0", 0), ("0(1)", "0.0 (1)"))),
            ("90-90(1)", (("90", "90.0", 90), ("90(1)", "90.0 (1)"))),
            ("180-180(1)", (("180", "180.0", 180), ("180(1)", "180.0 (1)"))),
            ("270-270(1)", (("270", "270.0", 270), ("270(1)", "270.0 (1)"))),
            ("360-0", (("360", "360.0", 360), ("0", "0.0"))),
        ]
    )
    """Define possible configurations for comparison. Key is the name of the
    configuration, value contains a couple valid values for the necessary
    two projections
    """

    def __init__(self, parent=None):
        qt.QMainWindow.__init__(self, parent)
        self._scan = None
        self.setWindowFlags(qt.Qt.Widget)
        self._isConnected = False
        self._images = {}
        self._symmetricalStates = {"first": False, "second": False}
        self._plot = CompareImages(parent=self)
        self._plot.setWindowFlags(qt.Qt.Widget)
        self._plot.getPlot().setYAxisInverted(Y_AXIS_DOWNWARD)
        self._on_load_callback = []

        self._topWidget = self.getControlWidget()

        self._dockWidgetMenu = qt.QDockWidget(parent=self)
        self._dockWidgetMenu.layout().setContentsMargins(0, 0, 0, 0)
        self._dockWidgetMenu.setFeatures(qt.QDockWidget.DockWidgetMovable)
        self._dockWidgetMenu.setWidget(self._topWidget)
        self.addDockWidget(qt.Qt.BottomDockWidgetArea, self._dockWidgetMenu)

        self._plotsWidget = qt.QWidget(parent=self)
        self._plotsWidget.setLayout(qt.QHBoxLayout())

        self._plotsWidget.layout().addWidget(self._plot)
        self.setCentralWidget(self._plotsWidget)

        if hasattr(self._selectorCB, "currentTextChanged"):
            self._selectorCB.currentTextChanged.connect(self.setConfiguration)
        else:
            self._selectorCB.currentIndexChanged["QString"].connect(
                self.setConfiguration
            )

        self._selectionTable.sigImageAChanged.connect(self._setConfigManual)
        self._selectionTable.sigImageBChanged.connect(self._setConfigManual)

        # expose API
        self.setSelection = self._selectionTable.setSelection

    def getControlWidget(self):
        if hasattr(self, "_topWidget"):
            return self._topWidget
        self._topWidget = qt.QWidget(parent=self)

        self._configWidget = qt.QWidget(parent=self._topWidget)
        self._configWidget.setLayout(qt.QHBoxLayout())

        self._configWidget.layout().addWidget(
            qt.QLabel("Configuration:", parent=self._topWidget)
        )
        self._selectorCB = qt.QComboBox(parent=self._topWidget)
        self._configWidget.layout().addWidget(self._selectorCB)

        self._selectionTable = AngleSelectionTable(parent=self._topWidget)
        self._topWidget.setLayout(qt.QVBoxLayout())
        self._topWidget.layout().setContentsMargins(0, 0, 0, 0)

        self._topWidget.layout().addWidget(self._configWidget)
        self._topWidget.layout().addWidget(self._selectionTable)

        self._selectionTable.sigImageAChanged.connect(self._changeImageA)
        self._selectionTable.sigImageBChanged.connect(self._changeImageB)
        return self._topWidget

    def setOnLoadAction(self, action):
        self._on_load_callback.append(action)

    def clearOnLoadActions(self):
        self._on_load_callback = []

    def clear(self):
        self._selectorCB.clear()
        self._selectionTable.clear()
        self._images = {}

    @property
    def scan(self):
        if self._scan is None or self._scan() is None:
            return None
        else:
            return self._scan()

    def setScan(self, scan):
        if scan is None:
            self._scan = None
        elif not isinstance(scan, TomwerScanBase):
            raise TypeError(
                f"scan is expected to be None or an instance of {TomwerScanBase}. {type(scan)} provided"
            )
        else:
            self._scan = weakref.ref(scan)

    def setImages(self, images):
        """
        Set the images in a key value system. Key should be in
        (0, 90, 180, 270) and the value should be the image.

        images value can be str (path to the file) or data

        :param dict images: images to set. key is index or file name, value
                            the image.
        """
        self.clear()
        self._images = images

        # update the default config
        self._selectorCB.clear()

        def contains_at_least_one_key(keys):
            for key in keys:
                if key in images.keys():
                    return True
            return False

        self._selectorCB.blockSignals(True)
        for config in self.CONFIGURATIONS:
            proj_0_keys, proj_1_keys = self.CONFIGURATIONS[config]
            if contains_at_least_one_key(proj_0_keys) and contains_at_least_one_key(
                proj_1_keys
            ):
                self._selectorCB.addItem(config)
        self._selectorCB.addItem("manual")

        for angleValue, file_path in images.items():
            self._selectionTable.addRadio(name=file_path, angle=angleValue)
        self._selectorCB.setCurrentIndex(0)
        self._selectorCB.blockSignals(False)
        if hasattr(self._selectorCB, "currentTextChanged"):
            self._selectorCB.currentTextChanged.emit(self._selectorCB.currentText())
        else:
            self._selectorCB.currentIndexChanged["QString"].emit(
                self._selectorCB.currentText()
            )

    def _updatePlot(self):
        imgA, imgB = self._selectionTable.getSelection()
        dataImgA = self._changeImageA(imgA)
        dataImgB = self._changeImageA(imgB)
        if dataImgA is not None and dataImgB is not None:
            self._plot.setData(image1=dataImgA, image2=dataImgB)

    def _changeImageA(self, img):
        if img is not None:
            imgAUrl = silx.io.url.DataUrl(path=img)
            if self.scan is None:
                dataImgA = get_data(imgAUrl)
            else:
                idxImgA = self.scan.get_url_proj_index(imgAUrl)
                dataImgA = self.scan.flat_field_correction((imgAUrl,), (idxImgA,))[0]
            self._plot.setImage1(image1=dataImgA)
            return dataImgA

    def _changeImageB(self, img):
        if img is not None:
            imgBUrl = silx.io.url.DataUrl(path=img)
            if self.scan is None:
                dataImgB = get_data(imgBUrl)
            else:
                idxImgB = self.scan.get_url_proj_index(imgBUrl)
                dataImgB = self.scan.flat_field_correction((imgBUrl,), (idxImgB,))[0]
            self._plot.setImage2(image2=dataImgB)
            return dataImgB

    def setConfiguration(self, config):
        if config == "manual":
            return
        if config not in self.CONFIGURATIONS:
            _logger.warning("Undefined configuration: %s" % config)
            return

        self._selectionTable.blockSignals(True)
        self._selectionTable.setAngleSelection(
            self.CONFIGURATIONS[config][0], self.CONFIGURATIONS[config][1]
        )
        self._updatePlot()
        self._selectionTable.blockSignals(False)

    def _setConfigManual(self):
        indexItemManual = self._selectorCB.findText("manual")
        if indexItemManual >= 0:
            self._selectorCB.setCurrentIndex(indexItemManual)
