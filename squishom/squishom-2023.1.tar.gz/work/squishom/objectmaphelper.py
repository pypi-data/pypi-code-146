# -*- coding: utf-8 -*-
# Copyright (C) 2016 - 2021 froglogic GmbH.
# Copyright (C) 2022 The Qt Company Ltd.
# All rights reserved.
#
# This file is part of Squish.
#
# Licensees holding a valid Squish License Agreement may use this
# file in accordance with the Squish License Agreement provided with
# the Software.
#
# This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
# WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
#
# See the LICENSE file in the toplevel directory of this package.
#
# Contact contact@froglogic.com if any conditions of this licensing are
# not clear to you.

class Wildcard(object):
    '''Class holds a wildcard pattern'''
    def __init__(self, pattern):
        self.__pattern = pattern

    @property
    def pattern(self):
        '''Get pattern'''
        return self.__pattern

class RegularExpression(object):
    '''Class holds a regular expression pattern'''
    def __init__(self, pattern):
        self.__pattern = pattern

    @property
    def pattern(self):
        '''Get pattern'''
        return self.__pattern

def symbolic_names(module):
    '''Returns a list of the existing symbolic names'''
    if "SYMBOLIC_NAMES" in module.__dict__:
        return module.__dict__["SYMBOLIC_NAMES"]

    return [k for k, v in module.__dict__.items() if isinstance(v, (dict, str)) and not k.startswith('__')]

def entries(module):
    result = {}
    for n in symbolic_names(module):
        result[n] = module.__dict__[n]
    return result
