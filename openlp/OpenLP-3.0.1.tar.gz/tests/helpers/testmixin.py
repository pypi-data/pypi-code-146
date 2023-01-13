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
Mixin class with helpers
"""
import os
from tempfile import mkstemp

from PyQt5 import QtCore, QtWidgets

from openlp.core.common.settings import Settings


class TestMixin(object):
    """
    The :class:`TestMixin` class provides test with extra functionality
    """

    def setup_application(self):
        """
        Build or reuse the Application object
        """
        old_app_instance = QtCore.QCoreApplication.instance()
        if old_app_instance is None:
            self.app = QtWidgets.QApplication([])
        else:
            self.app = old_app_instance

    def build_settings(self):
        """
        Build the settings Object and initialise it
        """
        self.fd, self.ini_file = mkstemp('.ini')
        Settings.set_filename(self.ini_file)
        Settings().setDefaultFormat(Settings.IniFormat)
        # Needed on windows to make sure a Settings object is available during the tests
        self.setting = Settings()
        Settings().setValue('themes/global theme', 'my_theme')

    def destroy_settings(self):
        """
        Destroy the Settings Object
        """
        del self.setting
        os.close(self.fd)
        os.unlink(Settings().fileName())
