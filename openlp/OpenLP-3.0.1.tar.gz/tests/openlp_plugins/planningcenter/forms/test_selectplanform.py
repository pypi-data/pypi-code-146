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
Package to test the openlp.plugins.planningcenter.forms.selectplanform package.
"""
import os
import re
from datetime import date, datetime
from unittest import TestCase, skip
from unittest.mock import patch, MagicMock

from PyQt5 import QtWidgets, QtTest, QtCore

from openlp.core.common.registry import Registry
from openlp.core.common.settings import Settings
from openlp.core.state import State
from openlp.core.ui.servicemanager import ServiceManager
from openlp.core.ui.settingsform import SettingsForm
from openlp.core.ui.thememanager import ThemeManager
from openlp.plugins.bibles.bibleplugin import BiblePlugin
from openlp.plugins.bibles.lib.mediaitem import BibleMediaItem
from openlp.plugins.custom.customplugin import CustomPlugin
from openlp.plugins.custom.lib.mediaitem import CustomMediaItem
from openlp.plugins.planningcenter.forms.selectplanform import SelectPlanForm
from openlp.plugins.planningcenter.planningcenterplugin import PlanningCenterPlugin
from openlp.plugins.songs.lib.mediaitem import SongMediaItem
from openlp.plugins.songs.songsplugin import SongsPlugin
from tests.helpers.testmixin import TestMixin
from tests.utils.constants import TEST_RESOURCES_PATH

TEST_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), TEST_RESOURCES_PATH, 'planningcenter'))


class TestSelectPlanForm(TestCase, TestMixin):
    """
    Test the SelectPlanForm class
    """

    def setUp(self):
        """
        Create the UI
        """
        self.registry = Registry()
        Registry.create()
        self.setup_application()
        self.build_settings()
        State().load_settings()
        Registry().register('settings', Settings())
        Registry().register('main_window', MagicMock())
        self.application_id = 'abc'
        self.secret = '123'
        Settings().setValue('planningcenter/application_id', self.application_id)
        Settings().setValue('planningcenter/secret', self.secret)
        # init the planning center plugin so we have default values defined for Settings()
        self.planning_center_plugin = PlanningCenterPlugin()
        # setup our form
        self.form = SelectPlanForm()
        self.form.planning_center_api.airplane_mode = True
        self.form.planning_center_api.airplane_mode_directory = TEST_PATH
        self.theme_manager = ThemeManager(None)
        self.theme_manager.get_theme_names = MagicMock()
        self.theme_manager.get_theme_names.return_value = ['themeA', 'themeB']

    def tearDown(self):
        """
        Delete all the C++ objects at the end so that we don't have a segfault
        """
        del self.form
        del self.planning_center_plugin
        del self.theme_manager
        del self.registry
        self.destroy_settings()

    def test_initial_defaults(self):
        """
        Test that the SelectPlanForm displays with correct defaults
        """
        # GIVEN: An SelectPlanForm instance with airplane mode enabled, resources available,
        # a theme manager with mocked themes, and a fake date = Sunday (7/29/2018)
        with patch('PyQt5.QtWidgets.QDialog.exec'), \
                patch('openlp.plugins.planningcenter.forms.selectplanform.date') as mock_date:
            # need to always return 9/29/2019 for date.today()
            mock_date.today.return_value = date(2019, 9, 29)
            mock_date.side_effect = lambda *args, **kw: date(*args, **kw)
            # WHEN: The form is shown
            self.form.exec()
        # THEN: The correct count of service types show up in the combo box
        combo_box_count = self.form.service_type_combo_box.count()
        self.assertEqual(combo_box_count, 2,
                         'The service_type_combo_box contains 2 items')
        # The first service type is selected
        self.assertEqual(self.form.service_type_combo_box.currentText(), 'gbf',
                         'The service_type_combo_box defaults to "gbf"')
        # the selected plan is today (the mocked date is a Sunday). Set to lowercase beacuse in some locales
        # months is not capitalized.
        self.assertEqual(self.form.plan_selection_combo_box.currentText(),
                         'September 29, 2019',
                         'Incorrect default date selected for Plan Date')
        # count the number of themes listed and make sure it matches expected value
        self.assertEqual(self.form.song_theme_selection_combo_box.count(),
                         2, 'Count of song themes is incorrect')
        self.assertEqual(self.form.slide_theme_selection_combo_box.count(),
                         2, 'Count of custom slide themes is incorrect')

    def test_warning_messagebox_shown_for_bad_credentials(self):
        """
        Test that if we don't have good credentials, then it will show a QMessageBox with a warning in it
        """
        # GIVEN: A SelectPlanForm instance with airplane mode enabled, resources, available,
        #        mocked check_credentials function to return ''
        with patch('PyQt5.QtWidgets.QDialog.exec'), \
            patch.object(self.form.planning_center_api, 'check_credentials', return_value=''), \
                patch('PyQt5.QtWidgets.QMessageBox.warning') as mock_warning:
            # WHEN: form is displayed
            self.form.exec()
            # THEN: we should have called a warning messagebox
            mock_warning.assert_called_once()

    def test_disable_import_buttons(self):
        """
        Test that the import buttons are disabled when the "Select Plan Date" element in the
        Plan Selection List is selected.
        """
        # GIVEN: An SelectPlanForm instance with airplane mode enabled, resources available, and the form
        with patch('PyQt5.QtWidgets.QDialog.exec'):
            self.form.exec()
            # WHEN: The Select Plan combo box is set to "Select Plan Date"
            index = self.form.plan_selection_combo_box.findText('Select Plan Date')
            self.form.plan_selection_combo_box.setCurrentIndex(index)
        # THEN: "Import New" and "Refresh Service" buttons become inactive
        self.assertEqual(self.form.import_as_new_button.isEnabled(), False,
                         '"Import as New" button should be disabled')
        self.assertEqual(self.form.update_existing_button.isEnabled(), False,
                         '"Refresh Service" button should be disabled')

    def test_default_plan_date_is_next_sunday(self):
        """
        Test that the SelectPlanForm displays Next Sunday's Date by Default
        """
        # GIVEN: An SelectPlanForm instance with airplane mode enabled, resources available,
        # a theme manager with mocked themes, and a fake date =  (9/24/2019)
        with patch('PyQt5.QtWidgets.QDialog.exec'), \
                patch('openlp.plugins.planningcenter.forms.selectplanform.date') as mock_date:
            # need to always return 9/24/2019 for date.today()
            mock_date.today.return_value = date(2019, 9, 24)
            mock_date.side_effect = lambda *args, **kw: date(*args, **kw)
            self.form.exec()
            # WHEN: The second (index=1) service type is selected
            self.form.service_type_combo_box.setCurrentIndex(1)
        # THEN: The plan selection date is 9/29 (the following Sunday)
        self.assertEqual(self.form.plan_selection_combo_box.currentText(), 'September 29, 2019',
                         'The next Sunday\'s Date is not selected in the plan_selection_combo_box')

    def test_service_type_changed_called_when_service_type_combo_changed(self):
        """
        Test that the "on_service_type_combobox_changed" function is executed when the
        service_type_combobox is changed
        """
        # GIVEN: An SelectPlanForm instance with airplane mode enabled, resources available
        with patch('PyQt5.QtWidgets.QDialog.exec'):
            self.form.exec()
        # WHEN: The Service Type combo is set to index 1
        self.form.service_type_combo_box.setCurrentIndex(1)
        # THEN: The on_service_type_combobox_changed function is called
        assert self.form.plan_selection_combo_box.count() > 0, 'Plan Selection Combo Box is not empty'
        assert self.form.plan_selection_combo_box.itemText(0) == 'Select Plan Date', 'Plan Combo Box has default text'

    def test_plan_selection_changed_called_when_plan_selection_combo_changed(self):
        """
        Test that the "on_plan_selection_combobox_changed" function is executed when the
        plan_selection_combobox is changed
        """
        # GIVEN: An SelectPlanForm instance with airplane mode enabled, resources available,
        with patch('PyQt5.QtWidgets.QDialog.exec'):
            self.form.exec()
        # WHEN: The Service Type combo is set to index 1
        self.form.service_type_combo_box.setCurrentIndex(1)
        self.form.plan_selection_combo_box.setCurrentIndex(1)
        # THEN: The import and update buttons should be enabled
        assert self.form.import_as_new_button.isEnabled() is True, 'Import button should be enabled'
        assert self.form.update_existing_button.isEnabled() is True, 'Update button should be enabled'

    def test_settings_tab_displayed_when_edit_auth_button_clicked(self):
        """
        Test that the settings dialog is displayed when the edit_auth_button is clicked
        """
        # GIVEN: A SelectPlanForm instance with airplane mode enabled and resources available
        with patch('PyQt5.QtWidgets.QDialog.exec'), \
                patch('openlp.core.ui.settingsform.SettingsForm.exec') as mock_settings_form:
            SettingsForm()
            self.form.exec()
            # WHEN: the edit_auth_button is clicked
            QtTest.QTest.mouseClick(self.form.edit_auth_button, QtCore.Qt.LeftButton)
        self.assertEqual(mock_settings_form.called, 1, "Settings Form opened when edit_auth_button clicked")

    def test_import_function_called_when_import_button_clicked(self):
        """
        Test that the "on_import_as_new_button_clicked" function is executed when the
        "Import New" button is clicked
        """
        # GIVEN: An SelectPlanForm instance with airplane mode enabled, resources available,
        with patch('PyQt5.QtWidgets.QDialog.exec'), \
                patch('openlp.plugins.planningcenter.forms.selectplanform.SelectPlanForm._do_import') \
                as mock_do_import:
            self.form.exec()
            # WHEN: The Service Type combo is set to index 1 and the Select Plan combo box is set
            # to index 1 and the "Import New" button is clicked
            self.form.service_type_combo_box.setCurrentIndex(1)
            self.form.plan_selection_combo_box.setCurrentIndex(4)
            QtTest.QTest.mouseClick(self.form.import_as_new_button, QtCore.Qt.LeftButton)
        # THEN: The on_import_as_new_button_cliced function is called
        mock_do_import.assert_called_with(update=False)

    def test_service_imported_when_import_button_clicked(self):
        """
        Test that a service is imported when the "Import New" button is clicked
        """
        # GIVEN: An SelectPlanForm instance with airplane mode enabled, resources available,
        # mocked out "on_new_service_clicked"
        with patch('PyQt5.QtWidgets.QDialog.exec'), \
                patch('openlp.plugins.planningcenter.lib.songimport.PlanningCenterSongImport.finish') \
                as mock_song_import, \
                patch('openlp.plugins.planningcenter.lib.customimport.CustomSlide') as mock_custom_slide_import, \
                patch('openlp.plugins.planningcenter.forms.selectplanform.parse_reference') as mock_bible_import, \
                patch('openlp.plugins.planningcenter.forms.selectplanform.date') as mock_date:
            # need to always return 9/29/2019 for date.today()
            mock_date.today.return_value = date(2019, 9, 29)
            mock_date.side_effect = lambda *args, **kw: date(*args, **kw)
            self.form.exec()
            Registry().register('service_manager', MagicMock())
            Registry().register('plugin_manager', MagicMock())
            Registry().register('songs', MagicMock())
            Registry().register('bibles', MagicMock())
            Registry().register('custom', MagicMock())
            # WHEN: The Service Type combo is set to index 1 and the Select Plan combo box is set to
            # index 1 and the "Import New" button is clicked
            self.form.service_type_combo_box.setCurrentIndex(1)
            QtTest.QTest.mouseClick(self.form.import_as_new_button, QtCore.Qt.LeftButton)
        # THEN: There should be 5 service items added, 1 song, 3 custom slides (one is a bible
        # title slide), and 1 bible verse
        self.assertEqual(mock_song_import.call_count, 1, '1 song added via song_media_item')
        self.assertEqual(mock_custom_slide_import.call_count, 4, '4 custom slide added via custom_media_item')
        self.assertEqual(mock_bible_import.call_count, 2, '2 bible verses submitted for parsing')

    def test_service_refreshed_when_refresh_button_clicked(self):
        """
        Test that a service is refreshed when the "Refresh Service" button is clicked
        """
        # GIVEN: An SelectPlanForm instance with airplane mode enabled, resources available,
        # mocked out "on_new_service_clicked"
        with patch('PyQt5.QtWidgets.QDialog.exec'), \
                patch('openlp.plugins.planningcenter.lib.songimport.PlanningCenterSongImport.finish') \
                as mock_song_import, \
                patch('openlp.plugins.planningcenter.lib.customimport.CustomSlide') as mock_custom_slide_import, \
                patch('openlp.plugins.planningcenter.forms.selectplanform.parse_reference') as mock_bible_import, \
                patch('openlp.plugins.planningcenter.forms.selectplanform.date') as mock_date:
            # need to always return 9/29/2019 for date.today()
            mock_date.today.return_value = date(2019, 9, 29)
            mock_date.side_effect = lambda *args, **kw: date(*args, **kw)
            self.form.exec()
            Registry().register('service_manager', MagicMock())
            Registry().register('plugin_manager', MagicMock())
            Registry().register('songs', MagicMock())
            Registry().register('bibles', MagicMock())
            Registry().register('custom', MagicMock())
            # WHEN: The Service Type combo is set to index 1 and the Select Plan combo box is
            # set to index 1 and the "Update" button is clicked
            self.form.service_type_combo_box.setCurrentIndex(1)
            QtTest.QTest.mouseClick(self.form.update_existing_button, QtCore.Qt.LeftButton)
        # THEN: There should be 5 service items added, 1 song, 3 custom slides (one is a bible
        # title slide), and 1 bible verse
        self.assertEqual(mock_song_import.call_count, 1, '1 song added via song_media_item')
        self.assertEqual(mock_custom_slide_import.call_count, 4, '4 custom slide added via custom_media_item')
        self.assertEqual(mock_bible_import.call_count, 2, '2 bible verses submitted for parsing')

    def test_other_bible_is_used_when_bible_gui_form_is_blank(self):
        """
        Test that an other bible is used when the GUI has an empty string for current selected bible
        """
        # GIVEN: An SelectPlanForm instance with airplane mode enabled, resources available,
        # mocked out "on_new_service_clicked"
        with patch('PyQt5.QtWidgets.QDialog.exec'), \
                patch('openlp.plugins.planningcenter.lib.songimport.PlanningCenterSongImport.finish'), \
                patch('openlp.plugins.planningcenter.lib.customimport.CustomSlide'), \
                patch('openlp.plugins.planningcenter.forms.selectplanform.parse_reference') as mock_bible_import, \
                patch('openlp.plugins.planningcenter.forms.selectplanform.date') as mock_date:
            # need to always return 9/29/2019 for date.today()
            mock_date.today.return_value = date(2019, 9, 29)
            mock_date.side_effect = lambda *args, **kw: date(*args, **kw)
            mock_bibles = {}
            mock_bibles['other_bible'] = MagicMock()
            Registry().register('service_manager', MagicMock())
            Registry().register('plugin_manager', MagicMock())
            Registry().register('songs', MagicMock())
            Registry().register('bibles', MagicMock())
            Registry().register('custom', MagicMock())
            self.form.exec()
            # WHEN: The Service Type combo is set to index 1 and the Select Plan combo box
            # is set to index 1 and the "Import New" button is clicked
            self.form.service_type_combo_box.setCurrentIndex(1)
            QtTest.QTest.mouseClick(self.form.import_as_new_button, QtCore.Qt.LeftButton)
        # THEN: There should be 2 bible verse parse attempts
        self.assertEqual(mock_bible_import.call_count, 2, '2 bible verses submitted for parsing')

    def _create_mock_action(self, name, **kwargs):
        """
        Create a fake action with some "real" attributes for Service Manager
        """
        action = QtWidgets.QAction(self.service_manager)
        action.setObjectName(name)
        if kwargs.get('triggers'):
            action.triggered.connect(kwargs.pop('triggers'))
        self.service_manager.toolbar.actions[name] = action
        return action

    @skip("fails to run when executed with all other openlp tests.  awaiting pytest fixtures to enable again")
    def test_less_mocking_service_refreshed_when_refresh_button_clicked_test(self):
        """
        Test that a service is refreshed when the "Refresh Service" button is clicked
        """
        # GIVEN: An SelectPlanForm instance with airplane mode enabled, resources available,
        # mocked out "on_new_service_clicked"
        with patch('PyQt5.QtWidgets.QDialog.exec'), \
                patch('openlp.plugins.planningcenter.forms.selectplanform.date') as mock_date:
            # need to always return 9/29/2019 for date.today()
            mock_date.today.return_value = date(2019, 9, 29)
            mock_date.side_effect = lambda *args, **kw: date(*args, **kw)
            # init ServiceManager
            Registry().register('plugin_manager', MagicMock())
            Registry().register('application', MagicMock())
            Registry().register('renderer', MagicMock())
            self.service_manager = ServiceManager()
            self.service_manager.setup_ui(self.service_manager)
            # init songs plugin
            with patch('openlp.plugins.songs.lib.mediaitem.EditSongForm'), \
                    patch('openlp.plugins.custom.lib.mediaitem.EditCustomForm'), \
                    patch('openlp.core.lib.mediamanageritem.create_widget_action'), \
                    patch('openlp.core.widgets.toolbar.create_widget_action'):
                # init songs plugin
                songs_plugin = SongsPlugin()
                song_media_item = SongMediaItem(None, songs_plugin)
                song_media_item.search_text_edit = MagicMock()
                song_media_item.initialise()
                # init custom plugin
                custom_plugin = CustomPlugin()
                CustomMediaItem(None, custom_plugin)
                # init bible plugin
                bible_plugin = BiblePlugin()
                bible_media_item = BibleMediaItem(None, bible_plugin)
                bible_media_item.build_display_results = MagicMock()
                self.form.exec()
            # WHEN:
            # The Service Type combo is set to index 1 and "Import New" button is clicked
            self.form.service_type_combo_box.setCurrentIndex(1)
            QtTest.QTest.mouseClick(self.form.import_as_new_button, QtCore.Qt.LeftButton)
            # make changes to the now imported service items
            # first, for serviceitem[0] update last_updated in xml_string and change "sweet" to "sublime"
            old_match = re.search('modifiedDate="(.+?)Z*"',
                                  self.service_manager.service_items[0]['service_item'].xml_version)
            old_string = old_match.group(1)
            now_string = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
            self.service_manager.service_items[0]['service_item'].xml_version = \
                self.service_manager.service_items[0]['service_item'].xml_version.replace(old_string, now_string)
            self.service_manager.service_items[0]['service_item'].xml_version = \
                self.service_manager.service_items[0]['service_item'].xml_version.replace("sweet", "sublime")
            # second, add the word modified to the slide text for serviceitem[1]
            self.service_manager.service_items[1]['service_item'].slides[0]['text'] = \
                self.service_manager.service_items[1]['service_item'].slides[0]['text'].replace("Test", "Modified Test")
            # third, delete serviceitems[2] and serviceitem[3]
            del self.service_manager.service_items[3]
            del self.service_manager.service_items[2]
            # last, draw the form again and request refresh
            self.form.exec()
            self.form.service_type_combo_box.setCurrentIndex(1)
            QtTest.QTest.mouseClick(self.form.update_existing_button, QtCore.Qt.LeftButton)
        # THEN:
        # There should be 4 service items added
        self.assertEqual(len(self.service_manager.service_items), 5, '5 items should be in the ServiceManager')
        # Amazon Grace should still include sublime
        self.assertTrue('sublime' in self.service_manager.service_items[0]['service_item'].xml_version)
        # Slides in service_item[1] should still contain the word "Modified"
        self.assertTrue('Modified' in self.service_manager.service_items[1]['service_item'].slides[0]['text'])
