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

class ToplevelWindow:

    @staticmethod
    def byName(objectName, timeout = None):
        """
        :type objectName: str
        :type timeout: int | None
        :rtype: ToplevelWindow
        """
        if timeout is None:
            return ToplevelWindow(squish.waitForObjectExists(objectName))
        return ToplevelWindow(squish.waitForObjectExists(objectName, timeout))

    @staticmethod
    def byObject(objectReference):
        """
        :type objectReference: object
        :rtype: ToplevelWindow
        """
        return ToplevelWindow(objectReference)

    @staticmethod
    def focused():
        """
        :rtype: ToplevelWindow
        """
        return ToplevelWindow(squish._squish_window_focused())

    def __init__(self, window):
        # TODO error handling, check validity of window
        self.window = window

    @property
    def geometry(self):
        return squish._squish_window_geometry_get(self.window)

    @property
    def nativeObject(self):
        return self.window

    def close(self):
        squish._squish_window_close(self.window)

    def maximize(self):
        squish._squish_window_maximize(self.window)

    def minimize(self):
        squish._squish_window_minimize(self.window)

    def moveTo(self, x, y):
        """
        :type x: int
        :type y: int
        """
        squish._squish_window_moveto(self.window, x, y)

    def resizeTo(self, w, h):
        """
        :type w: int
        :type h: int
        """
        squish._squish_window_resizeto(self.window, w, h)

    def restore(self):
        squish._squish_window_restore(self.window)

    def setFocus(self):
        squish._squish_window_focus_set(self.window)

    def setForeground(self):
        squish._squish_window_foreground_set(self.window)

    def setFullscreen(self):
        squish._squish_window_fullscreen_set(self.window)

    def __eq__(self, other):
        return self.nativeObject == other.nativeObject

