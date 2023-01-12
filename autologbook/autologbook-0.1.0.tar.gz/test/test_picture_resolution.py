# -*- coding: utf-8 -*-
"""
Created on Mon Sep 12 21:02:36 2022

@author: Antonio
"""

#  Copyright (c) 2022.  Antonio Bulgheroni.
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
#  documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
#  permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
#  Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
#  WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS
#  OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
#   documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
#   rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
#   permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#
#
#
#
#
import pytest

from autologbook.autoerror import WrongResolutionUnit
from autologbook.autotools import PictureResolution, ResolutionUnit


def test_creation():
    try:
        pr1 = PictureResolution(28.0, 28.0, ResolutionUnit.INCH)
    except (ValueError, WrongResolutionUnit):
        raise AssertionError

    with pytest.raises(ValueError):
        pr2 = PictureResolution(-1, 0, ResolutionUnit.INCH)

    with pytest.raises(WrongResolutionUnit):
        pr3 = PictureResolution(28.0, 28.0, 5)


def test_conversion():

    pr1 = PictureResolution(28., 28., ResolutionUnit.INCH)
    pr1.convert_to_unit(ResolutionUnit.CM)

    x, y, u = pr1.as_tuple()

    pr2 = PictureResolution(x, y, u)
    pr2.convert_to_unit(ResolutionUnit.INCH)

    assert pr1 == pr2
