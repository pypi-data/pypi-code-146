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
__date__ = "19/10/2021"


from tomwer.gui.reconstruction.nabu.slurm import SlurmSettingsWidget
from tomwer.core.settings import SlurmSettings
from silx.gui.utils.testutils import TestCaseQt
from silx.gui import qt
from tomwer.test.utils import skip_gui_test
import pytest


@pytest.mark.skipif(skip_gui_test(), reason="skip gui test")
class TestSlurmWidget(TestCaseQt):
    def setUp(self):
        TestCaseQt.setUp(self)
        self.slurmWidget = SlurmSettingsWidget(parent=None)

    def tearDown(self):
        self.slurmWidget.setAttribute(qt.Qt.WA_DeleteOnClose)
        self.slurmWidget.close()
        self.slurmWidget = None

    def testGetConfiguration(self):
        self.slurmWidget._slurmCB.setChecked(False)
        dict_res = self.slurmWidget.getConfiguration()
        expected_dict = {
            "active_slurm": False,
            "cpu-per-task": SlurmSettings.N_CORES_PER_TASK,
            "n_tasks": SlurmSettings.N_TASKS,
            "memory": SlurmSettings.MEMORY_PER_WORKER,
            "partition": SlurmSettings.PARTIION,
            "n_gpus": SlurmSettings.N_GPUS_PER_WORKER,
        }
        assert dict_res == expected_dict, f"{dict_res} vs {expected_dict}"

    def testSetConfiguration(self):
        self.slurmWidget.setConfiguration(
            {
                "cpu-per-task": 2,
                "n_tasks": 3,
                "memory": 156,
                "partition": "test-queue",
                "n_gpus": 5,
            }
        )

        assert self.slurmWidget.getNCores() == 2
        assert self.slurmWidget.getNWorkers() == 3
        assert self.slurmWidget.getMemory() == 156
        assert self.slurmWidget.getQueue() == "test-queue"
        assert self.slurmWidget.getNGPU() == 5
