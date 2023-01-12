# coding: utf-8
# /*##########################################################################
# Copyright (C) 2016 European Synchrotron Radiation Facility
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

__authors__ = ["H. Payno"]
__license__ = "MIT"
__date__ = "22/01/2017"


import os
from tomwer.test.utils import skip_gui_test
from silx.gui import qt
from silx.gui.utils.testutils import TestCaseQt
from tomwer.gui.control.volumeselectorwidget import VolumeSelectorWidget
from tomwer.core.volume import EDFVolume, HDF5Volume
import numpy
import shutil
import tempfile
import pytest


@pytest.mark.skipif(skip_gui_test(), reason="skip gui test")
class TestVolumeSelector(TestCaseQt):
    """
    Simple test for the VolumeSelector
    """

    def setUp(self):
        super().setUp()
        self.folder = tempfile.mkdtemp()

        self.volume_1 = HDF5Volume(
            file_path=os.path.join(self.folder, "my_volume.hdf5"),
            data_path="entry0000",
            data=numpy.linspace(1, 100, 300).reshape(3, 10, 10),
        )
        self.volume_1.save()

        self.volume_2 = HDF5Volume(
            file_path=os.path.join(self.folder, "my_volume.hdf5"),
            data_path="entry0001",
            data=numpy.linspace(1, 100, 400).reshape(4, 10, 10),
        )
        self.volume_2.save()

        self.volume_3 = EDFVolume(
            folder=os.path.join(self.folder, "vol"),
            data=numpy.linspace(1, 100, 500).reshape(5, 10, 10),
        )
        self.volume_3.save()

        self.widget = VolumeSelectorWidget(parent=None)

    def tearDown(self):
        self.widget.setAttribute(qt.Qt.WA_DeleteOnClose)
        self.widget.close()
        self.widget = None
        shutil.rmtree(self.folder)
        super().tearDown()

    def test(self):
        for volume in (self.volume_1, self.volume_2, self.volume_3):
            self.widget.add(volume)

        # self.widget.show()
        # self.qapp.exec_()
        self.assertEqual(self.widget.dataList.n_data(), 3)
        self.widget.remove(self.volume_2)
        self.assertEqual(self.widget.dataList.n_data(), 2)
        self.widget.remove(self.volume_3)
        self.assertEqual(self.widget.dataList.n_data(), 1)
        assert self.widget.dataList.rowCount() == 1
