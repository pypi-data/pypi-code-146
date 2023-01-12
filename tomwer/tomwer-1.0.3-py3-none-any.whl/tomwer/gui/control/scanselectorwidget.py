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
__date__ = "25/05/2018"


from tomwer.gui.qfolderdialog import QDataDialog
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.gui.control.datalist import GenericScanList
from .selectorwidgetbase import _SelectorWidget
import logging

logger = logging.getLogger(__name__)


class ScanSelectorWidget(_SelectorWidget):
    """Widget used to select a scan on a list"""

    def _buildDataList(self):
        return GenericScanList(parent=self)

    def n_scan(self) -> int:
        return super().n_data()

    def _callbackAddData(self):
        dialog = QDataDialog(self, multiSelection=True)

        if not dialog.exec_():
            dialog.close()
            return

        for folder in dialog.files_selected():
            tomo_objs = self.add(folder)
            self.setMySelection(tomo_objs)
        self.sigUpdated.emit()

    def setActiveData(self, data):
        if isinstance(data, TomwerScanBase):
            data = data.path
        super().setActiveData(data)
