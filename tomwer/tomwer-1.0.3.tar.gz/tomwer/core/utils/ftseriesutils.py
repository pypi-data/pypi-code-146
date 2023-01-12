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
__date__ = "20/01/2017"

import logging
import operator
import os

logger = logging.getLogger(__name__)


def get_vol_file_shape(file_path):
    ddict = {}
    f = open(file_path, "r")
    lines = f.readlines()
    for line in lines:
        if "=" not in line:
            continue
        line_str = line.rstrip().replace(" ", "")
        line_str = line_str.split("#")[0]
        key, value = line_str.split("=")
        ddict[key.lower()] = value

    dimX = None
    dimY = None
    dimZ = None

    if "num_z" in ddict:
        dimZ = int(ddict["num_z"])
    if "num_y" in ddict:
        dimY = int(ddict["num_y"])
    if "num_x" in ddict:
        dimX = int(ddict["num_x"])

    return (dimZ, dimY, dimX)


def orderFileByLastLastModification(folder, fileList):
    """Return the list of files sorted by time of last modification.
    From the oldest to the newest modify"""
    res = {}
    for f in fileList:
        res[os.path.getmtime(os.path.join(folder, f))] = f

    return sorted(res.items(), key=operator.itemgetter(0))
