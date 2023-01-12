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
__date__ = "16/06/2021"

import os
import shutil
import tempfile
import numpy
from tomwer.core.utils.scanutils import MockHDF5
from tomwer.gui.stacks import SliceStack, RadioStack
from silx.gui import qt
from silx.gui.utils.testutils import TestCaseQt
import logging
import time
import pytest
from tomoscan.esrf.volume.edfvolume import EDFVolume
from tomwer.test.utils import skip_gui_test
import weakref

logging.disable(logging.INFO)


@pytest.mark.skipif(skip_gui_test(), reason="skip gui test")
class TestSliceStack(TestCaseQt):
    """unit test for the :class:_ImageStack widget"""

    def setUp(self):
        super().setUp()
        self._widget = SliceStack()
        self._widget.setAttribute(qt.Qt.WA_DeleteOnClose)

    def tearDown(self):
        self._widget.close()
        self._widget = None
        self.qapp.processEvents()
        super().tearDown()

    def test_hdf5(self):
        self.assertEqual(len(self._widget._scans), 0)
        n_scan = 5
        n_slice_per_scan = 1
        with tempfile.TemporaryDirectory() as root_dir:
            for i_scan in range(n_scan):
                scan = MockHDF5(
                    scan_path=os.path.join(root_dir, f"scan{i_scan}"),
                    n_proj=10,
                    n_ini_proj=10,
                    scan_range=180,
                    dim=10,
                ).scan
                volume = EDFVolume(
                    folder=os.path.join(scan.path, "edf_volume"),
                    data=numpy.random.random(10 * 10 * n_slice_per_scan).reshape(
                        n_slice_per_scan, 10, 10
                    ),
                )
                volume.save()
                scan.set_latest_reconstructions((volume,))
                assert len(scan.latest_reconstructions) == 1
                self._widget.addLeafScan(scan)
        self.assertEqual(len(self._widget._scans), n_scan)
        self.assertEqual(len(self._widget.extractImages()), n_scan * n_slice_per_scan)


@pytest.mark.skipif(skip_gui_test(), reason="skip gui test")
class TestRadioStack(TestCaseQt):
    """
    Test for the RadioStack
    The main part of test on mode is done on silx side, test of silx.gui.plot.ImageStack
    """

    def setUp(self):
        super().setUp()
        self._widget = RadioStack()
        self._widget.setAttribute(qt.Qt.WA_DeleteOnClose)
        self.spinBox = weakref.ref(self._widget._viewer._qspinbox)
        self.slider = weakref.ref(self._widget._viewer._qslider)
        self._tmp_dir = tempfile.mkdtemp()
        os.makedirs(self._tmp_dir, exist_ok=True)
        self._scan = MockHDF5(
            os.path.join(self._tmp_dir, "my_scan"),
            n_proj=30,
            dim=10,
        ).scan

    def tearDown(self):
        shutil.rmtree(self._tmp_dir)
        self._widget.close()
        self._widget = None
        self.qapp.processEvents()
        super().tearDown()

    def _waitImages(self):
        for _ in range(5):
            self.qapp.processEvents()
            time.sleep(0.1)

    def testASAPMode(self):
        self._widget.setLoadingMode("load ASAP")
        self._widget.setForceSync(True)
        self._widget.addLeafScan(self._scan.master_file)
        self._waitImages()

        self.spinBox().setValue(20)
        self._waitImages()

        self.slider().setValue(10)
        self.qapp.processEvents()
