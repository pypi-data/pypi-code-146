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
__date__ = "05/08/2020"


from silx.gui import qt
from tomoscan.volumebase import VolumeBase
from tomoscan.identifier import VolumeIdentifier
from tomoscan.esrf.volume.hdf5volume import HDF5Volume
from tomoscan.factory import Factory
from silx.gui.data.DataViewerFrame import DataViewerFrame
from silx.gui.dialog.ColormapDialog import ColormapDialog
from silx.gui.data.DataViews import DataViewHooks
from silx.gui.data.DataViews import IMAGE_MODE
import os
from tomwer.core.scan.scanbase import TomwerScanBase
import logging
from tomwer.core.utils.ftseriesutils import get_vol_file_shape
import weakref
from tomwer.gui.visualization.reconstructionparameters import ReconstructionParameters
import silx
from silx.gui.colors import Colormap
import numpy
import numpy.lib.npyio

_logger = logging.getLogger(__name__)


class _ScanInfo(qt.QWidget):
    """Display information about the reconstruction currently displayed"""

    def __init__(self, parent=None):
        qt.QWidget.__init__(self, parent)
        self.setLayout(qt.QFormLayout())
        self._scanQLE = qt.QLineEdit("", self)
        self._scanQLE.setReadOnly(True)
        self.layout().addRow("scan", self._scanQLE)

        self._volumeQLE = qt.QLineEdit("", self)
        self._volumeQLE.setReadOnly(True)
        self.layout().addRow("volume", self._volumeQLE)

    def setScan(self, scan):
        if scan is None:
            self._scanQLE.setText("")
            self._volumeQLE.setText("")
        else:
            assert isinstance(scan, TomwerScanBase)
            self._scanQLE.setText(str(scan))
            if len(scan.latest_vol_reconstructions) == 0:
                self._volumeQLE.setText("")
            else:
                self._volumeQLE.setText(str(scan.latest_vol_reconstructions[0]))

    def clear(self):
        self.setScan(None)


class _TomoApplicationContext(DataViewHooks):
    """
    Store the context of the application

    It overwrites the DataViewHooks to custom the use of the DataViewer for
    the silx view application.

    - Create a single colormap shared with all the views
    - Create a single colormap dialog shared with all the views
    """

    def __init__(self, parent, settings=None):
        self.__parent = weakref.ref(parent)
        self.__defaultColormap = Colormap(name="gray")
        self.__defaultColormapDialog = None
        self.__settings = settings
        self.__recentFiles = []

    def getSettings(self):
        """Returns actual application settings.

        :rtype: qt.QSettings
        """
        return self.__settings

    def restoreLibrarySettings(self):
        """Restore the library settings, which must be done early"""
        settings = self.__settings
        if settings is None:
            return
        settings.beginGroup("library")
        plotBackend = settings.value("plot.backend", "")
        plotImageYAxisOrientation = settings.value("plot-image.y-axis-orientation", "")
        settings.endGroup()

        if plotBackend != "":
            silx.config.DEFAULT_PLOT_BACKEND = plotBackend
        if plotImageYAxisOrientation != "":
            silx.config.DEFAULT_PLOT_IMAGE_Y_AXIS_ORIENTATION = (
                plotImageYAxisOrientation
            )

    def restoreSettings(self):
        """Restore the settings of all the application"""
        settings = self.__settings
        if settings is None:
            return
        parent = self.__parent()
        parent.restoreSettings(settings)

        settings.beginGroup("colormap")
        byteArray = settings.value("default", None)
        if byteArray is not None:
            try:
                colormap = Colormap()
                colormap.restoreState(byteArray)
                self.__defaultColormap = colormap
            except Exception:
                _logger.debug("Backtrace", exc_info=True)
        settings.endGroup()

        self.__recentFiles = []
        settings.beginGroup("recent-files")
        for index in range(1, 10 + 1):
            if not settings.contains("path%d" % index):
                break
            filePath = settings.value("path%d" % index)
            self.__recentFiles.append(filePath)
        settings.endGroup()

    def saveSettings(self):
        """Save the settings of all the application"""
        settings = self.__settings
        if settings is None:
            return
        parent = self.__parent()
        parent.saveSettings(settings)

        if self.__defaultColormap is not None:
            settings.beginGroup("colormap")
            settings.setValue("default", self.__defaultColormap.saveState())
            settings.endGroup()

        settings.beginGroup("library")
        settings.setValue("plot.backend", silx.config.DEFAULT_PLOT_BACKEND)
        settings.setValue(
            "plot-image.y-axis-orientation",
            silx.config.DEFAULT_PLOT_IMAGE_Y_AXIS_ORIENTATION,
        )
        settings.endGroup()

        settings.beginGroup("recent-files")
        for index in range(0, 11):
            key = "path%d" % (index + 1)
            if index < len(self.__recentFiles):
                filePath = self.__recentFiles[index]
                settings.setValue(key, filePath)
            else:
                settings.remove(key)
        settings.endGroup()

    def getRecentFiles(self):
        """Returns the list of recently opened files.

        The list is limited to the last 10 entries. The newest file path is
        in first.

        :rtype: List[str]
        """
        return self.__recentFiles

    def pushRecentFile(self, filePath):
        """Push a new recent file to the list.

        If the file is duplicated in the list, all duplications are removed
        before inserting the new filePath.

        If the list becan bigger than 10 items, oldest paths are removed.

        :param filePath: File path to push
        """
        # Remove old occurencies
        self.__recentFiles[:] = (f for f in self.__recentFiles if f != filePath)
        self.__recentFiles.insert(0, filePath)
        while len(self.__recentFiles) > 10:
            self.__recentFiles.pop()

    def clearRencentFiles(self):
        """Clear the history of the rencent files."""
        self.__recentFiles[:] = []

    def getColormap(self, view):
        """Returns a default colormap.

        Override from DataViewHooks

        :rtype: Colormap
        """
        if self.__defaultColormap is None:
            self.__defaultColormap = Colormap(name="viridis")
        return self.__defaultColormap

    def getColormapDialog(self, view):
        """Returns a shared color dialog as default for all the views.

        Override from DataViewHooks

        :rtype: ColorDialog
        """
        if self.__defaultColormapDialog is None:
            parent = self.__parent()
            if parent is None:
                return None
            dialog = ColormapDialog(parent=parent)
            dialog.setModal(False)
            self.__defaultColormapDialog = dialog
        return self.__defaultColormapDialog


class VolumeViewer(qt.QMainWindow):
    def __init__(self, parent):
        qt.QMainWindow.__init__(self, parent)
        self._centralWidget = DataViewerFrame(parent=self)
        self.__context = _TomoApplicationContext(self)
        self._centralWidget.setGlobalHooks(self.__context)
        self._centralWidget.setSizePolicy(
            qt.QSizePolicy.Expanding, qt.QSizePolicy.Expanding
        )
        self.setCentralWidget(self._centralWidget)
        self._infoWidget = _ScanInfo(parent=self)

        # top level dock widget to display information regarding the scan
        # and volume
        self._dockInfoWidget = qt.QDockWidget(parent=self)
        self._dockInfoWidget.layout().setContentsMargins(0, 0, 0, 0)
        self._dockInfoWidget.setFeatures(qt.QDockWidget.DockWidgetMovable)
        self._dockInfoWidget.setWidget(self._infoWidget)
        self.addDockWidget(qt.Qt.TopDockWidgetArea, self._dockInfoWidget)

        # add dock widget for reconstruction parameters
        self._reconsInfoDockWidget = qt.QDockWidget(parent=self)
        self._reconsWidgetScrollArea = qt.QScrollArea(self)
        self._reconsWidgetScrollArea.setWidgetResizable(True)
        self._reconsWidget = ReconstructionParameters(self)
        self._reconsWidgetScrollArea.setWidget(self._reconsWidget)
        self._reconsInfoDockWidget.setWidget(self._reconsWidgetScrollArea)
        self._reconsInfoDockWidget.setFeatures(qt.QDockWidget.DockWidgetMovable)
        self.addDockWidget(qt.Qt.RightDockWidgetArea, self._reconsInfoDockWidget)

        self._h5_file = None
        """pointer to the hdf5 file since we want to set the HDF5Dataset for
        loading data on the fly and avoid loading everything into memory for
        hdf5."""
        self.__first_load = True
        self.__last_mode = None

    def _close_h5_file(self):
        if self._h5_file is not None:
            self._h5_file.close()
        self._h5_file = None

    def close(self):
        self._close_h5_file()
        super().close()

    def setScan(self, scan):
        self.clear()
        if scan is None:
            return

        elif len(scan.latest_vol_reconstructions) == 0:
            _logger.warning("No reconstructed volume for {}".format(scan))
            self.clear()
            self._infoWidget.setScan(scan)
        else:
            self._set_volumes(volumes=scan.latest_vol_reconstructions)
            self._infoWidget.setScan(scan)

    def setVolume(self, volume):
        self.clear()
        if volume is None:
            return
        self._set_volumes(volumes=(volume,))
        # TODO in the future: do the equivalent of setScan from the volume metadata

    def _get_data_volume(self, volume: VolumeBase):
        if not isinstance(volume, VolumeBase):
            raise TypeError(
                f"volume is expected to be an instance of {VolumeBase}. Not {type(volume)}"
            )

        if not isinstance(volume, HDF5Volume):
            _logger.warning(
                "Attempt to set a non HDF5 volume to the viewer. This requires to load all the data in memory. This can take a while"
            )
        data = volume.data if volume.data is not None else volume.load_data()
        return data

    def _set_volumes(self, volumes: tuple):
        self.clear()
        # for now handle a single volume
        if len(volumes) == 0:
            pass
        else:
            if len(volumes) > 1:
                _logger.warning(
                    "Only one volume can be displayed. Will display the first one"
                )
            volume = volumes[0]
            if isinstance(volume, (str, VolumeIdentifier)):
                volume = Factory.create_tomo_object_from_identifier(volume)
            elif isinstance(volume, VolumeBase):
                pass
            else:
                raise TypeError(
                    "Volume should be an instance of a Volume, a VolumeIdentifier or a string refering to a VolumeIdentifier"
                )

            data = self._get_data_volume(volume)
            # set volume dataset
            if data is not None:
                self._set_volume(data)
            # set reconstruction parameters
            try:
                self._reconsWidget.setUrl(volume.data_url)
            except Exception as e:
                _logger.info(
                    f"Unable to set reconstruction parameters from {volume.data_url}. Not handled for pyhst reconstructions. Error is {e}"
                )

    def _set_volume(self, volume: numpy.ndarray):
        self._centralWidget.setData(volume)
        if self.__first_load:
            self._centralWidget.setDisplayMode(IMAGE_MODE)
            self.__first_load = False
        elif self.__last_mode is not None:
            self._centralWidget.setDisplayMode(self.__last_mode)

    def clear(self):
        self.__last_mode = self._centralWidget.displayMode()
        self._close_h5_file()
        # self._centralWidget.setData(None)
        self._infoWidget.clear()

    def sizeHint(self):
        return qt.QSize(600, 600)

    # TODO: should be merged with dataviewer._load_vol function ?
    def _load_vol(self, url):
        """
        load a .vol file
        """
        if url.file_path().lower().endswith(".vol.info"):
            info_file = url.file_path()
            raw_file = url.file_path().replace(".vol.info", ".vol")
        else:
            assert url.file_path().lower().endswith(".vol")
            raw_file = url.file_path()
            info_file = url.file_path().replace(".vol", ".vol.info")

        if not os.path.exists(raw_file):
            data = None
            mess = f"Can't find raw data file {raw_file} associated with {info_file}"
            _logger.warning(mess)
        elif not os.path.exists(info_file):
            mess = f"Can't find info file {info_file} associated with {raw_file}"
            _logger.warning(mess)
            data = None
        else:
            shape = get_vol_file_shape(info_file)
            if None in shape:
                _logger.warning(f"Fail to retrieve data shape for {info_file}.")
                data = None
            else:
                try:
                    numpy.zeros(shape)
                except MemoryError:
                    data = None
                    _logger.warning(f"Raw file {raw_file} is too large for being read")
                else:
                    data = numpy.fromfile(
                        raw_file, dtype=numpy.float32, count=-1, sep=""
                    )
                    try:
                        data = data.reshape(shape)
                    except ValueError:
                        _logger.warning(
                            f"unable to fix shape for raw file {raw_file}. "
                            "Look for information in {info_file}"
                        )
                        try:
                            sqr = int(numpy.sqrt(len(data)))
                            shape = (1, sqr, sqr)
                            data = data.reshape(shape)
                        except ValueError:
                            _logger.info(
                                f"deduction of shape size for {raw_file} " "failed"
                            )
                            data = None
                        else:
                            _logger.warning(
                                f"try deducing shape size for {raw_file} "
                                "might be an incorrect interpretation"
                            )
        if url.data_slice() is None:
            return data
        else:
            return data[url.data_slice()]
