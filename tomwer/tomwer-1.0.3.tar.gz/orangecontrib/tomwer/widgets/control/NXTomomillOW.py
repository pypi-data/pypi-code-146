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

from silx.gui import qt
from orangewidget import widget, gui
from tomwer.gui.control.datalist import BlissHDF5DataListMainWindow
from tomwer.core.scan.hdf5scan import HDF5TomoScan, HDF5TomoScanIdentifier
from tomwer.web.client import OWClient
from tomwer.core.process.control.nxtomomill import H5ToNxProcess
import tomwer.core.process.control.nxtomomill
from orangewidget.settings import Setting
from orangewidget.widget import Output, Input
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.core.scan.blissscan import BlissScan
from nxtomomill import converter as nxtomomill_converter
from nxtomomill.io.config import TomoHDF5Config as HDF5Config
from tomwer.gui.control.nxtomomill import NXTomomillInput, OverwriteMessage
import os
import logging

logger = logging.getLogger(__name__)


class _NXTomoMixIn:

    _scans = Setting(list())

    _nxtomo_cfg_file = Setting(str())
    # to keep bacard compatibility (for NXTomomillOW)

    _static_input = Setting(dict())

    def _saveNXTomoCfgFile(self, cfg_file):
        """save the nxtomofile to the setttings"""
        self._nxtomo_cfg_file = cfg_file
        self._static_input["nxtomomill_cfg_file"] = cfg_file

    def _updateSettings(self):
        self._scans = []
        for scan in self.widget.datalist._myitems:
            # kept for backward compatibility since 0.11. To be removed on the future version.
            if "@" in scan:
                entry, file_path = scan.split("@")
                hdf5_tomo_scan = HDF5TomoScan(entry=entry, scan=file_path)
                self.add(hdf5_tomo_scan)
            else:
                self._scans.append(scan)
        self._static_input["output_dir"] = self.widget.getOutputFolder()


class NXTomomillOW(widget.OWBaseWidget, _NXTomoMixIn, OWClient, openclass=True):
    """
    Widget to allow user to pick some bliss files and that will convert them
    to HDF5scan.
    """

    name = "bliss(HDF5)-nxtomomill"
    id = "orange.widgets.tomwer.control.NXTomomillOW.NXTomomillOW"
    description = (
        "Read a bliss .h5 file and extract from it all possible"
        "NxTomo. When validated create a TomwerBaseScan for each "
        "file and entry"
    )
    icon = "icons/nxtomomill.svg"
    priority = 120
    keywords = [
        "hdf5",
        "nexus",
        "tomwer",
        "file",
        "convert",
        "NXTomo",
        "tomography",
        "nxtomomill",
    ]

    want_main_area = True
    want_control_area = False
    resizing_enabled = True
    compress_signal = False

    ewokstaskclass = tomwer.core.process.control.nxtomomill.H5ToNxProcess

    class Inputs:
        data = Input(name="bliss data", type=BlissScan, doc="bliss scan to be process")

    class Outputs:
        data = Output(name="data", type=TomwerScanBase, doc="one scan to be process")

    def __init__(self, parent=None):
        widget.OWBaseWidget.__init__(self, parent)
        OWClient.__init__(self)
        _NXTomoMixIn.__init__(self)
        self.widget = BlissHDF5DataListMainWindow(parent=self)
        layout = gui.vBox(self.mainArea, self.name).layout()
        layout.addWidget(self.widget)
        self.__request_input = True
        # do we ask the user for input if missing
        self._inputGUI = None
        """Gui with cache for missing field in files to be converted"""
        self._canOverwriteOutputs = False
        """Cache to know if we have to ask user permission for overwriting"""

        # expose API
        self.add = self.widget.add
        self.n_scan = self.widget.n_scan
        # alias used for the 'simple workflow' for now
        self.start = self._sendAll

        # connect signal / slot
        self.widget._sendButton.clicked.connect(self._sendAll)
        self.widget._sendSelectedButton.clicked.connect(self._sendSelected)
        self.widget.sigNXTomoCFGFileChanged.connect(self._saveNXTomoCfgFile)
        self.widget.sigUpdated.connect(self._updateSettings)
        # handle settings
        self._loadSettings()

    @property
    def request_input(self):
        return self.__request_input

    @request_input.setter
    def request_input(self, request):
        self.__request_input = request

    def _sendSelected(self):
        """Send a signal for selected scans found to the next widget"""
        self._inputGUI = NXTomomillInput()
        # reset the GUI for input (reset all the cache for answers)
        self._canOverwriteOutputs = False
        for bliss_url in self.widget.datalist.selectedItems():
            identifier = HDF5TomoScanIdentifier.from_str(bliss_url.text())
            self._inputGUI.setBlissScan(
                entry=identifier.data_path, file_path=identifier.file_path
            )
            self._process(bliss_url.text())

    def _sendAll(self):
        """Send a signal for each scan found to the next widget"""
        self._inputGUI = NXTomomillInput()
        # reset the GUI for input (reset all the cache for answers)
        self._canOverwriteOutputs = False
        for bliss_url in self.widget.datalist.selectedItems():
            identifier = HDF5TomoScanIdentifier.from_str(bliss_url.text())
            self._inputGUI.setBlissScan(
                entry=identifier.data_path, file_path=identifier.file_path
            )
            self._process(bliss_url.text())

    def _process(self, bliss_url):
        """

        :param str bliss_url: string at entry@file format
        """
        logger.processStarted("Start translate {} to NXTomo".format(str(bliss_url)))
        identifier = HDF5TomoScanIdentifier.from_str(bliss_url)
        bliss_scan = BlissScan(
            master_file=identifier.file_path,
            entry=identifier.data_path,
            proposal_file=None,
        )
        self._processBlissScan(bliss_scan)

    def _userAgreeForOverwrite(self, file_path):
        if self._canOverwriteOutputs:
            return True
        else:
            msg = OverwriteMessage(self)
            text = "NXtomomill will overwrite \n %s. Do you agree ?" % file_path
            msg.setText(text)
            if msg.exec_():
                self._canOverwriteOutputs = msg.canOverwriteAll()
                return True
            else:
                return False

    @Inputs.data
    def treatBlissScan(self, bliss_scan):
        self._processBlissScan(bliss_scan)

    def _processBlissScan(self, bliss_scan):
        if bliss_scan is None:
            return
        output_file_path = H5ToNxProcess.deduce_output_file_path(
            bliss_scan.master_file,
            entry=bliss_scan.entry,
            outputdir=self.widget.getOutputFolder(),
        )
        # check user has rights to write on the folder
        dirname = os.path.dirname(output_file_path)
        if not os.access(dirname, os.W_OK):
            msg = qt.QMessageBox(self)
            msg.setIcon(qt.QMessageBox.Warning)
            text = (
                "You don't have write rights on {}. Unable to generate "
                "the nexus file associated to {}".format(dirname, str(bliss_scan))
            )
            msg.setWindowTitle("No rights to write")
            msg.setText(text)
            msg.show()
            return
        # check if need to overwrite the file
        elif os.path.exists(output_file_path):
            if not self._userAgreeForOverwrite(output_file_path):
                return

        configuration = self.getHDF5Config()
        if configuration is None:
            return

        # TODO: management of inputs from url: do we want to ignore urls
        # provided ? Or check if the entry receive fit
        # one provided (a root entry for now)
        # force some parameters
        configuration.input_file = bliss_scan.master_file
        configuration.output_file = output_file_path
        configuration.entries = (bliss_scan.entry,)
        configuration.single_file = False
        configuration.overwrite = True
        configuration.request_input = self.request_input
        configuration.file_extension = ".nx"
        if hasattr(configuration, "bam_single_file"):
            configuration.bam_single_file = True
        try:
            convs = nxtomomill_converter.from_h5_to_nx(
                configuration=configuration,
                input_callback=self._inputGUI,
                progress=None,
            )
        except Exception as e:
            logger.processFailed(
                "Fail to convert from bliss file: %s to NXTomo."
                "Conversion error is: %s" % (bliss_scan, e)
            )
        else:
            # in the case of zserie we can have several scan for one entry
            for conv in convs:
                conv_file, conv_entry = conv
                scan_converted = HDF5TomoScan(scan=conv_file, entry=conv_entry)
                logger.processSucceed(
                    "{} has been translated to {}" "".format(bliss_scan, scan_converted)
                )
                self.Outputs.data.send(scan_converted)

    def _loadSettings(self):
        for scan in self._scans:
            assert isinstance(scan, str)
            try:
                self.widget.add(scan)
            except Exception as e:
                logger.error("Fail to add {}. Error is {}".format(scan, e))
            else:
                logger.warning("{} is an invalid link to a file".format(scan))
        if "nxtomomill_cfg_file" in self._static_input:
            nxtomo_cfg_file = self._static_input["nxtomomill_cfg_file"]
        else:
            nxtomo_cfg_file = self._nxtomo_cfg_file
        self.widget.setCFGFilePath(nxtomo_cfg_file)
        if "output_dir" in self._static_input:
            self.widget.setOutputFolder(self._static_input["output_dir"])

    def getHDF5Config(self):
        configuration_file = self.widget.getCFGFilePath()
        if configuration_file in (None, ""):
            configuration = HDF5Config()
        else:
            try:
                configuration = HDF5Config.from_cfg_file(configuration_file)
            except Exception as e:
                logger.error(
                    "Fail to use configuration file {}."
                    "Error is {}. No conversion will be done."
                    "".format(configuration_file, e)
                )
                return None
        return configuration

    def _saveNXTomoCfgFile(self, cfg_file):
        super()._saveNXTomoCfgFile(cfg_file)
        if os.path.exists(cfg_file):
            self.widget.setConfiguration(HDF5Config.from_cfg_file(cfg_file))
