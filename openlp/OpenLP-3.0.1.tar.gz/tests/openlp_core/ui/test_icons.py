# -*- coding: utf-8 -*-
##########################################################################
# OpenLP - Open Source Lyrics Projection                                 #
# ---------------------------------------------------------------------- #
# Copyright (c) 2008-2023 OpenLP Developers                              #
# ---------------------------------------------------------------------- #
# This program is free software: you can redistribute it and/or modify   #
# it under the terms of the GNU General Public License as published by   #
# the Free Software Foundation, either version 3 of the License, or      #
# (at your option) any later version.                                    #
#                                                                        #
# This program is distributed in the hope that it will be useful,        #
# but WITHOUT ANY WARRANTY; without even the implied warranty of         #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          #
# GNU General Public License for more details.                           #
#                                                                        #
# You should have received a copy of the GNU General Public License      #
# along with this program.  If not, see <https://www.gnu.org/licenses/>. #
##########################################################################
"""
Package to test the openlp.core.ui.icons package.
"""
from unittest.mock import patch
from PyQt5 import QtGui

from openlp.core.ui.icons import UiIcons


def test_simple_icon(settings):
    # GIVEN: an basic set of icons
    with patch('openlp.core.ui.icons.UiIcons.__init__', return_value=None):
        icons = UiIcons()
        icon_list = {
            'active': {'icon': 'fa.child'}
        }

        icons.load_icons(icon_list)
        # WHEN: I use the icons
        icon_active = UiIcons().active
        # THEN: I should have an icon
        assert isinstance(icon_active, QtGui.QIcon)
