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
__date__ = "15/21/2021"


from tomwer.core.process.reconstruction.nabu.castvolume import CastVolumeTask
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.core.settings import get_lbsram_path, isOnLbsram
from tomwer.core.tomwer_object import TomwerObject
from tomwer.core.utils import isLowOnMemory
from tomwer.core.volume.volumebase import TomwerVolumeBase
from tomwer.core.volume.volumefactory import VolumeFactory
from ..processingstack import FIFO, ProcessingThread
from processview.core.superviseprocess import SuperviseProcess
from processview.core.manager import ProcessManager, DatasetState
from silx.gui import qt
import logging
import functools

_logger = logging.getLogger(__name__)


class CastVolumeProcessStack(FIFO, qt.QObject):
    def __init__(self, process_id=None):
        qt.QObject.__init__(self)
        FIFO.__init__(self, process_id=process_id)
        self._dry_run = False

    def set_dry_run(self, dry_run):
        self._dry_run = dry_run

    def _process(self, data, configuration, callback=None):
        ProcessManager().notify_dataset_state(
            dataset=data,
            process=self,
            state=DatasetState.ON_GOING,
        )
        _logger.processStarted(
            f"start cast volume {str(data.get_identifier())} with parameters {configuration}"
        )

        if isinstance(data, TomwerVolumeBase):
            if data.data_url is not None:
                path = data.data_url.file_path()
            else:
                path = None
        elif isinstance(data, TomwerScanBase):
            path = data.path
        else:
            raise ValueError(
                f"data is expected to be an instance of {TomwerScanBase} or {TomwerVolumeBase}. {type(data)} provided"
            )

        if (
            path is not None
            and isOnLbsram(path)
            and isLowOnMemory(get_lbsram_path()) is True
        ):
            # if computer is running into low memory on lbsram skip it
            mess = f"low memory, skip volume cast {data}"
            ProcessManager().notify_dataset_state(
                dataset=data, process=self._process_id, state=DatasetState.SKIPPED
            )
            _logger.processSkipped(mess)
            if callback is not None:
                callback()
            self.scan_ready(scan=data)
        else:
            self._data_currently_computed = data
            self._computationThread.init(data=data, configuration=configuration)
            # need to manage connect before starting it because
            fct_callback = functools.partial(self._end_threaded_computation, callback)
            self._computationThread.finished.connect(fct_callback)
            self._computationThread.start()

    def _end_computation(self, data, future_tomo_obj, callback):
        """
        callback when the computation thread is finished

        :param scan: pass if no call to '_computationThread is made'
        """
        assert isinstance(data, TomwerObject)
        FIFO._end_computation(
            self, data=data, future_tomo_obj=future_tomo_obj, callback=callback
        )

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
    Thread use to execute the processing of the axis position
    """

    def __init__(self, process_id=None):
        SuperviseProcess.__init__(self, process_id=process_id)
        try:
            ProcessingThread.__init__(self, process_id=process_id)
        except TypeError:
            ProcessingThread.__init__(self)
        self._dry_run = False
        self._scan = None
        self._future_tomo_obj = None
        self._volume = None
        self._configuration = None

    @property
    def future_tomo_obj(self):
        return self._future_tomo_obj

    def set_dry_run(self, dry_run):
        self._dry_run = dry_run

    def init(self, data, configuration):
        if isinstance(data, TomwerVolumeBase):
            self._scan = None
            self._volume = data
        else:
            self._scan = data
            if len(data.latest_vol_reconstructions) < 1:
                raise ValueError(
                    "No reconstructed volume found. did you run the 'nabu volume reconstruction' process ?"
                )
            volume_identifier = data.latest_vol_reconstructions[0]
            self._volume = VolumeFactory.create_tomo_object_from_identifier(
                volume_identifier
            )
        self._data = data
        self._configuration = configuration

    def run(self):
        self.sigComputationStarted.emit()
        cast_volume = CastVolumeTask(
            process_id=self.process_id,
            varinfo=None,
            inputs={
                "volume": self._volume,
                "configuration": self._configuration,
            },
        )
        try:
            cast_volume.run()
        except Exception as e:
            _logger.error(str(e))
            if self._scan is not None:
                # if scan is provided update status because otherwise only the volume state is updated
                ProcessManager().notify_dataset_state(
                    dataset=self._scan,
                    process=self,
                    state=DatasetState.FAILED,
                )
        else:
            if self._scan is not None:
                # if scan is provided update status because otherwise only the volume state is updated
                ProcessManager().notify_dataset_state(
                    dataset=self._scan,
                    process=self,
                    state=DatasetState.SUCCEED,
                )
            if cast_volume.outputs.future_tomo_obj is not None:
                self._future_tomo_obj = cast_volume.outputs.future_tomo_obj
