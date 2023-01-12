# /*##########################################################################
# Copyright (C) 2016-2017 European Synchrotron Radiation Facility
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

__author__ = ["H. Payno"]
__license__ = "MIT"
__date__ = "11/07/2022"

from silx.gui import qt
from tomoscan.volumebase import VolumeBase
from tomwer.core.volume import (
    EDFVolume,
    HDF5Volume,
    TIFFVolume,
    MultiTIFFVolume,
    JP2KVolume,
    RawVolume,
)
from tomwer.core.volume.volumefactory import VolumeFactory as Factory
from silx.gui.dialog.DataFileDialog import DataFileDialog
from tomoscan.esrf.volume.utils import (
    guess_volumes as tomoscan_guess_volumes,
    get_most_common_extension as get_most_common_extension,
)
from silx.gui.utils import blockSignals
from silx.io.url import DataUrl
import logging
import h5py
import os

_logger = logging.getLogger()


class QDataDialog(qt.QFileDialog):
    """docstring for QFolderDialog"""

    def __init__(self, parent, multiSelection=False):
        qt.QFileDialog.__init__(self, parent)
        self.setNameFilters(
            [
                "HDF5 files (*.h5 *.hdf5 *.nx *.nxs *.nexus)",
                "Nexus files (*.nx *.nxs *.nexus)",
                "Any files (*)",
            ]
        )
        self._selected_files = []
        self.setFileMode(qt.QFileDialog.ExistingFiles)

        # self.QDialogButtonBox
        self.multiSelection = multiSelection
        # check if old data directory exists
        idir = False
        f_cd_last = os.environ["HOME"] + "/.octave/mylastpwd.txt"
        if os.path.isfile(f_cd_last) is True:
            with open(f_cd_last, "r") as fcdl:
                d_cd_last = fcdl.readlines()
                d_cd_last = d_cd_last[0][0 : d_cd_last[0].rfind("/")]
                idir = os.path.isdir(d_cd_last)

        if os.environ.get("TOMWER_DEFAULT_INPUT_DIR", None) and os.path.exists(
            os.environ["TOMWER_DEFAULT_INPUT_DIR"]
        ):
            self.setDirectory(os.environ["TOMWER_DEFAULT_INPUT_DIR"])
        elif idir is True:
            self.setDirectory(d_cd_last)
        elif os.path.isdir("/data"):
            self.setDirectory("/data")

        btns = self.findChildren(qt.QPushButton)
        if len(btns) == 0:
            _logger.error(
                "Cannot retrieve open button. switch to none " "native QFileDialog"
            )
            self.setOption(qt.QFileDialog.DontUseNativeDialog)
            btns = self.findChildren(qt.QPushButton)

        if self.multiSelection is True:
            # to make it possible to select multiple directories:
            self.file_view = self.findChild(qt.QListView, "listView")
            if self.file_view:
                self.file_view.setSelectionMode(qt.QAbstractItemView.MultiSelection)
                self.file_view.setSelectionMode(qt.QAbstractItemView.ExtendedSelection)

            self.f_tree_view = self.findChild(qt.QTreeView)
            if self.f_tree_view:
                self.f_tree_view.setSelectionMode(qt.QAbstractItemView.MultiSelection)
                self.f_tree_view.setSelectionMode(
                    qt.QAbstractItemView.ExtendedSelection
                )

            if len(btns) > 0:
                self.openBtn = [x for x in btns if "open" in str(x.text()).lower()][0]
                self.openBtn.clicked.disconnect()
                self.openBtn.hide()
                parent = self.openBtn.parent()
                self.openBtn = qt.QPushButton("Select", parent=parent)
                self.openBtn.clicked.connect(self.openClicked)
                parent.layout().insertWidget(0, self.openBtn)

    def openClicked(self):
        inds = self.f_tree_view.selectionModel().selectedIndexes()
        for i in inds:
            if i.column() == 0:
                self._selected_files.append(
                    os.path.join(str(self.directory().absolutePath()), str(i.data()))
                )
        self.accept()
        self.done(1)

    def files_selected(self):
        for file_ in self.selectedFiles():
            self._selected_files.append(file_)
        return self._selected_files


class QVolumeDialog(qt.QDialog):
    """
    dialog to selecct / define a volume
    """

    _EDF_EXTENSIONS = ("edf",)
    _TIFF_EXTENSIONS = (
        "tiff",
        "tif",
    )
    _JP2K_EXTENSIONS = (
        "jp2",
        "jp2k",
    )
    _HDF5_EXTENSIONS = ("hdf", "hdf5", "h5", "nx", "nexus")
    _RAW_EXTENSIONS = (
        "vol",
        "raw",
    )

    _VOLUME_TO_EXT = {
        EDFVolume: "edf",
        HDF5Volume: "hdf5",
        TIFFVolume: "tiff",
        MultiTIFFVolume: "tiff",
        JP2KVolume: "jp2",
        RawVolume: "vol",
    }

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setLayout(qt.QGridLayout())

        # add volume url
        self.layout().addWidget(qt.QLabel("volume url", parent=self), 0, 0, 1, 1)
        self._volumeUrlQL = qt.QLineEdit(parent=self)
        self._volumeUrlQL.setPlaceholderText("scheme:obj_type:path?queries")
        self._volumeUrlQL.setToolTip(
            "volume url defining the volume. Will be automatically updated from the other widgets"
        )
        self.layout().addWidget(self._volumeUrlQL, 0, 1, 1, 3)
        # add file path
        self.layout().addWidget(
            qt.QLabel("file or folder path", parent=self), 1, 0, 1, 1
        )
        self._filePathQL = qt.QLineEdit(parent=self)
        self._filePathQL.setToolTip(
            "File path (for hdf5 and multi-tiff) or folder path (for edf, jp2k, tiff...)"
        )
        self.layout().addWidget(self._filePathQL, 1, 1, 1, 2)
        self._selectPathPB = qt.QPushButton("select", self)
        self.layout().addWidget(self._selectPathPB, 1, 3, 1, 1)

        # data path
        self.layout().addWidget(
            qt.QLabel("data path", parent=self),
            3,
            0,
            1,
            1,
        )
        self._dataPathQL = qt.QLineEdit(parent=self)
        self._dataPathQL.setToolTip("data path for hdf5 file")
        self.layout().addWidget(self._dataPathQL, 3, 1, 1, 1)
        self._guessDataPathAuto = qt.QCheckBox("guess auto")
        self.layout().addWidget(self._guessDataPathAuto, 3, 2, 1, 1)
        self._guessDataPathAuto.setToolTip(
            "If checked will try to guess automatically data path from given hdf5 file"
        )
        self._selectDataPathPB = qt.QPushButton("select", self)
        self.layout().addWidget(self._selectDataPathPB, 3, 3, 1, 1)

        # basename
        self.layout().addWidget(
            qt.QLabel("basename", parent=self),
            4,
            0,
            1,
            1,
        )
        self._basenameQL = qt.QLineEdit(parent=self)
        self._basenameQL.setToolTip(
            "volume basename. Used for edf, tiff and jp2k volumes"
        )
        self.layout().addWidget(self._basenameQL, 4, 1, 1, 1)
        self._guessBasenameAuto = qt.QCheckBox("guess auto")
        self.layout().addWidget(self._guessBasenameAuto, 4, 2, 1, 1)
        self._guessBasenameAuto.setToolTip(
            "If checked will try to guess automatically basename from given folder"
        )
        # file extension
        self.layout().addWidget(
            qt.QLabel("extension", parent=self),
            5,
            0,
            1,
            1,
        )
        self._extensionQL = qt.QLineEdit(parent=self)
        self._extensionQL.setToolTip("file extension")
        self.layout().addWidget(self._extensionQL, 5, 1, 1, 1)
        self._guessExtensionAuto = qt.QCheckBox("guess auto")
        self.layout().addWidget(self._guessExtensionAuto, 5, 2, 1, 1)
        self._guessExtensionAuto.setToolTip(
            "If checked will try to guess automatically basename from given folder"
        )

        examples_text = """
        --- extra informations. ---

        This dialog has been though to be work with "automatic guess" active. It should work if you didn't used
        any 'fancy' volumes definition. In this case providing the file path of folder path should be enought.
        Regarding the 'fancy' definition be aware that: \n

           - for an hdf5 file: expects hdf5 file path and a data_path. \n
           - for multitiff file: expects the file path only \n
           - for 'folder' volumes (edf, tiff and jp2k): expects folder, basename (default is the folder name) \n
        """
        self._examplesQLE = qt.QTextEdit(self)
        self._examplesQLE.setText(examples_text)
        self._examplesQLE.setReadOnly(True)
        self.layout().addWidget(self._examplesQLE, 99, 0, 4, 4)

        # buttons for validation
        self._buttons = qt.QDialogButtonBox(self)
        types = qt.QDialogButtonBox.Ok | qt.QDialogButtonBox.Cancel
        self._buttons.setStandardButtons(types)

        self.layout().addWidget(self._buttons, 200, 0, 1, 4)

        # connect signal / slot
        self._buttons.button(qt.QDialogButtonBox.Ok).clicked.connect(self.accept)
        self._buttons.button(qt.QDialogButtonBox.Cancel).clicked.connect(self.reject)
        self._guessBasenameAuto.toggled.connect(self._basenameQL.setDisabled)
        self._guessDataPathAuto.toggled.connect(self._dataPathQL.setDisabled)
        self._guessExtensionAuto.toggled.connect(self._extensionQL.setDisabled)
        self._volumeUrlQL.textChanged.connect(self._volumeUrlChanged)
        self._filePathQL.textChanged.connect(self._filePathChanged)
        self._dataPathQL.textChanged.connect(self._dataChanged)
        self._basenameQL.textChanged.connect(self._basenameChanged)
        self._extensionQL.textChanged.connect(self._extensionChanged)
        self._selectPathPB.released.connect(self._selectFileOrFolder)
        self._selectDataPathPB.released.connect(self._selectDataPath)

        # set up - by default try to guess most of it automatically
        self._guessBasenameAuto.setChecked(True)
        self._guessDataPathAuto.setChecked(True)
        self._guessExtensionAuto.setChecked(True)

    def _selectFileOrFolder(self):
        dialog = QDataDialog(self, multiSelection=True)
        dialog.setNameFilters(
            [
                "Any files (*)",
                "HDF5 files (*.h5 *.hdf5 *.hdf *.nx *.nxs *.nexus)",
                "Nexus files (*.nx *.nxs *.nexus)",
                "multitiff files (*.tiff *.tif)",
                "raw files (*.vol *.raw)",
            ]
        )
        if dialog.exec_() == qt.QDialog.Accepted:
            selected_files = dialog.selectedFiles()
            if len(selected_files) > 0:
                self.setFilePath(selected_files[0])

    def _selectDataPath(self):
        self._guessDataPathAuto.setChecked(False)
        file_path = self.getFilePath()
        if file_path in (None, "") or not h5py.is_hdf5(file_path):
            _logger.warning(
                f"{file_path} is not an hdf5 file. can't browse it to define a data path"
            )
            return
        dialog = DataFileDialog(self)
        dialog.selectFile(file_path)

        if dialog.exec_():
            try:
                url = dialog.selectedUrl()
                url = DataUrl(path=url)
                if url is not None:
                    if url.file_path() != self.getFilePath():
                        # in case user get data path from another file update it too
                        with blockSignals(self._filePathQL):
                            self.setFilePath(url.file_path())
                        with blockSignals(self._dataPathQL):
                            self.setDataPath(url.data_path())
                    self._updateVolume_url()
            except Exception as e:
                _logger.error(e)

    def _volumeUrlChanged(self):
        url = self._volumeUrlQL.text()
        try:
            volume = Factory.create_tomo_object_from_identifier(url)
        except Exception as e:
            _logger.info(f"fail to create a volume from {url}. Error is {e}")
        else:
            try:
                if isinstance(volume, HDF5Volume):
                    data_path = volume.url.data_path()
                    file_path = volume.file_path
                    volume_basename = ""
                    volume_extension = os.path.splitext(volume.file_path)[-1].lstrip(
                        "."
                    )
                    # handle case no file path provided but only the extension
                    if volume_extension == "":
                        volume_extension = None
                elif isinstance(volume, MultiTIFFVolume):
                    data_path = ""
                    file_path = volume.file_path
                    volume_basename = ""
                    if volume.file_path is not None:
                        volume_extension = os.path.splitext(volume.file_path)[
                            -1
                        ].lstrip(".")
                    else:
                        volume_extension = None
                elif isinstance(volume, (EDFVolume, TIFFVolume, JP2KVolume)):
                    data_path = ""
                    file_path = volume.url.file_path()
                    volume_basename = volume.get_volume_basename()
                    volume_extension = volume.data_extension
                elif isinstance(volume, RawVolume):
                    data_path = ""
                    file_path = volume.url.file_path()
                    volume_basename = ""
                    volume_extension = os.path.splitext(volume.file_path)[-1].lstrip(
                        "."
                    )
                else:
                    raise TypeError(f"volume type {type(volume)} is not handled")
            except (AttributeError, ValueError) as e:
                _logger.error(
                    f"fail to update volume interface from url {url}. Error is {e}"
                )

            if volume_extension is not None:
                with blockSignals(self._extensionQL):
                    self.setDataExtension(volume_extension)
                assert url == self._volumeUrlQL.text()

            with blockSignals(self._filePathQL):
                self.setFilePath(file_path)
                assert url == self._volumeUrlQL.text()
            with blockSignals(self._dataPathQL):
                self.setDataPath(data_path)
                assert url == self._volumeUrlQL.text()

            with blockSignals(self._basenameQL):
                self.setVolumeBasename(volume_basename)
                assert url == self._volumeUrlQL.text()

    def _updateVolume_url(self, *args, **kwargs):
        volume = self.getVolume()
        if volume is None:
            return
        else:
            identifier = volume.get_identifier().to_str()
            with blockSignals(self._volumeUrlQL):
                self._volumeUrlQL.setText(identifier)

    def _filePathChanged(self, *args, **kwargs):
        # TODO: move VolumeList.DEFAULT_SCHEME_TO_VOL to a dedicated location
        from tomwer.gui.control.datalist import VolumeList  # avoid import cycle

        guess_basename = self._guessBasenameAuto.isChecked()
        guess_data_path = self._guessDataPathAuto.isChecked()
        guess_extension = self._guessExtensionAuto.isChecked()

        file_path = self.getFilePath()
        try_guess_volume = (
            guess_basename or guess_data_path or guess_extension
        ) and os.path.exists(file_path)
        if try_guess_volume:
            guessed_volumes = tomoscan_guess_volumes(
                file_path, scheme_to_vol=VolumeList.DEFAULT_SCHEME_TO_VOL
            )
            if guessed_volumes is None or len(guessed_volumes) == 0:
                data_path = ""
                data_extension = ""
                basename = ""
            else:
                first_vol = guessed_volumes[0]
                if len(guessed_volumes) > 1:
                    _logger.warning(
                        f"More than one volume found in {file_path}. Will only take the first one."
                    )
                if isinstance(first_vol, HDF5Volume):
                    data_path = first_vol.url.data_path()
                else:
                    data_path = ""

                if os.path.isfile(file_path):
                    _, data_extension = os.path.splitext(file_path)
                    if data_extension == "":
                        # in the folder use case provide a valid extension
                        data_extension = self._VOLUME_TO_EXT[type(first_vol)]
                    else:
                        data_extension = data_extension.lstrip(".")
                else:
                    data_extension = get_most_common_extension(file_path) or ""

                if isinstance(first_vol, (HDF5Volume, MultiTIFFVolume, RawVolume)):
                    basename = ""
                elif isinstance(first_vol, (EDFVolume, TIFFVolume, JP2KVolume)):
                    basename = os.path.basename(first_vol.get_volume_basename())
                else:
                    raise NotImplementedError
            if guess_extension:
                with blockSignals(self._extensionQL):
                    self._extensionQL.setText(data_extension)
            if guess_basename:
                with blockSignals(self._basenameQL):
                    self._basenameQL.setText(basename)
            if guess_data_path:
                with blockSignals(self._dataPathQL):
                    self._dataPathQL.setText(data_path)
            self._updateVolume_url()

    def _dataChanged(self, *args, **kwargs):
        self._updateVolume_url()

    def _basenameChanged(self, *args, **kwargs):
        self._updateVolume_url()

    def _extensionChanged(self, *args, **kwargs):
        self._updateVolume_url()

    def setFullAuto(self, auto: bool):
        for widget in (
            self._guessBasenameAuto,
            self._guessDataPathAuto,
            self._guessExtensionAuto,
        ):
            widget.setChecked(auto)

    def getFilePath(self):
        return self._filePathQL.text()

    def setFilePath(self, text):
        self._filePathQL.setText(text)

    def getDataPath(self):
        return self._dataPathQL.text()

    def setDataPath(self, text):
        self._dataPathQL.setText(text)

    def getVolumeBasename(self):
        return self._basenameQL.text()

    def setVolumeBasename(self, text: str):
        self._basenameQL.setText(text)

    def getDataExtension(self):
        return self._extensionQL.text()

    def setDataExtension(self, text):
        self._extensionQL.setText(text)

    def setVolumeUrl(self, text: str):
        self._volumeUrlQL.setText(text)

    def getVolume(self) -> VolumeBase:
        """
        Return possible volume from current information.
        this function is also used to determine the volume url

        :warning: the return volume might not exists (at all).
        """
        data_path = self._dataPathQL.text()
        file_path = self._filePathQL.text()
        basename = self._basenameQL.text()
        file_extension = self._extensionQL.text().lower().lstrip(".")

        single_frame_extensions = (
            list(self._EDF_EXTENSIONS)
            + list(self._TIFF_EXTENSIONS)
            + list(self._JP2K_EXTENSIONS)
        )
        if file_extension in self._TIFF_EXTENSIONS and os.path.isfile(file_path):
            for name, var in {"basename": basename, "data path": data_path}.items():
                if var not in ("", None):
                    _logger.warning(
                        f"{name} provided but not used for {MultiTIFFVolume}. Will be ignored"
                    )
            return MultiTIFFVolume(file_path=file_path)

        if file_extension in single_frame_extensions:
            if file_extension in self._EDF_EXTENSIONS:
                constructor = EDFVolume
            elif file_extension in self._TIFF_EXTENSIONS:
                constructor = TIFFVolume
            elif file_extension in self._JP2K_EXTENSIONS:
                constructor = JP2KVolume
            volume = constructor(
                folder=file_path,
                volume_basename=None if basename in ("", None) else basename,
                data_extension=self._extensionQL.text().lstrip("."),
            )
            if data_path not in (None, ""):
                _logger.warning(
                    f"{constructor} are not handling 'data path'. This information will be ignored"
                )
            return volume
        elif file_extension in self._HDF5_EXTENSIONS:
            if basename not in ("", None):
                _logger.warning(
                    f"basename provided but not used for {HDF5Volume}. Will be ignored"
                )
            return HDF5Volume(
                file_path=file_path,
                data_path=data_path,
            )
        elif file_extension in self._RAW_EXTENSIONS:
            return RawVolume(file_path=file_path)
        elif file_extension in (None, ""):
            return None
