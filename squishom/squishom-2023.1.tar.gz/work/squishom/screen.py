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

import squish

class Screen(object):
    LandscapeOrientation = 0x01
    PortraitOrientation = 0x02
    ReverseLandscapeOrientation = 0x04
    ReversePortraitOrientation = 0x08

    @staticmethod
    def count():
        """
        :rtype: int
        """
        try:
            return squish._squish_screen_count_get()
        except AttributeError:
            raise AttributeError('Trying to call undefined function. Make sure the AUT is running.')

    @staticmethod
    def byIndex(index):
        """
        :type index: int
        :rtype: Screen
        """
        return Screen(index)

    def __init__(self, index):
        if index < 0 or index >= Screen.count():
            raise IndexError('Screen index %d out of range' % index)
        self._index = index

    @property
    def index(self):
        return self._index

    @property
    def geometry(self):
        return squish._squish_screen_geometry_get(self._index)

    @property
    def orientation(self):
        return squish._squish_screen_orientation_get(self._index)

    @orientation.setter
    def orientation(self, orientation):
        squish._squish_screen_orientation_set(self._index, orientation)

