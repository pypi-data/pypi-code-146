# coding: utf-8
# /*##########################################################################
# Copyright (C) 2017 European Synchrotron Radiation Facility
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

"""
This module is used to define the process of the reference creator.
This is related to the issue #184
"""

__authors__ = ["H.Payno"]
__license__ = "MIT"
__date__ = "17/08/2021"


import os
from typing import Union
from silx.io.url import DataUrl
from silx.io.dictdump import dicttoh5
from tomoscan.io import HDF5File
import logging
from tomwer.core.process.reconstruction.darkref.darkrefs import DarkRefs
from tomwer.core.scan.scanbase import TomwerScanBase
from tomoscan.esrf.scan.utils import get_data
from tomoscan.esrf.scan.utils import copy_h5_dict_darks_to, copy_h5_dict_flats_to

logger = logging.getLogger(__name__)


class DarkRefsCopy(DarkRefs):
    """
    Reimplement Dark ref to deal with copy when there is no median/mean files
    """

    DEFAULT_SRCURRENT = 200.0  # mA

    def __init__(
        self,
        process_id=None,
        varinfo=None,
        inputs=None,
        node_id=None,
        node_attrs=None,
        execinfo=None,
    ):
        super().__init__(
            process_id=process_id,
            varinfo=varinfo,
            inputs=inputs,
            node_id=node_id,
            node_attrs=node_attrs,
            execinfo=execinfo,
        )
        if inputs is None:
            inputs = {}

        self._mode_auto = inputs.get("mode_auto", True)
        if "savedir" in inputs:
            raise KeyError("savedir is not a valid key. Use save_dir")
        self._savedir = inputs.get("save_dir", None)
        if self._savedir is None:
            raise KeyError(
                "save_dir is expected (where the ref and dark file should be saved)"
            )
        self._save_file = self.get_save_file(self._savedir)
        self._darks_url = self.get_darks_url(self._savedir)
        self._flats_url = self.get_flats_url(self._savedir)
        logger.info(f"Flats and darks will be stored in {self._save_file}")

        self._processOnlyCopy = inputs.get("process_only_copy", False)
        self._processOnlyDkRf = inputs.get("process_only_dkrf", False)
        init_ref_scan = inputs.get("init_dkrf_from", None)
        if init_ref_scan:
            if not isinstance(init_ref_scan, TomwerScanBase):
                raise TypeError(
                    "init_ref_scan is expected to be an instance of TomwerScanBase. Not {}".format(
                        type(init_ref_scan)
                    )
                )
            else:
                self.set_darks_and_flats_from_scan(init_ref_scan)

    @staticmethod
    def get_save_file(save_dir):
        return os.path.join(save_dir, "darks_and_flats.h5")

    @staticmethod
    def get_flats_url(save_dir):
        return DataUrl(
            file_path=DarkRefsCopy.get_save_file(save_dir),
            data_path="/flats",
            scheme="silx",
        )

    @staticmethod
    def get_darks_url(save_dir):
        return DataUrl(
            file_path=DarkRefsCopy.get_save_file(save_dir),
            data_path="/darks",
            scheme="silx",
        )

    def set_process_only_dkRf(self, value: bool) -> None:
        self._processOnlyDkRf = value
        self._processOnlyCopy = False

    def set_process_only_copy(self, value: bool) -> None:
        self._processOnlyDkRf = False
        self._processOnlyCopy = value

    @staticmethod
    def save_flats_to_be_copied(save_dir, data: Union[DataUrl, dict]):
        if isinstance(data, DataUrl):
            data = get_data(data)
        flat_url = DarkRefsCopy.get_flats_url(save_dir)
        dicttoh5(
            data,
            h5file=flat_url.file_path(),
            h5path=flat_url.data_path(),
            mode="a",
            update_mode="replace",
        )

    @staticmethod
    def save_darks_to_be_copied(save_dir, data: Union[DataUrl, dict]):
        if isinstance(data, DataUrl):
            data = get_data(data)
        dark_url = DarkRefsCopy.get_darks_url(save_dir)
        dicttoh5(
            data,
            h5file=dark_url.file_path(),
            h5path=dark_url.data_path(),
            mode="a",
            update_mode="replace",
        )

    def set_darks_and_flats_from_scan(self, scan: TomwerScanBase) -> bool:
        if scan.reduced_flats in (None, {}):
            logger.warning(f"No flat found for {scan}. Unable to copy them")
        else:
            dicttoh5(
                scan.reduced_flats,
                h5file=self._flats_url.file_path(),
                h5path=self._flats_url.data_path(),
                mode="a",
                update_mode="replace",
            )
        if scan.reduced_darks in (None, {}):
            logger.warning(f"No dark found for {scan}. Unable to copy them")
        else:
            dicttoh5(
                scan.reduced_darks,
                h5file=self._darks_url.file_path(),
                h5path=self._darks_url.data_path(),
                mode="a",
                update_mode="replace",
            )
        self._ref_has_been_set(scan=scan)

    def _ref_has_been_set(self, scan):
        pass

    def _copy_to(self, scan):
        if not isinstance(scan, TomwerScanBase):
            raise TypeError(
                "{} is expected to be a {} and not {}".format(
                    str(scan), TomwerScanBase, type(scan)
                )
            )

        if self.has_dark_stored():
            copy_h5_dict_darks_to(
                scan=scan,
                darks_url=self._darks_url,
                save=True,
                raise_error_if_url_empty=True,
            )
        if self.has_flat_stored():
            copy_h5_dict_flats_to(
                scan=scan,
                flats_url=self._flats_url,
                save=True,
                raise_error_if_url_empty=True,
            )

    def clean_save_files(self):
        if os.path.exists(self._save_file):
            os.remove(self._save_file)

    def run(self):
        """
        This is function triggered when a new scan / data is received.
        As explained in issue #184 the behavior is the following:

        * if the scan has already ref files files won't be overwrite
        * if the mode is in `auto` will register last ref file met
        * if the scan has no ref files and refCopy has some register. Will
          create a copy of those, normalized from srCurrent (for flat field)
        """
        scan = self.inputs.data
        if not isinstance(scan, (type(None), TomwerScanBase, dict)):
            raise TypeError(
                f"self.inputs.data is expected to be an instance "
                f"of None, TomwerScanBase or dict. Not {type(scan)}"
            )
        if scan is None or scan.path is None:
            return
        # process dark and ref calculation
        if not self._processOnlyCopy:
            super().run()
        # then copy if necessary
        if not self._processOnlyDkRf:
            if self.contains_dark_or_ref(scan):
                if self.is_on_mode_auto:
                    self.set_darks_and_flats_from_scan(scan)
            if self.has_missing_dark_or_ref(scan):
                self._copy_to(scan)

    def has_flat_or_dark_stored(self) -> bool:
        """

        :return: True if the process has at least registered one flat or one
                 dark
        :rtype: bool
        """
        return self.has_flat_stored() or self.has_dark_stored()

    def has_flat_stored(self) -> bool:
        """

        :return: True if the process has registered at least one ref
        :rtype: bool
        """
        if not os.path.exists(self._save_file):
            return False
        else:
            with HDF5File(self._save_file, mode="r") as h5f:
                return self._flats_url.data_path() in h5f

    def has_dark_stored(self) -> bool:
        """

        :return: True if the process has registered at least one dark
        :rtype: bool
        """
        if not os.path.exists(self._save_file):
            return False
        else:
            with HDF5File(self._save_file, mode="r") as h5f:
                return self._darks_url.data_path() in h5f

    def contains_dark(self, scan: TomwerScanBase) -> bool:
        """Return True if the scan has already some dark processed"""
        if not isinstance(scan, TomwerScanBase):
            return TypeError(
                "scan is expected to be an instance of {} and not {}".format(
                    TomwerScanBase, type(scan)
                )
            )
        else:
            return scan.reduced_darks or scan.load_reduced_darks()

    def contains_flat(self, scan: TomwerScanBase):
        """Return True if the scan has already some dark processed"""
        if not isinstance(scan, TomwerScanBase):
            return TypeError(
                "scan is expected to be an instance of {} and not {}".format(
                    TomwerScanBase, type(scan)
                )
            )
        else:
            return scan.reduced_flats or scan.load_reduced_flats()

    def contains_dark_or_ref(self, scan):
        return self.contains_dark(scan=scan) or self.contains_flat(scan=scan)

    def has_missing_dark_or_ref(self, scan: TomwerScanBase) -> bool:
        """return True if the scan has no ref or no dark registered"""
        assert isinstance(scan, TomwerScanBase)
        return not self.contains_dark(scan) or not self.contains_flat(scan)

    def _signal_done(self, scan):
        assert isinstance(scan, TomwerScanBase)
        raise NotImplementedError("Abstract class")

    def set_mode_auto(self, b):
        self._mode_auto = b

    @property
    def is_on_mode_auto(self):
        return self._mode_auto

    @property
    def refHST_prefix(self):
        return self._refHstPrefix

    @property
    def darkHST_prefix(self):
        return self._darkHstPrefix

    def set_refHST_prefix(self, prefix):
        self._refHstPrefix = prefix

    def set_darkHST_prefix(self, prefix):
        self._darkHstPrefix = prefix

    def clear_ref(self):
        if self._flat_save_file is not None:
            os.remove(self._flat_save_file)
        if self._dark_save_file is not None:
            os.remove(self._dark_save_file)
