# coding: utf-8
# /*##########################################################################
# Copyright (C) 2016- 2020 European Synchrotron Radiation Facility
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
#############################################################################
"""Module containing the TomoObject class. Parent class of any tomo object"""

__authors__ = ["H.Payno"]
__license__ = "MIT"
__date__ = "27/01/2022"


from typing import Union, Optional
from .identifier import BaseIdentifier
from tomoscan.utils import BoundingBox1D


class TomoObject:
    """Parent class of all tomographic object in tomoscan"""

    @staticmethod
    def from_identifier(identifier: Union[str, BaseIdentifier]):
        """Return the Dataset from a identifier"""
        raise NotImplementedError("Base class")

    def get_identifier(self) -> BaseIdentifier:
        """dataset unique identifier. Can be for example a hdf5 and
        en entry from which the dataset can be rebuild"""
        raise NotImplementedError("Base class")

    def get_bounding_box(self, axis: Optional[Union[str, int]] = None) -> BoundingBox1D:
        """
        Return the bounding box covered by the Tomo object
        axis is expected to be in (0, 1, 2) or (x==0, y==1, z==2)
        """
        raise NotImplementedError("Base class")
