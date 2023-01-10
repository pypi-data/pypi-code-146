#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from poppy.core.generic.metaclasses import Singleton

__all__ = ['IDBToBit']


class IDBToBitMappingException(Exception):
    pass


class IDBToBit(object, metaclass=Singleton):
    """
    A class to convert IDB types to the good bit length.
    """

    def __init__(self):
        self.mapping = {
            'b1Bool': 1,
            'bU1': 1,
            'bU2': 2,
            'bU3': 3,
            'bU4': 4,
            'bU5': 5,
            'bU6': 6,
            'bU7': 7,
            'bU8': 8,
            'bU9': 9,
            'bU10': 10,
            'bU12': 12,
            'bU24': 24,
            'UShort': 16,
            'b10': 10,
            'Short': 16,
            'UInt': 32,
            'Float': 32,
        }

    def __call__(self, value):
        if value not in self.mapping:
            raise IDBToBitMappingException('{0} type not mapped'.format(value))
        return self.mapping[value]


# vim: set tw=79 :
