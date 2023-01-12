# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2016-2017 European Synchrotron Radiation Facility
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

__authors__ = ["H. Payno"]
__license__ = "MIT"
__date__ = "11/03/2020"

from copy import copy
import os
from orangewidget import gui
from tomwer.core.scan.edfscan import EDFTomoScan
from orangecontrib.tomwer.orange.managedprocess import TomwerWithStackStack
from tomwer.core.scan.hdf5scan import HDF5TomoScan
from tomwer.gui.control.datalist import (
    EDFDataListMainWindow,
)
from nxtomomill.io.config import TomoEDFConfig as EDFConfig
from .NXTomomillOW import _NXTomoMixIn
from tomwer.gui.control.nxtomomill import NXTomomillInput
from tomwer.core.process.control.nxtomomill import EDFToNxProcess
from silx.gui import qt
import logging

logger = logging.getLogger(__name__)


class EDF2NXOW(TomwerWithStackStack, _NXTomoMixIn, ewokstaskclass=EDFToNxProcess):
    """
    Widget to allow user to pick some bliss files and that will convert them
    to HDF5scan.
    """

    name = "edf2nx-nxtomomill"
    id = "orange.widgets.tomwer.control.NXTomomillOW.EDF2NXOW"
    description = "Convert folders with .edf to .nx"
    icon = "icons/edf2nx.svg"
    priority = 121
    keywords = [
        "edf",
        "nexus",
        "tomwer",
        "file",
        "convert",
        "NXTomo",
        "tomography",
        "edf2nx",
        "nxtomomill",
    ]

    want_main_area = True
    want_control_area = False
    resizing_enabled = True
    compress_signal = False

    def __init__(self, parent=None):
        self.__configuration_cache = None
        # cache updated for each folder in order to match `_execute_ewoks_task` design

        TomwerWithStackStack.__init__(self, parent=parent)
        _NXTomoMixIn.__init__(self)
        _layout = gui.vBox(self.mainArea, self.name).layout()
        self.widget = EDFDataListMainWindow(parent=self)
        _layout.addWidget(self.widget)
        # add 'convert auto' check box

        self._convertAutoCB = qt.QCheckBox(
            "convert automatically when edf scan send through 'edf scan' channel", self
        )
        self._convertAutoCB.setChecked(True)
        _layout.addWidget(self._convertAutoCB)

        # connect signal / slot
        self.widget._sendButton.clicked.connect(self._sendAll)
        self.widget._sendSelectedButton.clicked.connect(self._sendSelected)
        self.widget.sigNXTomoCFGFileChanged.connect(self._saveNXTomoCfgFile)
        self.widget.sigUpdated.connect(self._updateSettings)
        self._convertAutoCB.toggled.connect(self._updateSettings)

        # set default configuration is no existing configuration file defined in the settings
        self.update_default_inputs(
            edf_to_nx_configuration=EDFConfig().to_dict(),
        )

        self.task_output_changed_callbacks.add(self._notify_state)

        # handle settings
        self._loadSettings()

    def _updateSettings(self):
        super()._updateSettings()
        self._static_input[
            "convert_auto_edfscan_channel"
        ] = self.convertAutoEDFScanReceivedFromChannel()

    def convertAutoEDFScanReceivedFromChannel(self) -> bool:
        return self._convertAutoCB.isChecked()

    def setConvertAutoEDFScanReceivedFromChannel(self, checked: bool):
        self._convertAutoCB.setChecked(checked)

    def add(self, folder):
        self.widget.add(folder)

    def _saveNXTomoCfgFile(self, cfg_file):
        """save the nxtomofile to the setttings"""
        self._nxtomo_cfg_file = cfg_file
        self._static_input["nxtomomill_cfg_file"] = cfg_file

        if os.path.exists(cfg_file):
            try:
                configuration = EDFConfig.from_cfg_file(cfg_file)
            except Exception as e:
                logger.error(
                    "Fail to use configuration file {}."
                    "Error is {}. No conversion will be done."
                    "".format(cfg_file, e)
                )
            else:
                self.update_default_inputs(
                    edf_to_nx_configuration=configuration.to_dict()
                )
        else:
            self.update_default_inputs(edf_to_nx_configuration=EDFConfig().to_dict())

    def _sendSelected(self):
        self._inputGUI = NXTomomillInput()
        # reset the GUI for input (reset all the cache for answers)
        self._canOverwriteOutputs = False
        for scan_id in self.widget.datalist._myitems:
            tomo_obj = self.widget.datalist.getEDFTomoScan(scan_id, None)
            if tomo_obj:
                self._convertAndSend(tomo_obj)

    def _sendAll(self):
        self._inputGUI = NXTomomillInput()
        # reset the GUI for input (reset all the cache for answers)
        self._canOverwriteOutputs = False
        for scan_id in self.widget.datalist._myitems:
            tomo_obj = self.widget.datalist.getEDFTomoScan(scan_id, None)
            if tomo_obj:
                self._convertAndSend(tomo_obj)

    def _loadSettings(self):
        for scan in self._scans:
            self.widget.add(scan)
        if "nxtomomill_cfg_file" in self._static_input:
            self._nxtomo_cfg_file = self._static_input["nxtomomill_cfg_file"]
            self.widget.setCFGFilePath(self._nxtomo_cfg_file)
        if "output_dir" in self._static_input:
            self.widget.setOutputFolder(self._static_input["output_dir"])
        if "convert_auto_edfscan_channel" in self._static_input:
            self.setConvertAutoEDFScanReceivedFromChannel(
                self._static_input["convert_auto_edfscan_channel"]
            )

    def _convertAndSend(self, edf_scan: EDFTomoScan):
        # cache updated for each folder in order to match `_execute_ewoks_task` design
        # for edf2nx we need to update input dir from the DataList and output_dir from
        # the one requested by the user
        if not isinstance(edf_scan, EDFTomoScan):
            raise TypeError(
                f"edf_scan is expected to be a {EDFTomoScan} not {type(edf_scan)}"
            )

        self.__configuration_cache = EDFConfig.from_dict(
            copy(self.get_default_input_values()["edf_to_nx_configuration"])
        )

        self.__configuration_cache.input_folder = edf_scan.path
        self.__configuration_cache.dataset_basename = edf_scan.dataset_basename

        output_file = EDFToNxProcess.deduce_output_file_path(
            folder_path=edf_scan.path, output_dir=self.widget.getOutputFolder()
        )
        output_entry = "entry"
        self.__configuration_cache.output_file = output_file
        # keep 'edf_to_nx_configuration' up to date according to input folder and output_file updates
        self.update_default_inputs(
            edf_to_nx_configuration=self.__configuration_cache.to_dict()
        )

        self.notify_on_going(scan=HDF5TomoScan(output_file, output_entry))
        self._execute_ewoks_task(propagate=True)

    def get_task_inputs(self):
        return {
            "edf_to_nx_configuration": self.__configuration_cache.to_dict(),
        }

    def handleNewSignals(self) -> None:
        """Invoked by the workflow signal propagation manager after all
        signals handlers have been called.
        """
        # for now we want to avoid propagation any processing.
        # task will be executed only when the user validates the dialog
        edf_scan = super().get_task_inputs().get("edf_scan", None)
        if edf_scan is not None:
            if not isinstance(edf_scan, EDFTomoScan):
                raise TypeError("edf_scan is expected to be an instance of EDFTomoScan")
            self.add(edf_scan.path)
            if self.convertAutoEDFScanReceivedFromChannel():
                self._convertAndSend(edf_scan)

    def _notify_state(self):
        try:
            task_executor = self.sender()
            task_suceeded = task_executor.succeeded
            config = task_executor.current_task.inputs.edf_to_nx_configuration
            config = EDFConfig.from_dict(config)
            scan = HDF5TomoScan(
                config.output_file,
                "entry",
            )
            if task_suceeded:
                self.notify_succeed(scan=scan)
            else:
                self.notify_failed(scan=scan)
        except Exception as e:
            logger.error(f"failed to handle task finished callback. Raiseon is {e}")

    def _get_task_arguments(self):
        adict = super()._get_task_arguments()
        # pop progress as does not fully exists on the orange-widget-base
        adict.pop("progress", None)
        return adict
