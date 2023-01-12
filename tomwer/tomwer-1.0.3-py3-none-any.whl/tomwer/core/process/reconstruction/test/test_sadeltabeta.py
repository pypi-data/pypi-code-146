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
__date__ = "27/02/2021"


import unittest
from tomwer.core.process.reconstruction.sadeltabeta.sadeltabeta import (
    SADeltaBetaProcess,
    SADeltaBetaParams,
)
from tomwer.core.utils.scanutils import MockHDF5
import os
import tempfile
import shutil


class TestSADeltaBetaProcess(unittest.TestCase):
    """Test the SAAxisProcess class"""

    def setUp(self) -> None:
        super().setUp()
        self.tempdir = tempfile.mkdtemp()
        dim = 10
        mock = MockHDF5(
            scan_path=self.tempdir, n_proj=10, n_ini_proj=10, scan_range=180, dim=dim
        )
        self.scan = mock.scan

    def tearDown(self) -> None:
        shutil.rmtree(self.tempdir)
        super().tearDown()

    def test(self):
        process = SADeltaBetaProcess(inputs={"data": self.scan})

        default_sadelta_beta_params = SADeltaBetaParams()
        default_sadelta_beta_params.output_dir = os.path.join(
            self.tempdir, "output_dir"
        )
        default_sadelta_beta_params.dry_run = True

        with self.assertRaises(Exception):
            process.run()
        process.set_configuration(default_sadelta_beta_params)
        process.run()
