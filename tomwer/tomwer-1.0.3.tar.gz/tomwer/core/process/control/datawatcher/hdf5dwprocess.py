# coding: utf-8
# /*##########################################################################
# Copyright (C) 2016-2017 European Synchrotron Radiation Facility
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
data watcher classes used to define the status of an acquisition for EDF
acquisitions
"""

__authors__ = ["C. Nemoz", "H. Payno"]
__license__ = "MIT"
__date__ = "30/09/2019"

from .datawatcherprocess import _DataWatcherProcess
import logging
import h5py

_logger = logging.getLogger(__name__)


class _DataWatcherProcessHDF5(_DataWatcherProcess):
    """
    look for hdf5 information
    """

    def __init__(self, dataDir, srcPattern, destPattern):
        super(_DataWatcherProcessHDF5, self).__init__(dataDir, srcPattern, destPattern)
        if h5py.is_hdf5(dataDir):
            self._nxtomo_file = dataDir

    def _removeAcquisition(self, scanID, reason):
        _logger.warning(
            "removing acquisition is not done for hdf5 data watcher " "process"
        )

    def is_data_complete(self):
        # For now data complete and is abort_is not handled for hdf5 and Nxtomo
        return True

    def is_abort(self):
        # For now data complete and is abort_is not handled for hdf5 and Nxtomo
        return False


class _BlissScanWatcherProcess(_DataWatcherProcess):
    def __init__(self, dataDir, srcPattern=None, destPattern=None):
        super().__init__(dataDir, srcPattern, destPattern)
        if h5py.is_hdf5(dataDir):
            self._blissScanFile = dataDir

    def _removeAcquisition(self, scanID, reason):
        _logger.warning(
            "remoing acquisition is not done for hdf5 data watcher " "process"
        )

    def is_data_complete(self):
        # For now data complete and is abort_is not handled for hdf5 and Nxtomo
        return True

    def is_abort(self):
        # For now data complete and is abort_is not handled for hdf5 and Nxtomo
        return False
