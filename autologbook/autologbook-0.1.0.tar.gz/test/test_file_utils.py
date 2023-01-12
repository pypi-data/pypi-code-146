# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 15:40:04 2022

@author: elog-admin
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

from pathlib import Path

from autologbook.autotools import DateType, get_date_from_file, pretty_fmt_filesize


def test_filesize():
    file = Path(__file__)
    size = file.stat().st_size
    print(f'This file size is {pretty_fmt_filesize(size)}')


def test_date_from_file():
    file = Path(__file__)
    get_date_from_file(file.stat(), DateType.ATIME)
    get_date_from_file(file.stat(), DateType.CTIME)
    get_date_from_file(file.stat(), DateType.MTIME)

    # print(f'{atime:%Y-%m-%d %H:%M:%S}')
    # print(f'{ctime:%Y-%m-%d %H:%M:%S}')
    # print(f'{mtime:%Y-%m-%d %H:%M:%S}')
