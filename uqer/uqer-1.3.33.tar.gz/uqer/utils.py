# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals

import sys
import os
import functools
from datetime import datetime

import dateutil.parser as dt_parser
from .config import *


def convert_date(date, format='%Y-%m-%d'):
    try:
        if isinstance(date, (str, unicode)):
            date = dt_parser.parse(date)
    except Exception as e:
        raise Exception('date:{}格式不能识别。' % date)

    return date.strftime(format)


def format_print(text, with_date=False, date_format='%Y-%m-%d %H:%M:%S,%f', end='\n'):
    """
    格式化文本输出
    Args:
        text: str
        with_date: bool
            default True
        date_format: str
        end: str
    Returns:
    """
    print('{} {}'.format(datetime.now().strftime(date_format), text), end=end) if with_date else print(text, end=end)


class Authorization(object):

    def __init__(self, name):
        self.name = name

    def __call__(self, func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if os.environ.get(self.name) == '1':
                return func(*args, **kwargs)
            else:
                print('您没有{}权限，可以联系4000 820 386进行购买。'.format(self.name))
                sys.exit(-1)

        return wrapper
