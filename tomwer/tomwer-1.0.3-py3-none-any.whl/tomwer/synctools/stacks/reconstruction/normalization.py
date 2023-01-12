# coding: utf-8
###########################################################################
# Copyright (C) 2016-2019 European Synchrotron Radiation Facility
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
#############################################################################

__authors__ = ["H.Payno"]
__license__ = "MIT"
__date__ = "19/07/2021"


from tomwer.core.process.reconstruction.normalization import (
    SinoNormalizationTask,
)
from processview.core.manager import ProcessManager
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.core.settings import get_lbsram_path, isOnLbsram
from tomwer.core.utils import isLowOnMemory
from processview.core.manager import DatasetState
from ..processingstack import FIFO, ProcessingThread
from processview.core.superviseprocess import SuperviseProcess
from silx.gui import qt
import functools
import logging

_logger = logging.getLogger(__name__)


class INormalizationProcessStack(FIFO, qt.QObject):
    """Implementation of the `.AxisProcess` but having a stack for treating
    scans and making computation in threads"""

    def __init__(self, process_id=None):
        qt.QObject.__init__(self)
        FIFO.__init__(self, process_id=process_id)

    def _process(self, data, configuration, callback=None):
        ProcessManager().notify_dataset_state(
            dataset=data,
            process=self,
            state=DatasetState.ON_GOING,
        )
        _logger.processStarted("start intensity normalization {}".format(str(data)))
        assert isinstance(data, TomwerScanBase)
        if isOnLbsram(data) and isLowOnMemory(get_lbsram_path()) is True:
            # if computer is running into low memory on lbsram skip it
            mess = "low memory, skip intensity normalization", data.path
            ProcessManager().notify_dataset_state(
                dataset=data, process=self._process_id, state=DatasetState.SKIPPED
            )
            _logger.processSkipped(mess)
            if callback is not None:
                callback()
            self.scan_ready(scan=data)
        else:
            self._data_currently_computed = data
            self._computationThread.init(data=data, i_norm_params=configuration)
            # need to manage connect before starting it because
            fct_callback = functools.partial(self._end_threaded_computation, callback)
            self._computationThread.finished.connect(fct_callback)
            self._computationThread.start()

    def _end_threaded_computation(self, callback=None):
        assert self._data_currently_computed is not None
        self._computationThread.finished.disconnect()
        if callback:
            callback()
        FIFO._end_threaded_computation(self)

    def _create_processing_thread(self, process_id=None) -> qt.QThread:
        return _ProcessingThread(process_id=process_id)


class _ProcessingThread(ProcessingThread, SuperviseProcess):
    """
    Thread use to execute the processing of intensity normalization
    (mostly load io and compute the mean / median on it)
    """

    def __init__(self, process_id=None):
        SuperviseProcess.__init__(self, process_id=process_id)
        ProcessingThread.__init__(self, process_id=process_id)
        self.center_of_rotation = None
        self._dry_run = False
        self._scan = None
        self._i_norm_params = None

    def init(self, data, i_norm_params):
        self._scan = data
        self._i_norm_params = i_norm_params

    def run(self):
        self.sigComputationStarted.emit()
        norm_process = SinoNormalizationTask(
            process_id=self.process_id,
            varinfo=None,
            inputs={
                "data": self._scan,
                "configuration": self._i_norm_params,
            },
        )
        try:
            norm_process.run()
        except Exception as e:
            _logger.error(str(e))
            mess = "Intensity normalization computation for {} failed.".format(
                str(self._scan)
            )
            state = DatasetState.FAILED
        else:
            mess = "Intensity normalization computation for {} succeed.".format(
                str(self._scan)
            )
            state = DatasetState.WAIT_USER_VALIDATION

        ProcessManager().notify_dataset_state(
            dataset=self._scan,
            process=self,
            state=state,
            details=mess,
        )
