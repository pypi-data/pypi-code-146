# -*- encoding: utf-8 -*-
"""
@File    :   __init__.py.py
@Time    :   2022-10-26 23:26
@Author  :   坐公交也用券
@Version :   1.0
@Contact :   faith01238@hotmail.com
@Homepage : https://liumou.site
@Desc    :   彩色日志模块
"""
# Copyright Jonathan Hartley 2013. BSD 3-Clause license, see LICENSE file.
# from .initialise import init, deinit, reinit, colorama_text
# from .ansi import Fore, Back, Style, Cursor
# from .ansitowin32 import AnsiToWin32

from .ColorInfo import ColorLogger
__all__ = ["ColorLogger"]
__version__ = '1.0.0'

