# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2016-2020 European Synchrotron Radiation Facility
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
# ###########################################################################*/

__authors__ = [
    "H. Payno",
]
__license__ = "MIT"
__date__ = "19/07/2021"


import logging
from silx.gui import qt
from tomwer.core.scan.scanbase import TomwerScanBase
from orangecontrib.tomwer.widgets.utils import WidgetLongProcessing
from orangewidget.settings import Setting
from orangewidget import gui
from orangewidget.widget import Input, Output
from ...orange.managedprocess import SuperviseOW
from tomwer.gui.reconstruction.normalization.intensity import (
    SinoNormWindow as _SinoNormWindow,
)
from tomwer.synctools.stacks.reconstruction.normalization import (
    INormalizationProcessStack,
)
from processview.core.manager import ProcessManager
from processview.core.manager import DatasetState
from tomwer.core.process.reconstruction.normalization import (
    SinoNormalizationTask,
)
from tomwer.core import settings
from tomwer.core import utils
from tomoscan.normalization import Method as NormMethod
from tomwer.core.process.reconstruction.normalization.params import _ValueSource
import functools

_logger = logging.getLogger(__name__)


class SinoNormWindow(_SinoNormWindow):
    """
    implementation of NormIntensityWindow for orange. Add a lock processing
    and a processing stack
    """

    sigValidate = qt.Signal()

    def __init__(self, parent, process_id=None):
        assert isinstance(parent, SinoNormOW)
        super().__init__(parent)
        self._parentValidate = self.parent()._validate
        self._processing_stack = INormalizationProcessStack(process_id=process_id)
        # connect signal / slot
        self._optsWidget.sigProcessingRequested.connect(self._processCurrentScan)

    def _validated(self):
        scan = self.getScan()
        self._parentValidate(scan)

    def _processCurrentScan(self):
        scan = self.getScan()
        if scan is None:
            return
        self._processScan(scan)

    def _processScan(self, scan):
        self._processing_stack.add(
            data=scan,
            configuration=self.getConfiguration(),
            callback=functools.partial(
                self._mightUpdateResult,
                scan,
                self.isLocked(),
            ),
        )

    def _mightUpdateResult(self, scan, validate):
        extra_info = scan.intensity_normalization.get_extra_infos()
        if "value" in extra_info:
            self.setResult(result=extra_info["value"])
        else:
            self.setResult(None)
        if validate is True:
            self._parentValidate(scan)


class SinoNormOW(WidgetLongProcessing, SuperviseOW):
    """
    A simple widget managing the copy of an incoming folder to an other one

    :param parent: the parent widget
    """

    # note of this widget should be the one registered on the documentation
    name = "sino normalization"
    id = "orange.widgets.tomwer.reconstruction.SinoNormOW.SinoNormOW"
    description = "Define normalization on intensity to be applied on projections"
    icon = "icons/norm_I.svg"
    priority = 28
    keywords = [
        "tomography",
        "normalization",
        "norm",
        "I",
        "intensity",
        "projections",
        "radios",
    ]

    want_main_area = True
    resizing_enabled = True
    compress_signal = False
    allows_cycle = True

    _rpSetting = Setting(dict())

    sigScanReady = qt.Signal(TomwerScanBase)
    "Signal emitted when a scan is ended"

    class Inputs:
        data_in = Input(name="data", type=TomwerScanBase)

    class Outputs:
        data_out = Output(name="data", type=TomwerScanBase)

    def __init__(self, parent=None):
        """
        Widget allowing the user to define the normalization to be applied on
        projections. This can be a scalar or an array.
        """
        SuperviseOW.__init__(self, parent)
        WidgetLongProcessing.__init__(self)

        self._window = SinoNormWindow(self, process_id=self.process_id)

        self._layout = gui.vBox(self.mainArea, self.name).layout()
        self._layout.setContentsMargins(0, 0, 0, 0)

        self._layout.addWidget(self._window)
        try:
            self.loadSettings()
        except Exception as e:
            _logger.warning(f"Failed to load settings: {e}")

        # connect signal / slot
        self._window.sigConfigurationChanged.connect(self._updateSettings)
        self.destroyed.connect(self._window.stop)
        self._window._processing_stack.sigComputationStarted.connect(
            self._startProcessing
        )
        self._window._processing_stack.sigComputationEnded.connect(self._endProcessing)

    def isLocked(self):
        return self._window.isLocked()

    def setLocked(self, locked):
        self._window.setLocked(locked)

    def setCurrentMethod(self, mode):
        self._window.setCurrentMethod(mode)

    def getCurrentMethod(self):
        return self._window.getCurrentMethod()

    def setCurrentSource(self, source):
        self._window.setCurrentSource(source)

    def getCurrentSource(self):
        return self._window.getCurrentSource()

    @Inputs.data_in
    def process(self, scan: TomwerScanBase):
        if not isinstance(scan, (TomwerScanBase, type(None))):
            raise TypeError(
                "scan should be None or an instance of "
                "TomwerScanBase. Not {}".format(type(scan))
            )
        if scan is None:
            return

        self._skipCurrentScan(new_scan=scan)
        if settings.isOnLbsram(scan) and utils.isLowOnMemory(
            settings.get_lbsram_path()
        ):
            details = "skip {} because low memory on lbsram".format(str(scan))
            self.notify_skip(scan=scan, details=details)
            self.Outputs.data_out.send(scan)
        else:
            self._window.setScan(scan=scan)

            if self.isLocked():
                self._window._processScan(scan=scan)

    def _validate(self, scan):
        if scan is None:
            return

        # save processing result for the one with interaction. Otherwise
        # this will be saved in the processing thread
        extra_infos = scan.intensity_normalization.get_extra_infos()
        tomwer_processing_res_code = extra_infos.pop(
            "tomwer_processing_res_code", "unprocessed"
        )
        SinoNormalizationTask._register_process(
            process_file=scan.process_file,
            process=SinoNormalizationTask,
            entry=scan.entry,
            configuration=self.getConfiguration(),
            results={
                "method": scan.intensity_normalization.method.value,
                "extra_infos": extra_infos,
            },
            process_index=scan.pop_process_index(),
        )
        if tomwer_processing_res_code is True:
            # if defined by manual scalar we need to set the value
            if extra_infos.get("source", None) == _ValueSource.MANUAL_SCALAR.value:
                extra_infos["value"] = self.getCurrentlyDefinedValues()
            self.notify_succeed(scan=scan)
        elif tomwer_processing_res_code is False:
            self.notify_failed(scan=scan)
        elif tomwer_processing_res_code is None:
            self.notify_skip(scan=scan)
        elif tomwer_processing_res_code == "unprocessed":
            # if validate manually we must set current method + value
            scan.intensity_normalization = self.getCurrentMethod()

            if self.getCurrentMethod() in (
                NormMethod.NONE,
                NormMethod.CHEBYSHEV,
                NormMethod.LSQR_SPLINE,
            ):
                extra_infos = {}
            elif self.getCurrentSource() is _ValueSource.DATASET:
                extra_infos = {
                    "dataset_url": self._window._optsWidget._datasetWidget.getDatasetUrl().path(),
                }
            else:
                extra_infos = {
                    "value": self.getCurrentlyDefinedValues(),
                    "source": self.getCurrentSource(),
                }
            self.notify_succeed(scan=scan)
        # clear flag
        scan.intensity_normalization.set_extra_infos(extra_infos)

        self.Outputs.data_out.send(scan)

    def _skipCurrentScan(self, new_scan):
        scan = self._window.getScan()
        # if the same scan has been run several scan
        if scan is None or str(scan) == str(new_scan):
            return
        current_scan_state = ProcessManager().get_dataset_state(
            dataset_id=scan.get_identifier(), process=self
        )
        if current_scan_state in (
            DatasetState.PENDING,
            DatasetState.WAIT_USER_VALIDATION,
        ):
            details = "Was pending and has been replaced by another scan."
            self.notify_skip(scan=scan, details=details)
            self.Outputs.data_out.send(scan)

    def getCurrentlyDefinedValues(self):
        return self._window._crtWidget.getResult()

    def validateCurrentScan(self):
        scan = self._window.getScan()
        self._validate(scan)

    def clear(self):
        self._window.clear()

    def getConfiguration(self):
        return self._window.getConfiguration()

    def stop(self):
        self._window.stop()

    def _updateSettings(self):
        self._rpSetting = self._window.getConfiguration()
        self._rpSetting["__lock__"] = self.isLocked()

    def loadSettings(self):
        self._window.setConfiguration(self._rpSetting)
        if "__lock__" in self._rpSetting:
            self.setLocked(self._rpSetting["__lock__"])
