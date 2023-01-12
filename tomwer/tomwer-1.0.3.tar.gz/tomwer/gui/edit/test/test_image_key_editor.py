# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2017 European Synchrotron Radiation Facility
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
__date__ = "28/10/2020"


from silx.gui import qt
from silx.gui.utils.testutils import TestCaseQt, SignalListener
from tomwer.test.utils import skip_gui_test
from tomwer.gui.edit.imagekeyeditor import (
    ImageKeyDialog,
    ImageKeyUpgraderWidget,
    _AddImageKeyUpgradeOperation,
)
from tomwer.core.utils.scanutils import MockHDF5
from tomoscan.esrf.hdf5scan import ImageKey
import tempfile
import pytest


@pytest.mark.skipif(skip_gui_test(), reason="skip gui test")
class TestImageKeyEditorGUI(TestCaseQt):
    """
    Simple test the interface for configuration is working
    """

    def setUp(self):
        TestCaseQt.setUp(self)
        self._widget = ImageKeyDialog(parent=None)
        self.output_folder = tempfile.mkdtemp()

        hdf5_mock = MockHDF5(
            scan_path=self.output_folder,
            n_ini_proj=20,
            n_proj=20,
        )
        self._scan = hdf5_mock.scan

    def tearDown(self):
        self._widget.setAttribute(qt.Qt.WA_DeleteOnClose)
        self._widget.close()
        self._widget = None

    def testEdition(self):
        modifications = {
            2: ImageKey.INVALID,
        }
        self._widget.setScan(self._scan)
        self._widget.setModifications(modifications)
        self.assertEqual(self._widget.getModifications(), modifications)


@pytest.mark.skipif(skip_gui_test(), reason="skip gui test")
class Test_AddImageKeyUpgradeOperation(TestCaseQt):
    def setUp(self):
        super().setUp()
        self._widget = _AddImageKeyUpgradeOperation()
        self._signalLisener = SignalListener()
        self._widget.sigOperationAdded.connect(self._signalLisener)

    def tearDown(self):
        self._widget.setAttribute(qt.Qt.WA_DeleteOnClose)
        self._widget.close()
        self._widget = None
        super().tearDown()

    def test(self):
        self._widget._addButtonPB.released.emit()
        self.qapp.processEvents()
        assert self._signalLisener.callCount() == 1
        assert self._signalLisener.callCount() == 1
        assert self._signalLisener.arguments() == [
            (
                {
                    "from_image_key": ImageKey.PROJECTION.value,
                    "to_image_key": ImageKey.DARK_FIELD.value,
                },
            ),
        ]


@pytest.mark.skipif(skip_gui_test(), reason="skip gui test")
class TestImageKeyUpgraderList(TestCaseQt):
    def setUp(self):
        super().setUp()
        self._widget = ImageKeyUpgraderWidget()

    def tearDown(self):
        self._widget.setAttribute(qt.Qt.WA_DeleteOnClose)
        self._widget.close()
        self._widget = None
        super().tearDown()

    def test_add_remove_operations(self):
        """
        test adding and remove operations to the list
        """
        self._widget.addOperation(
            from_image_key=ImageKey.PROJECTION, to_image_key=ImageKey.DARK_FIELD
        )
        assert self._widget.getOperations() == {
            ImageKey.PROJECTION: ImageKey.DARK_FIELD,
        }
        self._widget.addOperation(
            from_image_key=ImageKey.FLAT_FIELD, to_image_key=ImageKey.DARK_FIELD
        )
        assert self._widget.getOperations() == {
            ImageKey.PROJECTION: ImageKey.DARK_FIELD,
            ImageKey.FLAT_FIELD: ImageKey.DARK_FIELD,
        }
        self._widget.addOperation(
            from_image_key=ImageKey.PROJECTION, to_image_key=ImageKey.FLAT_FIELD
        )
        assert self._widget.getOperations() == {
            ImageKey.PROJECTION: ImageKey.FLAT_FIELD,
            ImageKey.FLAT_FIELD: ImageKey.DARK_FIELD,
        }
        self._widget.removeOperation(
            from_image_key=ImageKey.PROJECTION, to_image_key=ImageKey.FLAT_FIELD
        )
        assert self._widget.getOperations() == {
            ImageKey.FLAT_FIELD: ImageKey.DARK_FIELD,
        }
        self._widget.removeOperation(
            from_image_key=ImageKey.PROJECTION, to_image_key=ImageKey.DARK_FIELD
        )
        assert self._widget.getOperations() == {
            ImageKey.FLAT_FIELD: ImageKey.DARK_FIELD,
        }
        self._widget.removeOperation(
            from_image_key=ImageKey.FLAT_FIELD, to_image_key=ImageKey.DARK_FIELD
        )
        assert self._widget.getOperations() == {}

        self._widget.setOperations(
            {
                ImageKey.PROJECTION: ImageKey.FLAT_FIELD,
                ImageKey.FLAT_FIELD: ImageKey.DARK_FIELD,
            }
        )
        assert self._widget.getOperations() == {
            ImageKey.PROJECTION: ImageKey.FLAT_FIELD,
            ImageKey.FLAT_FIELD: ImageKey.DARK_FIELD,
        }
