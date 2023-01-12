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
__date__ = "11/07/2021"


from tomwer.core.process.reconstruction.normalization import params, normalization
from tomoscan.normalization import Method
from tomwer.core.utils.scanutils import MockHDF5
import unittest
import tempfile
import shutil
import h5py
import numpy


class TestNormalization(unittest.TestCase):
    """
    Test the normalization process
    """

    def setUp(self) -> None:
        self.tempdir = tempfile.mkdtemp()
        dim = 100
        self.scan = MockHDF5(
            scan_path=self.tempdir,
            n_proj=2,
            n_ini_proj=2,
            scan_range=180,
            dim=dim,
            create_ini_dark=False,
            create_ini_ref=False,
            create_final_ref=False,
        ).scan

    def tearDown(self) -> None:
        shutil.rmtree(self.tempdir)

    def testManualROI(self):
        # step1: rewrite the detector data to simplify result check
        with h5py.File(self.scan.master_file, mode="a") as h5f:
            dataset = h5f["/entry/instrument/detector/data"]
            assert dataset.shape == (2, 100, 100)
            del h5f["/entry/instrument/detector/data"]
            h5f["/entry/instrument/detector/data"] = numpy.arange(
                100 * 100 * 2
            ).reshape(2, 100, 100)

        process_params = normalization.SinoNormalizationParams()
        process_params.method = Method.SUBTRACTION
        process_params.source = params._ValueSource.MANUAL_ROI
        expected_results = {
            "mean": numpy.array([800.5, 10800.5]),
            "median": numpy.array([800.5, 10800.5]),
        }

        for calc_fct in params._ValueCalculationFct.values():
            with self.subTest(calc_fct=calc_fct):
                process_params.extra_infos = {
                    "start_x": 0,
                    "end_x": 2,
                    "start_y": 8,
                    "end_y": 9,
                    "calc_fct": calc_fct,
                    "calc_area": "volume",
                }
                process = normalization.SinoNormalizationTask(
                    inputs={
                        "data": self.scan,
                        "configuration": process_params,
                    }
                )
                process.run()
                res = self.scan.intensity_normalization.get_extra_infos().get("value")
                if isinstance(res, numpy.ndarray):
                    numpy.testing.assert_array_equal(res, expected_results[calc_fct])
                else:
                    numpy.testing.assert_array_equal(res, expected_results[calc_fct])
