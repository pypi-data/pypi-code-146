# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2016-2021 European Synchrotron Radiation Facility
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
__date__ = "25/08/2022"

from orangewidget import widget, gui
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.core.scan.scanfactory import ScanFactory
from tomwer.core.tomwer_object import TomwerObject
from tomwer.core.volume.volumefactory import VolumeFactory
from tomwer.gui.control.singletomoobj import SingleTomoObj
from tomwer.web.client import OWClient
from orangewidget.settings import Setting
from orangewidget.widget import Output, Input, OWBaseWidget
import tomoscan.esrf.scan.utils
import tomwer.core.process.control.singletomoobj
import logging

_logger = logging.getLogger(__name__)


class SingleTomoObjOW(OWBaseWidget, OWClient, openclass=True):
    name = "single tomo obj"
    id = "orange.widgets.tomwer.control.SingleScanOW.SingleScanOW"
    description = "Definition of a single dataset"
    icon = "icons/single_tomo_obj.svg"
    priority = 51
    keywords = ["tomography", "NXtomo", "tomwer", "folder", "scan"]

    want_main_area = True
    want_control_area = False
    resizing_enabled = True
    compress_signal = False

    ewokstaskclass = tomwer.core.process.control.singletomoobj.SingleTomoObjProcess

    _tomo_obj_setting = Setting(str())

    class Inputs:
        tomo_obj = Input(name="tomo_obj", type=TomwerObject)

    class Outputs:
        tomo_obj = Output(
            name="tomo_obj", type=TomwerObject, doc="one object to be process"
        )
        reduced_darks = Output(
            name="reduced dark(s)",
            type=dict,
            doc="DataUrl of the reduced dark. Key is the relative position, value is the reduced dark",
        )
        reduced_flats = Output(
            name="reduced flat(s)",
            type=dict,
            doc="DataUrl of the reduced flat. Key is the relative position, value is the reduced flat",
        )

    def __init__(self, parent=None):
        widget.OWBaseWidget.__init__(self, parent)
        OWClient.__init__(self)
        self._latest_received_scan = None
        # small work around to keep in scan processing cache and avoid recomputing it if not necessary
        self.widget = SingleTomoObj(parent=self)
        self.widget.sigTomoObjChanged.connect(self._updateSettings)
        self.widget.sigTomoObjChanged.connect(self._triggerObjDownstream)

        self._loadSettings()
        layout = gui.vBox(self.mainArea, self.name).layout()
        layout.addWidget(self.widget)

    @Inputs.tomo_obj
    def add(self, tomo_obj):
        if tomo_obj is None:
            return
        self.widget.setTomoObject(tomo_obj)

    def _loadSettings(self):
        if self._tomo_obj_setting != str():
            self.widget.setTomoObject(self._tomo_obj_setting)

    def _updateSettings(self):
        self._tomo_obj_setting = self.widget.getTomoObjIdentifier()

    def _triggerObjDownstream(self):
        obj_identifier = self.widget.getTomoObjIdentifier()
        if (
            self._latest_received_scan is not None
            and self._latest_received_scan.get_identifier() == obj_identifier
        ):
            data = self._latest_received_scan
        else:
            try:
                data = VolumeFactory.create_tomo_object_from_identifier(obj_identifier)
            except:  # noqa E722
                try:
                    data = ScanFactory.create_tomo_object_from_identifier(
                        obj_identifier
                    )
                except:  # noqa E722
                    _logger.warning(
                        f"Unable to find an obj with {obj_identifier} as identifier"
                    )
                    return

        self.Outputs.tomo_obj.send(data)
        # if the data is a scan then provide also access to the reduced frames. Can be convenient
        if isinstance(data, TomwerScanBase):
            if data.reduced_darks not in (None, {}):
                # we want to send those in relative position to have something generic. This is a convention for now
                self.Outputs.reduced_darks.send(
                    tomoscan.esrf.scan.utils.from_absolute_reduced_frames_to_relative(
                        reduced_frames=data.reduced_darks, scan=data
                    )
                )
            if data.reduced_flats not in (None, {}):
                # we want to send those in relative position to have something generic. This is a convention for now
                self.Outputs.reduced_flats.send(
                    tomoscan.esrf.scan.utils.from_absolute_reduced_frames_to_relative(
                        reduced_frames=data.reduced_flats, scan=data
                    )
                )
