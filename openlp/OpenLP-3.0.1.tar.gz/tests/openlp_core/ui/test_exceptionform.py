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
Package to test the openlp.core.ui.exeptionform package.
"""
import os
import tempfile
from collections import OrderedDict
from pathlib import Path
from unittest import TestCase
from unittest.mock import call, patch

from openlp.core.common.settings import Settings
from openlp.core.common.registry import Registry
from openlp.core.ui import exceptionform
from tests.helpers.testmixin import TestMixin


exceptionform.MIGRATE_VERSION = 'Migrate Test'
exceptionform.CHARDET_VERSION = 'CHARDET Test'
exceptionform.ENCHANT_VERSION = 'Enchant Test'
exceptionform.MAKO_VERSION = 'Mako Test'
exceptionform.ICU_VERSION = 'ICU Test'
exceptionform.VLC_VERSION = 'VLC Test'

MAIL_ITEM_TEXT = ('**OpenLP Bug Report**\nVersion: Trunk Test\n\n--- Details of the Exception. ---\n\n'
                  'Description Test\n\n --- Exception Traceback ---\nopenlp: Traceback Test\n'
                  '--- System information ---\nPlatform: Nose Test\n\n--- Library Versions ---\n'
                  'Python: Python Test\nQt5: Qt5 Test\nPyQt5: PyQt5 Test\n'
                  'SQLAlchemy: SQLAlchemy Test\nAlembic: Alembic Test\nBeautifulSoup: BeautifulSoup Test\n'
                  'lxml: ETree Test\nChardet: Chardet Test\nPyEnchant: PyEnchant Test\nMako: Mako Test\n'
                  'pyICU: pyICU Test\nVLC: VLC Test\nPyUNO: UNO Bridge Test\n')
LIBRARY_VERSIONS = OrderedDict([
    ('Python', 'Python Test'),
    ('Qt5', 'Qt5 Test'),
    ('PyQt5', 'PyQt5 Test'),
    ('SQLAlchemy', 'SQLAlchemy Test'),
    ('Alembic', 'Alembic Test'),
    ('BeautifulSoup', 'BeautifulSoup Test'),
    ('lxml', 'ETree Test'),
    ('Chardet', 'Chardet Test'),
    ('PyEnchant', 'PyEnchant Test'),
    ('Mako', 'Mako Test'),
    ('pyICU', 'pyICU Test'),
    ('VLC', 'VLC Test')
])


@patch('openlp.core.ui.exceptionform.QtGui.QDesktopServices.openUrl')
@patch('openlp.core.ui.exceptionform.get_version')
@patch('openlp.core.ui.exceptionform.get_library_versions')
@patch('openlp.core.ui.exceptionform.is_linux')
@patch('openlp.core.ui.exceptionform.platform.platform')
class TestExceptionForm(TestMixin, TestCase):
    """
    Test functionality of exception form functions
    """
    def __method_template_for_class_patches(self, __PLACEHOLDER_FOR_LOCAL_METHOD_PATCH_DECORATORS_GO_HERE__,
                                            mocked_platform, mocked_is_linux, mocked_get_library_versions,
                                            mocked_get_version, mocked_openurl):
        """
        Template so you don't have to remember the layout of class mock options for methods
        """
        mocked_is_linux.return_value = False
        mocked_get_version.return_value = 'Trunk Test'
        mocked_get_library_versions.return_value = LIBRARY_VERSIONS

    def setUp(self):
        self.setup_application()
        self.app.setApplicationVersion('0.0')
        # Set up a fake "set_normal_cursor" method since we're not dealing with an actual OpenLP application object
        self.app.set_normal_cursor = lambda: None
        self.app.process_events = lambda: None
        Registry.create()
        Registry().register('application', self.app)
        Registry().register('settings', Settings())
        self.tempfile = os.path.join(tempfile.gettempdir(), 'testfile')

    def tearDown(self):
        if os.path.isfile(self.tempfile):
            os.remove(self.tempfile)

    @patch("openlp.core.ui.exceptionform.Ui_ExceptionDialog")
    @patch("openlp.core.ui.exceptionform.FileDialog")
    @patch("openlp.core.ui.exceptionform.QtCore.QUrl")
    @patch("openlp.core.ui.exceptionform.QtCore.QUrlQuery.addQueryItem")
    def test_on_send_report_button_clicked(self, mocked_add_query_item, mocked_qurl, mocked_file_dialog,
                                           mocked_ui_exception_dialog, mocked_platform, mocked_is_linux,
                                           mocked_get_library_versions, mocked_get_version, mocked_openurl):
        """
        Test send report  creates the proper system information text
        """
        # GIVEN: Test environment
        mocked_platform.return_value = 'Nose Test'
        mocked_is_linux.return_value = False
        mocked_get_version.return_value = 'Trunk Test'
        mocked_get_library_versions.return_value = LIBRARY_VERSIONS
        test_form = exceptionform.ExceptionForm()
        test_form.file_attachment = None

        with patch.object(test_form, '_get_pyuno_version') as mock_pyuno, \
                patch.object(test_form.exception_text_edit, 'toPlainText') as mock_traceback, \
                patch.object(test_form.description_text_edit, 'toPlainText') as mock_description:
            mock_pyuno.return_value = 'UNO Bridge Test'
            mock_traceback.return_value = 'openlp: Traceback Test'
            mock_description.return_value = 'Description Test'

            # WHEN: on_send_report_button_clicked called
            test_form.on_send_report_button_clicked()

        # THEN: Verify strings were formatted properly
        mocked_add_query_item.assert_called_with('body', MAIL_ITEM_TEXT)

    @patch("openlp.core.ui.exceptionform.FileDialog.getSaveFileName")
    def test_on_save_report_button_clicked(self, mocked_save_filename, mocked_platform, mocked_is_linux,
                                           mocked_get_library_versions, mocked_get_version, mocked_openurl):
        """
        Test save report saves the correct information to a file
        """
        mocked_platform.return_value = 'Nose Test'
        mocked_is_linux.return_value = False
        mocked_get_version.return_value = 'Trunk Test'
        mocked_get_library_versions.return_value = LIBRARY_VERSIONS
        with patch.object(Path, 'open') as mocked_path_open:
            test_path = Path('testfile.txt')
            mocked_save_filename.return_value = test_path, 'ext'

            test_form = exceptionform.ExceptionForm()
            test_form.file_attachment = None

            with patch.object(test_form, '_get_pyuno_version') as mock_pyuno, \
                    patch.object(test_form.exception_text_edit, 'toPlainText') as mock_traceback, \
                    patch.object(test_form.description_text_edit, 'toPlainText') as mock_description:
                mock_pyuno.return_value = 'UNO Bridge Test'
                mock_traceback.return_value = 'openlp: Traceback Test'
                mock_description.return_value = 'Description Test'

                # WHEN: on_save_report_button_clicked called
                test_form.on_save_report_button_clicked()

        # THEN: Verify proper calls to save file
        # self.maxDiff = None
        mocked_path_open.assert_has_calls([call().__enter__().write(MAIL_ITEM_TEXT)])
