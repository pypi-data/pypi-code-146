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

__authors__ = [
    "H. Payno",
]
__license__ = "MIT"
__date__ = "12/07/2022"


from tomwer.gui.control.datalist import VolumeList
from tomwer.gui.qfolderdialog import QVolumeDialog

from .selectorwidgetbase import _SelectorWidget
import logging

logger = logging.getLogger(__name__)


class VolumeSelectorWidget(_SelectorWidget):
    """Widget used to select a volume on a list"""

    def _buildDataList(self):
        return VolumeList(self)

    def _callbackAddData(self):
        dialog = QVolumeDialog(self)

        if not dialog.exec_():
            dialog.close()
            return

        volume = dialog.getVolume()
        if volume is not None:
            added_objs = self.add(volume)
            self.setMySelection(added_objs)
        self.sigUpdated.emit()
