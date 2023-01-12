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
import os
import shutil
from tomwer.core.scan.edfscan import EDFTomoScan
from subprocess import getstatusoutput as myux
from glob import glob

_logger = logging.getLogger(__name__)
try:
    from tomwer.synctools.rsyncmanager import RSyncManager

    has_rsync = False
except ImportError:
    _logger.warning("rsyncmanager not available")
    has_rsync = True


def get_dir_size(dir):
    if not os.path.isdir(dir):
        err = "%s is not a directory, can't get size" % dir
        raise ValueError(err)
    else:
        aux = myux("du -ms " + dir.replace(" ", "\ "))  # noqa W605
        if len(aux) < 2:
            return 0
        return float((aux[1].split("\t"))[0])


def get_info_val(lines, key):
    r = range(len(lines))
    key = key + "="
    for i in r:
        if key in lines[i]:
            val = float(lines[i].split("=")[1])
    return val


class _DataWatcherEDFProcess(_DataWatcherProcess):
    """
    Base class for edf acquisition observation
    """

    XML_EXT = ".xml"

    SLICE_WC = "slice"

    INFO_EXT = ".info"

    FILE_INFO_KEYS = ["TOMO_N", "REF_ON", "REF_N", "DARK_N"]

    DEFAULT_DETECTOR = "Frelon"

    DATA_EXT = "0000.edf"

    def __init__(self, dataDir, srcPattern=None, destPattern=None):
        super(_DataWatcherEDFProcess, self).__init__(
            dataDir=dataDir, srcPattern=srcPattern, destPattern=destPattern
        )
        self.expected_dirsize = 0
        self.dirsize = 0
        self.file_rec_ext = ".rec"  # never used

    def _removeAcquisition(self, scanID, reason):
        if os.path.exists(scanID) and os.path.isdir(scanID):
            if self._removed is None:
                _logger.info("removing folder %s because %s" % (scanID, reason))
                if has_rsync:
                    RSyncManager().removeDir(scanID)
                    # avoid multiple removal as removal is asynchronous and might
                    # fail
                    self._removed = scanID
                else:
                    shutil.rmtree(scanID)

    def is_abort(self):
        if os.path.exists(path=self.scan_name):
            return EDFTomoScan(scan=self.scan_name).is_abort(
                src_pattern=self.srcPattern, dest_pattern=self.destPattern
            )
        else:
            return False


class _DataWatcherProcessXML(_DataWatcherEDFProcess):
    """
    This method will parse the [scan].info file and look if all .edf file
    specified in the .info file are recorded and complete.
    """

    def __init__(self, dataDir, srcPattern, destPattern):
        _DataWatcherEDFProcess.__init__(self, dataDir, srcPattern, destPattern)

        # hack for acquisition on lbsram:
        # in this case .info and .xml are in /data instead of /lbsram. To simplify we copy those from /data to /lbsram
        # not very elegant but as this is expected to be 'legacy code'
        if self.srcPattern is not None and self.destPattern is not None:
            for ext in (self.INFO_EXT, self.XML_EXT):
                aux = self.parsing_dir.split(os.path.sep)
                file_on_lbsram = os.path.join(
                    self.RootDir, self.parsing_dir, aux[len(aux) - 1] + ext
                )

                file_on_nice = file_on_lbsram.replace(
                    self.srcPattern, self.destPattern, 1
                )
                if os.path.exists(file_on_nice) and not os.path.exists(file_on_lbsram):
                    try:
                        shutil.copyfile(file_on_nice, file_on_lbsram)
                    except Exception:
                        # in case for example dest pattern doesn't exists
                        pass

    def is_data_complete(self):
        self._sync()
        aux = self.parsing_dir.split(os.path.sep)
        xmlfilelbsram = os.path.join(
            self.RootDir, self.parsing_dir, aux[len(aux) - 1] + self.XML_EXT
        )

        if self.srcPattern is None:
            self.scan_completed = os.path.isfile(xmlfilelbsram)
        else:
            xmlfilenice = xmlfilelbsram.replace(self.srcPattern, self.destPattern, 1)

            self.scan_completed = os.path.isfile(xmlfilenice) or os.path.isfile(
                xmlfilelbsram
            )

        return self.scan_completed


class _DataWatcherProcessUserFilePattern(_DataWatcherEDFProcess):
    """
    This method will look for a specific pattern given by the user.
    If a file in the given folder exists then we will consider the acquisition
    ended

    :param str pattern: the pattern we are looking for
    """

    def __init__(self, dataDir, srcPattern, destPattern, pattern):
        _DataWatcherEDFProcess.__init__(self, dataDir, srcPattern, destPattern)
        self.pattern = pattern

    def is_data_complete(self):
        self._sync()
        fullPattern = os.path.join(self.getCurrentDir(), self.pattern)
        self.scan_completed = len(glob(fullPattern)) > 0
        return self.scan_completed


class _DataWatcherProcessParseInfo(_DataWatcherEDFProcess):
    """
    This method will look for a '[scan].info' pattern
    """

    def __init__(self, dataDir, srcPattern, destPattern):
        _DataWatcherEDFProcess.__init__(self, dataDir, srcPattern, destPattern)

    @staticmethod
    def get_data_size(edfType):
        if edfType in _DataWatcherProcessParseInfo.TYPES:
            return _DataWatcherProcessParseInfo.TYPES[edfType]
        else:
            return 2

    def is_data_complete(self):
        self._sync()

        aux = self.parsing_dir.split(os.path.sep)
        info_file = os.path.join(
            self.RootDir, self.parsing_dir, aux[len(aux) - 1] + self.INFO_EXT
        )

        if self.srcPattern is None:
            self.scan_completed = os.path.isfile(info_file)
        else:
            infofilenice = info_file.replace(self.srcPattern, self.destPattern, 1)

            self.scan_completed = os.path.isfile(infofilenice) or os.path.isfile(
                info_file
            )

        return self.scan_completed
