#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from poppy.core.generic.metaclasses import Singleton
from poppy.core.logger import logger

__all__ = ['IDBToNumpy']


class IDBToNumpy(object, metaclass=Singleton):
    """
    A class to convert IDB types to the good numpy type.
    """

    def __init__(self):
        self.mapping = {
            'b1Bool': 'uint8',
            'bU1': 'uint8',
            'bU2': 'uint8',
            'bU3': 'uint8',
            'bU4': 'uint8',
            'bU5': 'uint8',
            'bU6': 'uint8',
            'bU7': 'uint8',
            'bU8': 'uint8',
            'bU9': 'uint16',
            'bU10': 'uint16',
            'bU12': 'uint16',
            'bU24': 'uint32',
            'UShort': 'uint16',
            'Short': 'int16',
            'b10': 'int16',
            'UInt': 'uint32',
            'Float': 'float32',
        }

    def __call__(self, value):
        if value not in self.mapping:
            logger.error('{0} type not mapped to C type'.format(value))
            return
        return self.mapping[value]


# vim: set tw=79 :
