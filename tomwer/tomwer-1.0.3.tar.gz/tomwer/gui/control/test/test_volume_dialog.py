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


import os
import shutil
import tempfile
from silx.gui.utils.testutils import TestCaseQt
from silx.gui import qt
from tomwer.test.utils import skip_gui_test
from tomwer.gui.qfolderdialog import QVolumeDialog
from tomoscan.esrf.volume.edfvolume import EDFVolume
from tomoscan.esrf.volume.hdf5volume import HDF5Volume
import numpy
import pytest


@pytest.mark.skipif(skip_gui_test(), reason="skip gui test")
class TestVolumeDialog(TestCaseQt):
    """Test QVolumeDialog"""

    def setUp(self):
        super().setUp()
        self.tmp_dir = tempfile.mkdtemp()
        self._dialog = QVolumeDialog()

    def tearDown(self):
        shutil.rmtree(self.tmp_dir)
        self._dialog.setAttribute(qt.Qt.WA_DeleteOnClose)
        self._dialog.close()
        self._dialog = None
        return super().tearDown()

    def test_provide_hdf5_volume_auto(self):
        """
        Test everything can be discovered from a single 'default' hdf5 file
        """
        self._dialog.setFullAuto(True)
        file_path = os.path.join(self.tmp_dir, "myvolume.nx")
        volume = HDF5Volume(
            file_path=file_path,
            data_path="entry",
            data=numpy.linspace(1, 10, 300, dtype=numpy.uint8).reshape(3, 10, 10),
        )
        volume.save()
        self._dialog.show()
        self._dialog.setFilePath(file_path)
        self.qapp.processEvents()
        assert self._dialog.getDataPath() in ("entry", "/entry")
        assert self._dialog.getDataExtension() == "nx"
        assert self._dialog.getVolumeBasename() in ("", None)
        volume_defined = self._dialog.getVolume()
        assert volume_defined is not None
        volume_defined.load()
        assert volume_defined.data is not None
        assert (
            self._dialog._volumeUrlQL.text() == volume_defined.get_identifier().to_str()
        )

    def test_provide_hdf5_volume_manual(self):
        """
        Test we can create a volume if everything is defined manually from hdf5 volume file
        """
        self._dialog.setFullAuto(False)
        file_path = os.path.join(self.tmp_dir, "myvolume.nx")
        volume = HDF5Volume(
            file_path=file_path,
            data_path="entry",
            data=numpy.linspace(1, 10, 300, dtype=numpy.uint8).reshape(3, 10, 10),
        )
        volume.save()

        self._dialog.setDataExtension("nx")
        assert self._dialog.getVolume() is not None
        self._dialog.setFilePath(file_path)
        self._dialog.setDataPath("entry")
        volume_defined = self._dialog.getVolume()
        volume_defined.load()
        assert volume_defined.data is not None
        assert (
            self._dialog._volumeUrlQL.text() == volume_defined.get_identifier().to_str()
        )

    def test_provide_edf_volume_auto(self):
        """
        Test everything can be discovered from a single 'default' edf volume folder
        """
        self._dialog.setFullAuto(True)
        volume = EDFVolume(
            folder=self.tmp_dir,
            data=numpy.linspace(1, 10, 300, dtype=numpy.uint8).reshape(3, 10, 10),
        )
        volume.save()
        self._dialog.show()

        self._dialog.setFilePath(self.tmp_dir)
        self.qapp.processEvents()
        assert self._dialog.getDataPath() in ("", None)
        assert self._dialog.getDataExtension() == "edf"
        assert self._dialog.getVolumeBasename() == os.path.basename(self.tmp_dir)
        volume_defined = self._dialog.getVolume()
        assert volume_defined is not None
        volume_defined.load()
        assert volume_defined.data is not None
        assert (
            self._dialog._volumeUrlQL.text() == volume_defined.get_identifier().to_str()
        )

    def test_provide_edf_volume_manual(self):
        """
        Test we can create a volume if everything is defined manually from edf volume folder
        """
        self._dialog.setFullAuto(False)
        volume = EDFVolume(
            folder=self.tmp_dir,
            data=numpy.linspace(1, 10, 300, dtype=numpy.uint8).reshape(3, 10, 10),
            volume_basename="test",
        )
        volume.save()
        self._dialog.show()

        self._dialog.setFilePath(self.tmp_dir)
        self.qapp.processEvents()
        self._dialog.setDataExtension(
            ".edf"
        )  # should be edf but test works also if user add the dot
        self._dialog.setVolumeBasename("test")
        volume_defined = self._dialog.getVolume()
        assert volume_defined is not None
        volume_defined.load()
        assert volume_defined.data is not None
        assert (
            self._dialog._volumeUrlQL.text() == volume_defined.get_identifier().to_str()
        )

    def test_provide_hdf5_volume_url(self):
        """
        Test we can create a volume if the url (of a hdf5 volume) is provided by the user
        """
        file_path = os.path.join(self.tmp_dir, "myvolume.hdf")
        volume = HDF5Volume(
            file_path=file_path,
            data_path="entry",
            data=numpy.linspace(1, 10, 300, dtype=numpy.uint8).reshape(3, 10, 10),
        )
        volume.save()
        self._dialog.setVolumeUrl(volume.get_identifier().to_str())
        volume_defined = self._dialog.getVolume()
        assert volume_defined is not None
        volume_defined.load()
        assert volume_defined.data is not None
        assert self._dialog.getDataPath() in ("entry", "/entry")
        assert self._dialog.getVolumeBasename() in ("", None)
        assert self._dialog.getFilePath() == file_path
        assert self._dialog.getDataExtension() == "hdf"

    def test_provide_edf_volume_url(self):
        """
        Test we can create a volume if the url (of a EDFVolume) is provided by the user
        """
        volume = EDFVolume(
            folder=self.tmp_dir,
            data=numpy.linspace(1, 10, 300, dtype=numpy.uint8).reshape(3, 10, 10),
            volume_basename="test",
        )
        volume.save()
        self._dialog.setVolumeUrl(volume.get_identifier().to_str())
        volume_defined = self._dialog.getVolume()
        assert volume_defined is not None
        volume_defined.load()
        assert volume_defined.data is not None
        assert self._dialog.getDataPath() in ("", None)
        assert self._dialog.getVolumeBasename() == "test"
        assert self._dialog.getFilePath() == self.tmp_dir
        assert self._dialog.getDataExtension() == "edf"
