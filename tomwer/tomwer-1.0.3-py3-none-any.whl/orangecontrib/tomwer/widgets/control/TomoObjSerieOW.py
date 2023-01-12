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

from orangewidget import gui
from orangewidget.widget import Output, Input, OWBaseWidget
from tomoscan.serie import Serie
from tomwer.core.tomwer_object import TomwerObject
from tomwer.web.client import OWClient
from orangewidget.settings import Setting
import tomwer.core.process.control.tomoobjserie
import logging

logger = logging.getLogger(__name__)


class TomoObjSerieOW(OWBaseWidget, OWClient, openclass=True):
    name = "tomo obj serie"
    id = "orange.widgets.tomwer.tomoobjserieow"
    description = "Allow user define a serie of object that will be defined as a Serie (grouped together and can be used within a purpose like stiching)"
    icon = "icons/tomoobjserie.svg"
    priority = 55
    keywords = ["tomography", "selection", "tomwer", "serie", "group"]

    ewokstaskclass = tomwer.core.process.control.tomoobjserie._TomoobjseriePlaceHolder

    want_main_area = True
    want_control_area = False
    resizing_enabled = True
    compress_signal = False

    _scanIDs = Setting(list())

    class Inputs:
        tomo_obj = Input(name="tomo obj", type=TomwerObject, multiple=True)

    class Outputs:
        serie = Output(name="serie", type=Serie)

    def __init__(self, parent=None):
        """ """
        OWBaseWidget.__init__(self, parent)
        OWClient.__init__(self)

    @Inputs.tomo_obj
    def addTomoObj(self, tomo_obj, id):
        if tomo_obj is not None:
            raise NotImplementedError()
            self.widget.add(tomo_obj)

    def send(self):
        raise NotImplementedError()
