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
Package to test the openlp.core.lib.pluginmanager package.
"""
import shutil
import sys
import pytest
from pathlib import Path
from tempfile import mkdtemp
from unittest import TestCase, skip
from unittest.mock import MagicMock, patch

from PyQt5 import QtWidgets

from openlp.core.state import State
from openlp.core.common.platform import is_win
from openlp.core.common.registry import Registry
from openlp.core.common.settings import Settings
from openlp.core.lib.plugin import PluginStatus
from openlp.core.lib.pluginmanager import PluginManager
from tests.helpers.testmixin import TestMixin


@pytest.fixture()
def plugin_manager_env(registry, state):
    mocked_main_window = MagicMock()
    mocked_main_window.file_import_menu.return_value = None
    mocked_main_window.file_export_menu.return_value = None
    mocked_main_window.file_export_menu.return_value = None
    mocked_settings_form = MagicMock()
    Registry().register('service_list', MagicMock())
    Registry().register('main_window', mocked_main_window)
    Registry().register('settings_form', mocked_settings_form)
    Registry().register('settings', MagicMock())


def test_bootstrap_initialise(settings, state):
    """
    Test the PluginManager.bootstrap_initialise() method
    """
    # GIVEN: A plugin manager with some mocked out methods
    State().add_service('mediacontroller', 0)
    State().update_pre_conditions('mediacontroller', True)
    manager = PluginManager()

    with patch.object(manager, 'hook_settings_tabs') as mocked_hook_settings_tabs, \
            patch.object(manager, 'hook_media_manager') as mocked_hook_media_manager, \
            patch.object(manager, 'hook_import_menu') as mocked_hook_import_menu, \
            patch.object(manager, 'hook_export_menu') as mocked_hook_export_menu, \
            patch.object(manager, 'hook_tools_menu') as mocked_hook_tools_menu, \
            patch.object(manager, 'initialise_plugins') as mocked_initialise_plugins:
        # WHEN: bootstrap_initialise() is called
        manager.bootstrap_initialise()
        manager.bootstrap_post_set_up()

    # THEN: The hook methods should have been called
    mocked_hook_settings_tabs.assert_called_with()
    mocked_hook_media_manager.assert_called_with()
    mocked_hook_import_menu.assert_called_with()
    mocked_hook_export_menu.assert_called_with()
    mocked_hook_tools_menu.assert_called_with()
    mocked_initialise_plugins.assert_called_with()


def test_hook_media_manager_with_disabled_plugin(registry, state):
    """
    Test running the hook_media_manager() method with a disabled plugin
    """
    # GIVEN: A PluginManager instance and a list with a mocked up plugin whose status is set to Disabled
    mocked_plugin = MagicMock()
    mocked_plugin.status = PluginStatus.Disabled
    plugin_manager = PluginManager()
    Registry().register('mock_plugin', mocked_plugin)
    State().add_service("mock", 1, is_plugin=True, status=PluginStatus.Disabled)
    State().flush_preconditions()

    # WHEN: We run hook_media_manager()
    plugin_manager.hook_media_manager()

    # THEN: The create_media_manager_item() method should have been called
    assert 0 == mocked_plugin.create_media_manager_item.call_count, \
        'The create_media_manager_item() method should not have been called.'


def test_hook_media_manager_with_active_plugin(registry, state):
    """
    Test running the hook_media_manager() method with an active plugin
    """
    # GIVEN: A PluginManager instance and a list with a mocked up plugin whose status is set to Active
    mocked_plugin = MagicMock()
    mocked_plugin.status = PluginStatus.Active
    plugin_manager = PluginManager()
    Registry().register('mock_plugin', mocked_plugin)
    State().add_service("mock", 1, is_plugin=True, status=PluginStatus.Active)
    State().flush_preconditions()

    # WHEN: We run hook_media_manager()
    plugin_manager.hook_media_manager()

    # THEN: The create_media_manager_item() method should have been called
    mocked_plugin.create_media_manager_item.assert_called_with()


def test_hook_settings_tabs_with_disabled_plugin_and_no_form(registry, state):
    """
    Test running the hook_settings_tabs() method with a disabled plugin and no form
    """
    # GIVEN: A PluginManager instance and a list with a mocked up plugin whose status is set to Disabled
    mocked_plugin = MagicMock()
    mocked_plugin.status = PluginStatus.Disabled
    plugin_manager = PluginManager()
    Registry().register('mock_plugin', mocked_plugin)
    State().add_service("mock", 1, is_plugin=True, status=PluginStatus.Active)
    State().flush_preconditions()

    # WHEN: We run hook_settings_tabs()
    plugin_manager.hook_settings_tabs()

    # THEN: The hook_settings_tabs() method should have been called
    assert 0 == mocked_plugin.create_media_manager_item.call_count, \
        'The create_media_manager_item() method should not have been called.'


def test_hook_settings_tabs_with_disabled_plugin_and_mocked_form(registry, state):
    """
    Test running the hook_settings_tabs() method with a disabled plugin and a mocked form
    """
    # GIVEN: A PluginManager instance and a list with a mocked up plugin whose status is set to Disabled
    mocked_plugin = MagicMock()
    mocked_plugin.status = PluginStatus.Disabled
    plugin_manager = PluginManager()
    Registry().register('mock_plugin', mocked_plugin)
    mocked_settings_form = MagicMock()
    # Replace the autoloaded plugin with the version for testing in real code this would error
    mocked_settings_form.plugin_manager = plugin_manager
    State().add_service("mock", 1, is_plugin=True, status=PluginStatus.Active)
    State().flush_preconditions()

    # WHEN: We run hook_settings_tabs()
    plugin_manager.hook_settings_tabs()

    # THEN: The create_settings_tab() method should not have been called, but the plugins lists should be the same
    assert 0 == mocked_plugin.create_settings_tab.call_count, \
        'The create_media_manager_item() method should not have been called.'


def test_hook_settings_tabs_with_active_plugin_and_mocked_form(registry, state):
    """
    Test running the hook_settings_tabs() method with an active plugin and a mocked settings form
    """
    # GIVEN: A PluginManager instance and a list with a mocked up plugin whose status is set to Active
    mocked_plugin = MagicMock()
    mocked_plugin.status = PluginStatus.Active
    plugin_manager = PluginManager()
    Registry().register('mock_plugin', mocked_plugin)
    mocked_settings_form = MagicMock()
    # Replace the autoloaded plugin with the version for testing in real code this would error
    mocked_settings_form.plugin_manager = plugin_manager
    State().add_service("mock", 1, is_plugin=True, status=PluginStatus.Active)
    State().flush_preconditions()

    # WHEN: We run hook_settings_tabs()
    plugin_manager.hook_settings_tabs()

    # THEN: The create_media_manager_item() method should have been called with the mocked settings form
    assert 1 == mocked_plugin.create_settings_tab.call_count, \
        'The create_media_manager_item() method should have been called once.'


def test_hook_settings_tabs_with_active_plugin_and_no_form(plugin_manager_env):
    """
    Test running the hook_settings_tabs() method with an active plugin and no settings form
    """
    # GIVEN: A PluginManager instance and a list with a mocked up plugin whose status is set to Active
    mocked_plugin = MagicMock()
    mocked_plugin.status = PluginStatus.Active
    plugin_manager = PluginManager()
    Registry().register('mock_plugin', mocked_plugin)
    State().add_service("mock", 1, is_plugin=True, status=PluginStatus.Active)
    State().flush_preconditions()

    # WHEN: We run hook_settings_tabs()
    plugin_manager.hook_settings_tabs()

    # THEN: The create_settings_tab() method should have been called
    mocked_plugin.create_settings_tab.assert_called_with(Registry().get('settings_form'))


def test_hook_import_menu_with_disabled_plugin(registry, state):
    """
    Test running the hook_import_menu() method with a disabled plugin
    """
    # GIVEN: A PluginManager instance and a list with a mocked up plugin whose status is set to Disabled
    mocked_plugin = MagicMock()
    mocked_plugin.status = PluginStatus.Disabled
    plugin_manager = PluginManager()
    Registry().register('mock_plugin', mocked_plugin)
    State().add_service("mock", 1, is_plugin=True, status=PluginStatus.Active)
    State().flush_preconditions()

    # WHEN: We run hook_import_menu()
    plugin_manager.hook_import_menu()

    # THEN: The create_media_manager_item() method should have been called
    assert 0 == mocked_plugin.add_import_menu_item.call_count, \
        'The add_import_menu_item() method should not have been called.'


def test_hook_import_menu_with_active_plugin(plugin_manager_env):
    """
    Test running the hook_import_menu() method with an active plugin
    """
    # GIVEN: A PluginManager instance and a list with a mocked up plugin whose status is set to Active
    mocked_plugin = MagicMock()
    mocked_plugin.status = PluginStatus.Active
    plugin_manager = PluginManager()
    Registry().register('mock_plugin', mocked_plugin)
    State().add_service("mock", 1, is_plugin=True, status=PluginStatus.Active)
    State().flush_preconditions()

    # WHEN: We run hook_import_menu()
    plugin_manager.hook_import_menu()

    # THEN: The add_import_menu_item() method should have been called
    mocked_plugin.add_import_menu_item.assert_called_with(Registry().get('main_window').file_import_menu)


def test_hook_export_menu_with_disabled_plugin(registry, state):
    """
    Test running the hook_export_menu() method with a disabled plugin
    """
    # GIVEN: A PluginManager instance and a list with a mocked up plugin whose status is set to Disabled
    mocked_plugin = MagicMock()
    mocked_plugin.status = PluginStatus.Disabled
    plugin_manager = PluginManager()
    Registry().register('mock_plugin', mocked_plugin)
    State().add_service("mock", 1, is_plugin=True, status=PluginStatus.Active)
    State().flush_preconditions()

    # WHEN: We run hook_export_menu()
    plugin_manager.hook_export_menu()

    # THEN: The add_export_menu_item() method should not have been called
    assert 0 == mocked_plugin.add_export_menu_item.call_count, \
        'The add_export_menu_item() method should not have been called.'


def test_hook_export_menu_with_active_plugin(plugin_manager_env):
    """
    Test running the hook_export_menu() method with an active plugin
    """
    # GIVEN: A PluginManager instance and a list with a mocked up plugin whose status is set to Active
    mocked_plugin = MagicMock()
    mocked_plugin.status = PluginStatus.Active
    plugin_manager = PluginManager()
    Registry().register('mock_plugin', mocked_plugin)
    State().add_service("mock", 1, is_plugin=True, status=PluginStatus.Active)
    State().flush_preconditions()

    # WHEN: We run hook_export_menu()
    plugin_manager.hook_export_menu()

    # THEN: The add_export_menu_item() method should have been called
    mocked_plugin.add_export_menu_item.assert_called_with(Registry().get('main_window').file_export_menu)


def test_hook_upgrade_plugin_settings_with_disabled_plugin(registry, state):
    """
    Test running the hook_upgrade_plugin_settings() method with a disabled plugin
    """
    # GIVEN: A PluginManager instance and a list with a mocked up plugin whose status is set to Disabled
    mocked_plugin = MagicMock()
    mocked_plugin.status = PluginStatus.Disabled
    plugin_manager = PluginManager()
    Registry().register('mock_plugin', mocked_plugin)
    State().add_service("mock", 1, is_plugin=True, status=PluginStatus.Active)
    State().flush_preconditions()
    settings = Settings()

    # WHEN: We run hook_upgrade_plugin_settings()
    plugin_manager.hook_upgrade_plugin_settings(settings)

    # THEN: The upgrade_settings() method should not have been called
    assert 0 == mocked_plugin.upgrade_settings.call_count, \
        'The upgrade_settings() method should not have been called.'


def test_hook_upgrade_plugin_settings_with_active_plugin(registry, state):
    """
    Test running the hook_upgrade_plugin_settings() method with an active plugin
    """
    # GIVEN: A PluginManager instance and a list with a mocked up plugin whose status is set to Active
    mocked_plugin = MagicMock()
    mocked_plugin.status = PluginStatus.Active
    plugin_manager = PluginManager()
    Registry().register('mock_plugin', mocked_plugin)
    State().add_service("mock", 1, is_plugin=True, status=PluginStatus.Active)
    State().flush_preconditions()
    settings = Settings()

    # WHEN: We run hook_upgrade_plugin_settings()
    plugin_manager.hook_upgrade_plugin_settings(settings)

    # THEN: The add_export_menu_item() method should have been called
    mocked_plugin.upgrade_settings.assert_called_with(settings)


def test_hook_tools_menu_with_disabled_plugin(registry, state):
    """
    Test running the hook_tools_menu() method with a disabled plugin
    """
    # GIVEN: A PluginManager instance and a list with a mocked up plugin whose status is set to Disabled
    mocked_plugin = MagicMock()
    mocked_plugin.status = PluginStatus.Disabled
    plugin_manager = PluginManager()
    Registry().register('mock_plugin', mocked_plugin)
    State().add_service("mock", 1, is_plugin=True, status=PluginStatus.Active)
    State().flush_preconditions()

    # WHEN: We run hook_tools_menu()
    plugin_manager.hook_tools_menu()

    # THEN: The add_tools_menu_item() method should have been called
    assert 0 == mocked_plugin.add_tools_menu_item.call_count, \
        'The add_tools_menu_item() method should not have been called.'


def test_hook_tools_menu_with_active_plugin(plugin_manager_env):
    """
    Test running the hook_tools_menu() method with an active plugin
    """
    # GIVEN: A PluginManager instance and a list with a mocked up plugin whose status is set to Active
    mocked_plugin = MagicMock()
    mocked_plugin.status = PluginStatus.Active
    plugin_manager = PluginManager()
    Registry().register('mock_plugin', mocked_plugin)
    State().add_service("mock", 1, is_plugin=True, status=PluginStatus.Active)
    State().flush_preconditions()

    # WHEN: We run hook_tools_menu()
    plugin_manager.hook_tools_menu()

    # THEN: The add_tools_menu_item() method should have been called
    mocked_plugin.add_tools_menu_item.assert_called_with(Registry().get('main_window').tools_menu)


def test_initialise_plugins_with_disabled_plugin(registry, state):
    """
    Test running the initialise_plugins() method with a disabled plugin
    """
    # GIVEN: A PluginManager instance and a list with a mocked up plugin whose status is set to Disabled
    mocked_plugin = MagicMock()
    mocked_plugin.status = PluginStatus.Disabled
    mocked_plugin.is_active.return_value = False
    plugin_manager = PluginManager()
    Registry().register('mock_plugin', mocked_plugin)
    State().add_service("mock", 1, is_plugin=True, status=PluginStatus.Active)
    State().flush_preconditions()

    # WHEN: We run initialise_plugins()
    plugin_manager.initialise_plugins()

    # THEN: The is_active() method should have been called, and initialise() method should NOT have been called
    mocked_plugin.is_active.assert_called_with()
    assert 0 == mocked_plugin.initialise.call_count, 'The initialise() method should not have been called.'


def test_initialise_plugins_with_active_plugin(registry, state):
    """
    Test running the initialise_plugins() method with an active plugin
    """
    # GIVEN: A PluginManager instance and a list with a mocked up plugin whose status is set to Active
    mocked_plugin = MagicMock()
    mocked_plugin.status = PluginStatus.Active
    mocked_plugin.is_active.return_value = True
    plugin_manager = PluginManager()
    Registry().register('mock_plugin', mocked_plugin)
    State().add_service("mock", 1, is_plugin=True, status=PluginStatus.Active)
    State().flush_preconditions()

    # WHEN: We run initialise_plugins()
    plugin_manager.initialise_plugins()

    # THEN: The is_active() and initialise() methods should have been called
    mocked_plugin.is_active.assert_called_with()
    mocked_plugin.initialise.assert_called_with()


def test_finalise_plugins_with_disabled_plugin(registry, state):
    """
    Test running the finalise_plugins() method with a disabled plugin
    """
    # GIVEN: A PluginManager instance and a list with a mocked up plugin whose status is set to Disabled
    mocked_plugin = MagicMock()
    mocked_plugin.status = PluginStatus.Disabled
    mocked_plugin.is_active.return_value = False
    plugin_manager = PluginManager()
    Registry().register('mock_plugin', mocked_plugin)
    State().add_service("mock", 1, is_plugin=True, status=PluginStatus.Active)
    State().flush_preconditions()

    # WHEN: We run finalise_plugins()
    plugin_manager.finalise_plugins()

    # THEN: The is_active() method should have been called, and initialise() method should NOT have been called
    mocked_plugin.is_active.assert_called_with()
    assert 0 == mocked_plugin.finalise.call_count, 'The finalise() method should not have been called.'


def test_finalise_plugins_with_active_plugin(registry, state):
    """
    Test running the finalise_plugins() method with an active plugin
    """
    # GIVEN: A PluginManager instance and a list with a mocked up plugin whose status is set to Active
    mocked_plugin = MagicMock()
    mocked_plugin.status = PluginStatus.Active
    mocked_plugin.is_active.return_value = True
    plugin_manager = PluginManager()
    Registry().register('mock_plugin', mocked_plugin)
    State().add_service("mock", 1, is_plugin=True, status=PluginStatus.Active)
    State().flush_preconditions()

    # WHEN: We run finalise_plugins()
    plugin_manager.finalise_plugins()

    # THEN: The is_active() and finalise() methods should have been called
    mocked_plugin.is_active.assert_called_with()
    mocked_plugin.finalise.assert_called_with()


def test_get_plugin_by_name_does_not_exist(registry, state):
    """
    Test running the get_plugin_by_name() method to find a plugin that does not exist
    """
    # GIVEN: A PluginManager instance and a list with a mocked up plugin whose status is set to Active
    mocked_plugin = MagicMock()
    mocked_plugin.name = 'Mocked Plugin'
    plugin_manager = PluginManager()
    Registry().register('mock_plugin', mocked_plugin)
    State().add_service("mock", 1, is_plugin=True, status=PluginStatus.Active)
    State().flush_preconditions()

    # WHEN: We run finalise_plugins()
    result = plugin_manager.get_plugin_by_name('Missing Plugin')

    # THEN: The is_active() and finalise() methods should have been called
    assert result is None, 'The result for get_plugin_by_name should be None'


def test_get_plugin_by_name_exists(registry, state):
    """
    Test running the get_plugin_by_name() method to find a plugin that exists
    """
    # GIVEN: A PluginManager instance and a list with a mocked up plugin whose status is set to Active
    mocked_plugin = MagicMock()
    mocked_plugin.name = 'Mocked Plugin'
    plugin_manager = PluginManager()
    Registry().register('mock_plugin', mocked_plugin)
    State().add_service("mock", 1, is_plugin=True, status=PluginStatus.Active)
    State().flush_preconditions()

    # WHEN: We run finalise_plugins()
    result = plugin_manager.get_plugin_by_name('Mocked Plugin')

    # THEN: The is_active() and finalise() methods should have been called
    assert result == mocked_plugin, 'The result for get_plugin_by_name should be the mocked plugin'


def test_get_plugin_by_name_disabled(registry, state):
    """
    Test running the get_plugin_by_name() method to find a plugin that is disabled
    """
    # GIVEN: A PluginManager instance and a list with a mocked up plugin whose status is set to Active
    mocked_plugin = MagicMock()
    mocked_plugin.name = 'Mocked Plugin'
    plugin_manager = PluginManager()
    Registry().register('mock_plugin', mocked_plugin)
    State().add_service("mock", 1, is_plugin=True, status=PluginStatus.Disabled)
    State().flush_preconditions()

    # WHEN: We run finalise_plugins()
    result = plugin_manager.get_plugin_by_name('Mocked Plugin')

    # THEN: The is_active() and finalise() methods should have been called
    assert result == mocked_plugin, 'The result for get_plugin_by_name should be the mocked plugin'


def test_new_service_created_with_disabled_plugin(registry, state):
    """
    Test running the new_service_created() method with a disabled plugin
    """
    # GIVEN: A PluginManager instance and a list with a mocked up plugin whose status is set to Disabled
    mocked_plugin = MagicMock()
    mocked_plugin.status = PluginStatus.Disabled
    mocked_plugin.is_active.return_value = False
    plugin_manager = PluginManager()
    Registry().register('mock_plugin', mocked_plugin)
    State().add_service("mock", 1, is_plugin=True, status=PluginStatus.Active)
    State().flush_preconditions()

    # WHEN: We run finalise_plugins()
    plugin_manager.new_service_created()

    # THEN: The isActive() method should have been called, and initialise() method should NOT have been called
    mocked_plugin.is_active.assert_called_with()
    assert 0 == mocked_plugin.new_service_created.call_count, \
        'The new_service_created() method should not have been called.'


def test_new_service_created_with_active_plugin(registry, state):
    """
    Test running the new_service_created() method with an active plugin
    """
    # GIVEN: A PluginManager instance and a list with a mocked up plugin whose status is set to Active
    mocked_plugin = MagicMock()
    mocked_plugin.status = PluginStatus.Active
    mocked_plugin.is_active.return_value = True
    plugin_manager = PluginManager()
    Registry().register('mock_plugin', mocked_plugin)
    State().add_service("mock", 1, is_plugin=True, status=PluginStatus.Active)
    State().flush_preconditions()

    # WHEN: We run new_service_created()
    plugin_manager.new_service_created()

    # THEN: The is_active() and finalise() methods should have been called
    mocked_plugin.is_active.assert_called_with()
    mocked_plugin.new_service_created.assert_called_with()


class TestPluginManager(TestCase, TestMixin):
    """
    Test the PluginManager class
    """

    def setUp(self):
        """
        Some pre-test setup required.
        """
        self.setup_application()
        self.build_settings()
        self.temp_dir_path = Path(mkdtemp('openlp'))
        Settings().setValue('advanced/data path', self.temp_dir_path)
        Registry.create()
        Registry().register('service_list', MagicMock())
        self.main_window = QtWidgets.QMainWindow()
        Registry().register('main_window', self.main_window)

    def tearDown(self):
        Settings().remove('advanced/data path')
        self.destroy_settings()
        del self.main_window
        # On windows we need to manually garbage collect to close sqlalchemy files
        # to avoid errors when temporary files are deleted.
        if is_win():
            import gc
            gc.collect()
        shutil.rmtree(self.temp_dir_path)

    @skip
    # This test is broken but totally unable to debug it.
    @patch('openlp.plugins.songusage.songusageplugin.Manager')
    @patch('openlp.plugins.songs.songsplugin.Manager')
    @patch('openlp.plugins.images.imageplugin.Manager')
    @patch('openlp.plugins.custom.customplugin.Manager')
    @patch('openlp.plugins.alerts.alertsplugin.Manager')
    def test_find_plugins(self, mocked_is1, mocked_is2, mocked_is3, mocked_is4, mocked_is5):
        """
        Test the find_plugins() method to ensure it imports the correct plugins
        """
        # GIVEN: A plugin manager
        plugin_manager = PluginManager()
        plugin_manager.bootstrap_initialise()

        # WHEN: We mock out sys.platform to make it return "darwin" and then find the plugins
        old_platform = sys.platform
        sys.platform = 'darwin'
        sys.platform = old_platform

        # THEN: We should find the "Songs", "Bibles", etc in the plugins list
        plugin_names = [plugin.name for plugin in State().list_plugins()]
        assert 'songs' in plugin_names, 'There should be a "songs" plugin'
        assert 'bibles' in plugin_names, 'There should be a "bibles" plugin'
        assert 'presentations' in plugin_names, 'There should be a "presentations" plugin'
        assert 'images' in plugin_names, 'There should be a "images" plugin'
        assert 'media' in plugin_names, 'There should be a "media" plugin'
        assert 'custom' in plugin_names, 'There should be a "custom" plugin'
        assert 'songusage' in plugin_names, 'There should be a "songusage" plugin'
        assert 'alerts' in plugin_names, 'There should be a "alerts" plugin'
