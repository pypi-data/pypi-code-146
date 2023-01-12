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

__authors__ = ["C. Nemoz", "H. Payno"]
__license__ = "MIT"
__date__ = "13/08/2021"


import logging
import shutil
from typing import Union
from silx.gui import qt
from tomwer.core.process.reconstruction.darkref.darkrefscopy import DarkRefsCopy
from tomwer.io.utils import get_default_directory
from tomwer.core import settings
from tomwer.core import utils
from tomwer.gui.reconstruction.darkref.darkrefwidget import DarkRefWidget
from silx.io.url import DataUrl
from silx.gui.dialog.DataFileDialog import DataFileDialog

_logger = logging.getLogger(__name__)


class DarkRefAndCopyWidget(DarkRefWidget):
    """
    Widget associated to the DarkRefCopy process
    """

    sigModeAutoChanged = qt.Signal()
    """Signal emitted when the mode auto change"""
    sigCopyActivationChanged = qt.Signal()
    """Signal emitted when the copy is activated or deactivated"""

    def __init__(self, save_dir: str, parent=None, reconsparams=None, process_id=None):
        DarkRefWidget.__init__(
            self, parent=parent, reconsparams=reconsparams, process_id=process_id
        )
        self._mode_auto = True

        self._refCopyWidget = RefCopyWidget(
            parent=self, save_dir=save_dir, refCopy=self
        )
        iCopy = self.mainWidget.addTab(self._refCopyWidget, "copy")
        tooltip = (
            "When copy is activated it will record refHST and dark "
            "files. \n Then when an acquisition without dark or refHST "
            "go through the widget it will copy those dark and refHST "
            "in the acquisition."
        )
        self.mainWidget.setTabToolTip(iCopy, tooltip)
        self.layout().setContentsMargins(0, 0, 0, 0)

        # connect signal / slot
        self._refCopyWidget.sigModeAutoChanged.connect(self._triggerModeAuto)
        self._refCopyWidget.sigCopyActivationChanged.connect(
            self._triggerCopyActivation
        )

    def setRefSetBy(self, scan_id: str):
        self._refCopyWidget._statusBar.showMessage(f"ref set from {scan_id}")

    def set_mode_auto(self, auto):
        self._mode_auto = auto

    def setRefsFromScan(self, value):
        raise NotImplementedError()

    def _triggerModeAuto(self, *args, **kwargs):
        self.sigModeAutoChanged.emit()

    def _triggerCopyActivation(self, *args, **kwargs):
        self.sigCopyActivationChanged.emit()

    def setCopyActive(self, active):
        self._refCopyWidget.setChecked(active)

    def isCopyActive(self):
        return self._refCopyWidget.isChecked()

    def setModeAuto(self, mode_auto):
        old = self.blockSignals(True)
        self._refCopyWidget.setModeAuto(mode_auto)
        self.blockSignals(old)

    def isOnModeAuto(self):
        return self._refCopyWidget.is_on_mode_auto()

    def close(self):
        self.blockSignals(True)
        self._refCopyWidget.close()
        super(DarkRefAndCopyWidget, self).close()

    def _dealWithMissingRef(self, scanID):
        # Security: if lbs is full, skip requesting fir user ref
        if (
            settings.isOnLbsram(scanID)
            and utils.isLowOnMemory(settings.get_lbsram_path()) is True
        ):
            # if computer is running into low memory on lbsram skip it
            mess = (
                "low memory, do not ask user for references (refCopy) "
                "for %s" % scanID
            )
            _logger.processSkipped(mess)
            return
        if (not self._gui.askForFlatUrl()) or (not self._gui.askForDarkUrl()):
            mes = "no reference created for %s, no link registred." % scanID
            _logger.processSkipped(mes)
        else:
            # process ref on this folder if only originals are here
            self.worker.set_process_only_dkRf(True)
            originalFolder = self.worker.directory
            self.worker.directory = self._gui.getCopyFolder()
            self.worker.process()
            self.worker.set_refs_from_scan(self.worker.directory)
            self.worker.directory = originalFolder

            if self.worker.has_flat_or_dark_stored() is True:
                self.worker.set_process_only_copy(True)
                self.worker.run()
            else:
                self._dealWithMissingRef(scanID)


class RefCopyWidget(qt.QGroupBox):
    """
    GUI for the :class:RefCopy
    """

    sigModeAutoChanged = qt.Signal()
    """Signal emitted when the mode auto change"""
    sigCopyActivationChanged = qt.Signal()
    """Signal emitted when the copy is activated or deactivated"""

    _DEFAULT_DIRECTORY = "/lbsram/data/visitor"
    """Default directory used when the user need to set path to references"""

    _MSG_NO_REF = "!!! No reference recorded !!!"

    def __init__(self, parent, save_dir: str, refCopy):
        """

        :param parent: Qt parent
        :param str save_dir: where the dark and flats 'references' are stored
        """
        qt.QGroupBox.__init__(self, "activate", parent)
        self.__save_dir = save_dir
        self._refCopy = refCopy
        self.setLayout(qt.QVBoxLayout())
        self.setCheckable(True)
        self._infoLabel = qt.QLabel(
            """
            The copy action happen after the reduced (computed) darks and flats. It can be activate or not. \n\n
            Reduced darks and / or flats can be registered and then copy to scan without darks or flat. \n
            You can set manually Darks and flat (button displayed when the mode auto is unchcked.) \n
            Otherwise if the mode 'auto' is activated then each time he meets scan with dark and / or flat it will register those as the one to be copied. \n

            Then each time the copy action meets scan without reduced dark and / or flat it will copy them. \n
            """,
            self,
        )
        self.layout().addWidget(self._infoLabel)
        self.layout().addWidget(self.__createManualGUI())
        self._qcbAutoMode = qt.QCheckBox("auto", parent=self)
        self.layout().addWidget(self._qcbAutoMode)
        spacer = qt.QWidget(self)
        spacer.setSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Expanding)
        self.layout().addWidget(spacer)
        self.layout().addWidget(self.__createStatusBarGUI())

        self.setModeAuto(True)
        self._qcbAutoMode.toggled.connect(self._updateModeAuto)

        # expose API
        self.sigActivated = self.toggled

        # connect signal / slot
        self.toggled.connect(self._triggerCopyActivated)
        self._qcbAutoMode.toggled.connect(self._triggerModeAutoChanged)

    def _triggerCopyActivated(self, *args, **kwargs):
        self.sigCopyActivationChanged.emit()

    def _triggerModeAutoChanged(self, *args, **kwargs):
        self.sigModeAutoChanged.emit()

    def sizeHint(self):
        return qt.QSize(400, 200)

    def __createManualGUI(self):
        self._manualSelectionWidget = qt.QWidget(self)
        self._manualSelectionWidget.setLayout(qt.QFormLayout())

        self._selectDarks = qt.QPushButton("select darks url", parent=self)
        self._manualSelectionWidget.layout().addRow(self._selectDarks)
        self._selectFlats = qt.QPushButton("select flats url", parent=self)
        self._manualSelectionWidget.layout().addRow(self._selectFlats)

        self._cacheFileLabel = qt.QLabel(
            DarkRefsCopy.get_save_file(self.__save_dir), self
        )
        self._manualSelectionWidget.layout().addRow(
            "current cache file is", self._cacheFileLabel
        )
        self._cacheFileLabel.setToolTip(
            "Dark-Flat copy mecanism store darks and flat at a specific location. If you want you can browse the file to see what are the dark and flat you will copy"
        )

        self._selectDarks.released.connect(self.askForDarksUrl)
        self._selectFlats.released.connect(self.askForFlatsUrl)

        return self._manualSelectionWidget

    def __createStatusBarGUI(self):
        self._statusBar = qt.QStatusBar(parent=self)
        self._statusBar.showMessage(self._MSG_NO_REF)
        return self._statusBar

    def _clearRef(self):
        shutil.rmtree(self.__save_dir)

    def askForFlatsUrl(self):
        dialog = DataFileDialog()
        dialog.setDirectory(get_default_directory())
        if dialog.exec_():
            url = dialog.selectedUrl()
            try:
                url = DataUrl(path=url)
            except Exception as e:
                _logger.error(f"Fails to define flat url. Error is {e}")
                return False

        if dialog.exec_():
            DarkRefsCopy.save_flats_to_be_copied(self.__save_dir, data=url)
            return True
        return False

    def askForDarksUrl(self):
        dialog = DataFileDialog()
        dialog.setDirectory(get_default_directory())
        if dialog.exec_():
            url = dialog.selectedUrl()
            try:
                url = DataUrl(path=url)
            except Exception as e:
                _logger.error(f"Fails to define flat url. Error is {e}")
                return False

        if dialog.exec_():
            DarkRefsCopy.save_darks_to_be_copied(self.__save_dir, data=url)
            return True
        return False

    def setModeAuto(self, b):
        self._refCopy.set_mode_auto(b)
        self._manualSelectionWidget.setVisible(not b)
        self._qcbAutoMode.setChecked(b)

    def is_on_mode_auto(self):
        return self._qcbAutoMode.isChecked()

    def _updateModeAuto(self):
        """call back of `_qcbGiveManually`"""
        self._refCopy.set_mode_auto(self._qcbAutoMode.isChecked())
        self._manualSelectionWidget.setVisible(not self._qcbAutoMode.isChecked())

    def copyActivated(self):
        """

        :return bool: Return True if the user want to aply the dark ref copy
        """
        return self.isChecked()

    def save_darks_to_be_copied(self, darks: Union[DataUrl, dict]):
        DarkRefsCopy.save_darks_to_be_copied(data=darks, save_dir=self.__save_dir)

    def save_flats_to_be_copied(self, flats: Union[DataUrl, dict]):
        DarkRefsCopy.save_flats_to_be_copied(data=flats, save_dir=self.__save_dir)
