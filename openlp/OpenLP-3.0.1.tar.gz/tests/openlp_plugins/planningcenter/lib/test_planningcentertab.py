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
Package to test the openlp.plugins.planningcenter.lib.planningcentertab package.
"""
from unittest import TestCase
from unittest.mock import patch

from PyQt5 import QtCore, QtTest, QtWidgets

from openlp.core.common.registry import Registry
from openlp.core.common.settings import Settings
from openlp.core.state import State
from openlp.plugins.planningcenter.lib.planningcentertab import PlanningCenterTab
from openlp.plugins.planningcenter.planningcenterplugin import PlanningCenterPlugin
from tests.helpers.testmixin import TestMixin


class TestPlanningCenterTab(TestCase, TestMixin):
    """
    Test the PlanningCenterTab class
    """
    def setUp(self):
        """
        Create the UI
        """
        self.setup_application()
        Registry.create()
        State().load_settings()
        Registry().register('settings', Settings())
        self.plugin = PlanningCenterPlugin()
        Settings().setValue('planningcenter/application_id', 'abc')
        Settings().setValue('planningcenter/secret', '123')
        self.dialog = QtWidgets.QDialog()
        self.tab = PlanningCenterTab(self.dialog, 'PlanningCenter')
        self.tab.setup_ui()
        self.tab.retranslate_ui()
        self.tab.load()
        self.tab.resizeEvent()

    def tearDown(self):
        """
        Delete all the C++ objects at the end so that we don't have a segfault
        """
        del self.tab
        del self.dialog

    def test_bad_authentication_credentials(self):
        """
        Test that the tab can be created and Test authentication clicked for bad application id and secret
        """
        # GIVEN: A PlanningCenterTab Class
        # WHEN:  tab is drawn and application_id/secret values are entered in the GUI and the test buttin is clicked
        with patch('openlp.plugins.planningcenter.lib.planningcentertab.PlanningCenterAPI.check_credentials') \
            as mock_check_credentials, \
                patch('openlp.plugins.planningcenter.lib.planningcentertab.QtWidgets.QMessageBox.warning') \
                as mock_qmessagebox:
            mock_check_credentials.return_value = ''
            QtTest.QTest.mouseClick(self.tab.test_credentials_button, QtCore.Qt.LeftButton)
        # THEN:
        # The warning messagebox should be called
        self.assertEqual(mock_qmessagebox.call_count, 1, 'Warning dialog used for bad credentials')

    def test_empty_authentication_credentials(self):
        """
        Test that the tab can be created and Test authentication clicked for missing application id and secret
        """
        # GIVEN: A PlanningCenterTab Class
        # WHEN:  tab is drawn and application_id/secret values are entered in the GUI and the test buttin is clicked
        with patch('openlp.plugins.planningcenter.lib.planningcentertab.QtWidgets.QMessageBox.warning') \
                as mock_qmessagebox:
            self.tab.application_id_line_edit.setText('')
            self.tab.secret_line_edit.setText('')
            QtTest.QTest.mouseClick(self.tab.test_credentials_button, QtCore.Qt.LeftButton)
        # THEN:
        # The warning messagebox should be called
        self.assertEqual(mock_qmessagebox.call_count, 1, 'Warning dialog used for missing credentials')

    def test_good_authentication_credentials(self):
        """
        Test that the tab can be created and Test authentication clicked for good application id and secret
        """
        # GIVEN: A PlanningCenterTab Class
        # WHEN:  tab is drawn and application_id/secret values are entered in the GUI and the test buttin is clicked
        with patch('openlp.plugins.planningcenter.lib.planningcentertab.PlanningCenterAPI.check_credentials') \
            as mock_check_credentials, \
                patch('openlp.plugins.planningcenter.lib.planningcentertab.QtWidgets.QMessageBox.information') \
                as mock_qmessagebox:
            mock_check_credentials.return_value = 'good'
            QtTest.QTest.mouseClick(self.tab.test_credentials_button, QtCore.Qt.LeftButton)
        # THEN:
        # The information messagebox should be called
        self.assertEqual(mock_qmessagebox.call_count, 1, 'Information dialog used for good credentials')

    def test_save_credentials(self):
        """
        Test that credentials are saved in settings when the save function is called
        """
        # GIVEN: A PlanningCenterTab Class
        # WHEN: application id and secret values are set to something and the save function is called
        new_application_id = 'planningcenter'
        new_secret = 'woohoo'
        self.tab.application_id_line_edit.setText(new_application_id)
        self.tab.secret_line_edit.setText(new_secret)
        self.tab.save()
        # THEN: The settings version of application_id and secret should reflect the new values
        settings = Settings()
        application_id = settings.value('planningcenter/application_id')
        secret = settings.value('planningcenter/secret')
        self.assertEqual(application_id, new_application_id)
        self.assertEqual(secret, new_secret)
