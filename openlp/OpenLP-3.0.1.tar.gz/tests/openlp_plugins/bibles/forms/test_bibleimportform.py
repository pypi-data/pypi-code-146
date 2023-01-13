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
Package to test the openlp.plugins.bibles.forms.bibleimportform package.
"""
from unittest import TestCase, skip
from unittest.mock import MagicMock, patch

from PyQt5 import QtWidgets, QtTest, QtCore

from openlp.core.common.registry import Registry
from openlp.plugins.bibles.forms.bibleimportform import BibleImportForm
from tests.helpers.testmixin import TestMixin


@skip('One of the QFormLayouts in the BibleImportForm is causing a segfault')
class TestBibleImportForm(TestCase, TestMixin):
    """
    Test the BibleImportForm class
    """

    def setUp(self):
        """
        Create the UI
        """
        Registry.create()
        self.setup_application()
        self.main_window = QtWidgets.QMainWindow()
        Registry().register('main_window', self.main_window)
        self.mocked_manager = MagicMock()
        self.form = BibleImportForm(self.main_window, self.mocked_manager, MagicMock())

    def tearDown(self):
        """
        Delete all the C++ objects at the end so that we don't have a segfault
        """
        del self.form
        del self.main_window

    @patch('openlp.plugins.bibles.forms.bibleimportform.CWExtract.get_bibles_from_http')
    @patch('openlp.plugins.bibles.forms.bibleimportform.BGExtract.get_bibles_from_http')
    @patch('openlp.plugins.bibles.forms.bibleimportform.BSExtract.get_bibles_from_http')
    def test_on_web_update_button_clicked(self, mocked_bsextract, mocked_bgextract, mocked_cwextract):
        """
        Test that on_web_update_button_clicked handles problems correctly
        """
        # GIVEN: Some mocked GUI components and mocked bibleextractors
        self.form.web_source_combo_box = MagicMock()
        self.form.web_translation_combo_box = MagicMock()
        self.form.web_update_button = MagicMock()
        self.form.web_progress_bar = MagicMock()
        mocked_bsextract.return_value = None
        mocked_bgextract.return_value = None
        mocked_cwextract.return_value = None

        # WHEN: Running on_web_update_button_clicked
        self.form.on_web_update_button_clicked()

        # THEN: The webbible list should still be empty
        assert self.form.web_bible_list == {}, 'The webbible list should be empty'

    def test_custom_init(self):
        """
        Test that custom_init works as expected if pysword is unavailable
        """
        # GIVEN: A mocked sword_tab_widget
        self.form.sword_tab_widget = MagicMock()

        # WHEN: Running custom_init
        self.form.custom_init()

        # THEN: sword_tab_widget.setDisabled(True) should have been called
        self.form.sword_tab_widget.setDisabled.assert_called_with(True)

    @patch.object(BibleImportForm, 'provide_help')
    def test_help(self, mocked_help, settings):
        """
        Test the help button
        """
        # GIVEN: A bible import wizard and a patched help function
        bible_import_form = BibleImportForm(None, MagicMock(), None)

        # WHEN: The Help button is clicked
        QtTest.QTest.mouseClick(bible_import_form.button(QtWidgets.QWizard.HelpButton), QtCore.Qt.LeftButton)

        # THEN: The Help function should be called
        mocked_help.assert_called_once()
