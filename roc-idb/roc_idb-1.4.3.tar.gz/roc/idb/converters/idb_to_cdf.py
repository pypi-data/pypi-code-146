#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from poppy.core.generic.metaclasses import Singleton
from poppy.core.logger import logger

__all__ = ['IDBToCDF']


class IDBToCDF(object, metaclass=Singleton):
    """
    A class to convert a value to the good type of the CDF variable.
    """

    def __init__(self):
        self.mapping = {
            'b1Bool': 'CDF_UINT1',
            'bU1': 'CDF_UINT1',
            'bU2': 'CDF_UINT1',
            'bU3': 'CDF_UINT1',
            'bU4': 'CDF_UINT1',
            'bU5': 'CDF_UINT1',
            'bU6': 'CDF_UINT1',
            'bU7': 'CDF_UINT1',
            'bU8': 'CDF_UINT1',
            'bU9': 'CDF_UINT2',
            'bU10': 'CDF_UINT2',
            'bU12': 'CDF_UINT2',
            'UShort': 'CDF_UINT2',
            'Short': 'CDF_INT2',
            'bU24': 'CDF_UINT4',
            'UInt': 'CDF_UINT4',
            'b10': 'CDF_INT2',
            '4': 'CDF_UINT4',
            'Float': 'CDF_REAL4',
        }

    def __call__(self, value):
        if value not in self.mapping:
            logger.error('{0} type not mapped'.format(value))
            return
        return self.mapping[value]


# vim: set tw=79 :
