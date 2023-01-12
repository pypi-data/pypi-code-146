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
__date__ = "19/07/2018"

from silx.gui import qt
from orangewidget import widget
from orangewidget.widget import Input, Output
from tomwer.core.tomwer_object import TomwerObject


class NotifierWidgetOW(widget.OWBaseWidget):
    """
    simple widget which pop up and closes when recive a new object
    """

    name = "notifier"
    id = "orangecontrib.tomwer.widgets.control.NotifierOW"
    description = "Simple widget which pop up for 2 second when recives a new object"
    icon = "icons/notification.png"
    priority = 145
    keywords = ["control", "notifier", "notification"]

    want_main_area = False
    resizing_enabled = False
    compress_signal = False

    class Inputs:
        tomo_obj = Input(name="tomo_obj", type=TomwerObject, multiple=True)

    class Outputs:
        tomo_obj = Output(name="tomo_obj", type=TomwerObject)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.pop_up = None
        self.setLayout(qt.QVBoxLayout())
        self.label = qt.QLabel(parent=self)
        self.label.setMinimumSize(300, 200)
        self.layout().addWidget(self.label)

    @Inputs.tomo_obj
    def process(self, tomo_obj, *args, **kwargs):
        self.notify(tomo_obj)
        self.Outputs.tomo_obj.send(tomo_obj)

    def notify(self, tomo_obj):
        if self.pop_up is not None:
            self.pop_up.close()

        self.pop_up = NotificationMessage()
        text = f"Object {tomo_obj} received."
        self.pop_up.setText(text)
        self.pop_up.show()


class NotificationMessage(qt.QMessageBox):
    EXPOSITION_TIME = 3000  # in ms

    def __init__(self) -> None:
        super().__init__()
        self.setModal(False)
        self.setIcon(qt.QMessageBox.Information)
        # types = qt.QDialogButtonBox.Ok
        # self.setStandardButtons(types)
        self.addButton(
            f"Ok - will close automatically after {self.EXPOSITION_TIME / 1000}s",
            qt.QMessageBox.YesRole,
        )
        # print("self.standardButtons()", self.standardButtons())
        # self.standardButtons()[0].setText(f"Ok - will close automatically after {self.EXPOSITION_TIME / 1000}s")

    def show(self):
        super().show()
        timer = qt.QTimer(self)
        timer.singleShot(
            self.EXPOSITION_TIME,
            self.close,
        )
