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
Package to test the openlp.core.ui.slidecontroller package.
"""
from pathlib import Path
from unittest import TestCase
from unittest.mock import MagicMock, patch

import pytest
from PyQt5 import QtCore, QtGui, QtWidgets

from openlp.core.common import ThemeLevel
from openlp.core.common.registry import Registry
from openlp.core.common.settings import Settings
from openlp.core.common.enum import ServiceItemType
from openlp.core.lib.serviceitem import ItemCapabilities, ServiceItem
from openlp.core.ui.servicemanager import ServiceManager, ServiceManagerList
from openlp.core.widgets.toolbar import OpenLPToolbar

from tests.helpers.testmixin import TestMixin


def test_initial_service_manager(settings):
    """
    Test the initial of service manager.
    """
    # GIVEN: A new service manager instance.
    ServiceManager(None)
    # WHEN: the default service manager is built.
    # THEN: The the controller should be registered in the registry.
    assert Registry().get('service_manager') is not None, 'The base service manager should be registered'


def test_new_file(registry):
    """Test the new_file() method"""
    # GIVEN: A service manager
    mocked_settings = MagicMock()
    mocked_plugin_manager = MagicMock()
    mocked_main_window = MagicMock()
    mocked_slide_controller = MagicMock()
    registry.register('settings', mocked_settings)
    registry.register('plugin_manager', mocked_plugin_manager)
    registry.register('main_window', mocked_main_window)
    registry.register('live_controller', mocked_slide_controller)
    service_manager = ServiceManager(None)
    service_manager.service_items = [MagicMock(), MagicMock()]
    service_manager.service_id = 5
    service_manager._service_path = 'service.osz'
    service_manager._modified = True
    service_manager.service_manager_list = MagicMock()
    service_manager.plugin_manager.new_service_created = MagicMock()

    # WHEN: new_file() is called
    service_manager.new_file()

    # THEN: Everything should be correct
    service_manager.service_manager_list.clear.assert_called_once_with()
    assert service_manager.service_items == [], 'The list of service items should be blank'
    assert service_manager._service_path is None, 'The file_name should be None'
    assert service_manager.service_id == 7, 'The service id should be 6'
    mocked_settings.setValue.assert_called_with('servicemanager/last file', None)
    mocked_plugin_manager.new_service_created.assert_called_once_with()
    assert mocked_slide_controller.slide_count == 0, 'Slide count should be zero'


def test_create_basic_service(settings):
    """
    Test the create basic service array
    """
    # GIVEN: A new service manager instance.
    service_manager = ServiceManager(None)
    # WHEN: when the basic service array is created.
    service_manager._save_lite = False
    service_manager.service_theme = 'test_theme'
    service = service_manager.create_basic_service()[0]
    # THEN: The controller should be registered in the registry.
    assert service is not None, 'The base service should be created'
    assert service['openlp_core']['service-theme'] == 'test_theme', 'The test theme should be saved'
    assert service['openlp_core']['lite-service'] is False, 'The lite service should be saved'


def test_is_modified(settings):
    """
    Test the is_modified() method
    """
    # GIVEN: A service manager with the self._modified set
    service_manager = ServiceManager(None)
    service_manager._modified = True

    # WHEN: is_modified is called
    result = service_manager.is_modified()

    # THEN: The result should be True
    assert result is True, 'is_modified should return True'


def test_supported_suffixes(settings):
    """
    Test the create basic service array
    """
    # GIVEN: A new service manager instance.
    service_manager = ServiceManager(None)
    # WHEN: a suffix is added as an individual or a list.
    service_manager.supported_suffixes('txt')
    service_manager.supported_suffixes(['pptx', 'ppt'])
    # THEN: The suffixes should be available to test.
    assert 'txt' in service_manager.suffixes, 'The suffix txt should be in the list'
    assert 'ppt' in service_manager.suffixes, 'The suffix ppt should be in the list'
    assert 'pptx' in service_manager.suffixes, 'The suffix pptx should be in the list'


def test_reset_supported_suffixes(settings):
    """
    Test the create basic service array
    """
    # GIVEN: A new service manager instance with some supported suffixes
    service_manager = ServiceManager(None)
    service_manager.suffixes = ['mp3', 'aac', 'wav', 'flac']

    # WHEN: reset_supported_suffixes() is called
    service_manager.reset_supported_suffixes()

    # THEN: The suffixes should be cleared out
    assert service_manager.suffixes == [], 'There should not be any suffixes'


def test_build_context_menu(settings):
    """
    Test the creation of a context menu from a null service item.
    """
    # GIVEN: A new service manager instance and a default service item.
    service_manager = ServiceManager(None)
    item = MagicMock()
    item.parent.return_value = False
    item.data.return_value = 0
    service_manager.service_manager_list = MagicMock()
    service_manager.service_manager_list.itemAt.return_value = item
    service_item = ServiceItem(None)
    service_manager.service_items.insert(1, {'service_item': service_item})
    service_manager.edit_action = MagicMock()
    service_manager.rename_action = MagicMock()
    service_manager.create_custom_action = MagicMock()
    service_manager.maintain_action = MagicMock()
    service_manager.notes_action = MagicMock()
    service_manager.time_action = MagicMock()
    service_manager.auto_start_action = MagicMock()
    service_manager.auto_play_slides_menu = MagicMock()
    service_manager.auto_play_slides_once = MagicMock()
    service_manager.auto_play_slides_loop = MagicMock()
    service_manager.timed_slide_interval = MagicMock()
    service_manager.theme_menu = MagicMock()
    service_manager.menu = MagicMock()
    # WHEN I define a context menu
    service_manager.context_menu(1)
    # THEN the following calls should have occurred.
    assert service_manager.edit_action.setVisible.call_count == 1, 'Should have been called once'
    assert service_manager.rename_action.setVisible.call_count == 1, 'Should have been called once'
    assert service_manager.create_custom_action.setVisible.call_count == 1, 'Should have been called once'
    assert service_manager.maintain_action.setVisible.call_count == 1, 'Should have been called once'
    assert service_manager.notes_action.setVisible.call_count == 1, 'Should have been called once'
    assert service_manager.time_action.setVisible.call_count == 1, 'Should have been called once'
    assert service_manager.auto_start_action.setVisible.call_count == 1, 'Should have been called once'
    assert service_manager.auto_play_slides_menu.menuAction().setVisible.call_count == 1, \
        'Should have been called once'
    assert service_manager.auto_play_slides_once.setChecked.call_count == 0, 'Should not be called'
    assert service_manager.auto_play_slides_loop.setChecked.call_count == 0, 'Should not be called'
    assert service_manager.timed_slide_interval.setChecked.call_count == 0, 'Should not be called'
    assert service_manager.theme_menu.menuAction().setVisible.call_count == 1, \
        'Should have been called once'


def test_build_song_context_menu(settings, state):
    """
    Test the creation of a context menu from service item of type text from Songs.
    """
    # GIVEN: A new service manager instance and a default service item.
    mocked_renderer = MagicMock()
    mocked_renderer.theme_level = ThemeLevel.Song
    Registry().register('plugin_manager', MagicMock())
    Registry().register('renderer', mocked_renderer)
    service_manager = ServiceManager(None)
    item = MagicMock()
    item.parent.return_value = False
    item.data.return_value = 0
    service_manager.service_manager_list = MagicMock()
    service_manager.service_manager_list.itemAt.return_value = item
    service_item = ServiceItem(None)
    for capability in [ItemCapabilities.CanEdit, ItemCapabilities.CanPreview, ItemCapabilities.CanLoop,
                       ItemCapabilities.OnLoadUpdate, ItemCapabilities.AddIfNewItem,
                       ItemCapabilities.CanSoftBreak]:
        service_item.add_capability(capability)
    service_item.service_item_type = ServiceItemType.Text
    service_item.edit_id = 1
    service_item._display_slides = []
    service_item._display_slides.append(MagicMock())
    service_manager.service_items.insert(1, {'service_item': service_item})
    service_manager.edit_action = MagicMock()
    service_manager.rename_action = MagicMock()
    service_manager.create_custom_action = MagicMock()
    service_manager.maintain_action = MagicMock()
    service_manager.notes_action = MagicMock()
    service_manager.time_action = MagicMock()
    service_manager.auto_start_action = MagicMock()
    service_manager.auto_play_slides_menu = MagicMock()
    service_manager.auto_play_slides_once = MagicMock()
    service_manager.auto_play_slides_loop = MagicMock()
    service_manager.timed_slide_interval = MagicMock()
    service_manager.theme_menu = MagicMock()
    service_manager.menu = MagicMock()
    # WHEN I define a context menu
    service_manager.context_menu(1)
    # THEN the following calls should have occurred.
    assert service_manager.edit_action.setVisible.call_count == 2, 'Should have be called twice'
    assert service_manager.rename_action.setVisible.call_count == 1, 'Should have be called once'
    assert service_manager.create_custom_action.setVisible.call_count == 1, 'Should have be called once'
    assert service_manager.maintain_action.setVisible.call_count == 1, 'Should have be called once'
    assert service_manager.notes_action.setVisible.call_count == 1, 'Should have be called once'
    assert service_manager.time_action.setVisible.call_count == 1, 'Should have be called once'
    assert service_manager.auto_start_action.setVisible.call_count == 1, 'Should have be called once'
    assert service_manager.auto_play_slides_menu.menuAction().setVisible.call_count == 1, \
        'Should have be called once'
    assert service_manager.auto_play_slides_once.setChecked.call_count == 0, 'Should not be called'
    assert service_manager.auto_play_slides_loop.setChecked.call_count == 0, 'Should not be called'
    assert service_manager.timed_slide_interval.setChecked.call_count == 0, 'Should not be called'
    assert service_manager.theme_menu.menuAction().setVisible.call_count == 2, \
        'Should have be called twice'
    # THEN we add a 2nd display frame
    service_item._display_slides.append(MagicMock())
    service_manager.context_menu(1)
    # THEN the following additional calls should have occurred.
    assert service_manager.auto_play_slides_menu.menuAction().setVisible.call_count == 2, \
        'Should have be called twice'
    assert service_manager.auto_play_slides_once.setChecked.call_count == 1, 'Should have be called once'
    assert service_manager.auto_play_slides_loop.setChecked.call_count == 1, 'Should have be called once'
    assert service_manager.timed_slide_interval.setChecked.call_count == 1, 'Should have be called once'


def test_build_bible_context_menu(settings, state):
    """
    Test the creation of a context menu from service item of type text from Bibles.
    """
    # GIVEN: A new service manager instance and a default service item.
    mocked_renderer = MagicMock()
    mocked_renderer.theme_level = ThemeLevel.Song
    Registry().register('plugin_manager', MagicMock())
    Registry().register('renderer', mocked_renderer)
    service_manager = ServiceManager(None)
    item = MagicMock()
    item.parent.return_value = False
    item.data.return_value = 0
    service_manager.service_manager_list = MagicMock()
    service_manager.service_manager_list.itemAt.return_value = item
    service_item = ServiceItem(None)
    for capability in [ItemCapabilities.NoLineBreaks, ItemCapabilities.CanPreview,
                       ItemCapabilities.CanLoop, ItemCapabilities.CanWordSplit,
                       ItemCapabilities.CanEditTitle]:
        service_item.add_capability(capability)
    service_item.service_item_type = ServiceItemType.Text
    service_item.edit_id = 1
    service_item._display_slides = []
    service_item._display_slides.append(MagicMock())
    service_manager.service_items.insert(1, {'service_item': service_item})
    service_manager.edit_action = MagicMock()
    service_manager.rename_action = MagicMock()
    service_manager.create_custom_action = MagicMock()
    service_manager.maintain_action = MagicMock()
    service_manager.notes_action = MagicMock()
    service_manager.time_action = MagicMock()
    service_manager.auto_start_action = MagicMock()
    service_manager.auto_play_slides_menu = MagicMock()
    service_manager.auto_play_slides_once = MagicMock()
    service_manager.auto_play_slides_loop = MagicMock()
    service_manager.timed_slide_interval = MagicMock()
    service_manager.theme_menu = MagicMock()
    service_manager.menu = MagicMock()
    # WHEN I define a context menu
    service_manager.context_menu(1)
    # THEN the following calls should have occurred.
    assert service_manager.edit_action.setVisible.call_count == 1, 'Should have be called once'
    assert service_manager.rename_action.setVisible.call_count == 2, 'Should have be called twice'
    assert service_manager.create_custom_action.setVisible.call_count == 1, 'Should have be called once'
    assert service_manager.maintain_action.setVisible.call_count == 1, 'Should have be called once'
    assert service_manager.notes_action.setVisible.call_count == 1, 'Should have be called once'
    assert service_manager.time_action.setVisible.call_count == 1, 'Should have be called once'
    assert service_manager.auto_start_action.setVisible.call_count == 1, 'Should have be called once'
    assert service_manager.auto_play_slides_menu.menuAction().setVisible.call_count == 1, \
        'Should have be called once'
    assert service_manager.auto_play_slides_once.setChecked.call_count == 0, 'Should not be called'
    assert service_manager.auto_play_slides_loop.setChecked.call_count == 0, 'Should not be called'
    assert service_manager.timed_slide_interval.setChecked.call_count == 0, 'Should not be called'
    assert service_manager.theme_menu.menuAction().setVisible.call_count == 2, \
        'Should have be called twice'
    # THEN we add a 2nd display frame
    service_item._display_slides.append(MagicMock())
    service_manager.context_menu(1)
    # THEN the following additional calls should have occurred.
    assert service_manager.auto_play_slides_menu.menuAction().setVisible.call_count == 2, \
        'Should have be called twice'
    assert service_manager.auto_play_slides_once.setChecked.call_count == 1, 'Should have be called once'
    assert service_manager.auto_play_slides_loop.setChecked.call_count == 1, 'Should have be called once'
    assert service_manager.timed_slide_interval.setChecked.call_count == 1, 'Should have be called once'


def test_build_custom_context_menu(settings, state):
    """
    Test the creation of a context menu from service item of type text from Custom.
    """
    # GIVEN: A new service manager instance and a default service item.
    mocked_renderer = MagicMock()
    mocked_renderer.theme_level = ThemeLevel.Song
    Registry().register('plugin_manager', MagicMock())
    Registry().register('renderer', mocked_renderer)
    service_manager = ServiceManager(None)
    item = MagicMock()
    item.parent.return_value = False
    item.data.return_value = 0
    service_manager.service_manager_list = MagicMock()
    service_manager.service_manager_list.itemAt.return_value = item
    service_item = ServiceItem(None)
    service_item.add_capability(ItemCapabilities.CanEdit)
    service_item.add_capability(ItemCapabilities.CanPreview)
    service_item.add_capability(ItemCapabilities.CanLoop)
    service_item.add_capability(ItemCapabilities.CanSoftBreak)
    service_item.add_capability(ItemCapabilities.OnLoadUpdate)
    service_item.service_item_type = ServiceItemType.Text
    service_item.edit_id = 1
    service_item._display_slides = []
    service_item._display_slides.append(MagicMock())
    service_manager.service_items.insert(1, {'service_item': service_item})
    service_manager.edit_action = MagicMock()
    service_manager.rename_action = MagicMock()
    service_manager.create_custom_action = MagicMock()
    service_manager.maintain_action = MagicMock()
    service_manager.notes_action = MagicMock()
    service_manager.time_action = MagicMock()
    service_manager.auto_start_action = MagicMock()
    service_manager.auto_play_slides_menu = MagicMock()
    service_manager.auto_play_slides_once = MagicMock()
    service_manager.auto_play_slides_loop = MagicMock()
    service_manager.timed_slide_interval = MagicMock()
    service_manager.theme_menu = MagicMock()
    service_manager.menu = MagicMock()
    # WHEN I define a context menu
    service_manager.context_menu(1)
    # THEN the following calls should have occurred.
    assert service_manager.edit_action.setVisible.call_count == 2, 'Should have be called twice'
    assert service_manager.rename_action.setVisible.call_count == 1, 'Should have be called once'
    assert service_manager.create_custom_action.setVisible.call_count == 1, 'Should have be called once'
    assert service_manager.maintain_action.setVisible.call_count == 1, 'Should have be called once'
    assert service_manager.notes_action.setVisible.call_count == 1, 'Should have be called once'
    assert service_manager.time_action.setVisible.call_count == 1, 'Should have be called once'
    assert service_manager.auto_start_action.setVisible.call_count == 1, 'Should have be called once'
    assert service_manager.auto_play_slides_menu.menuAction().setVisible.call_count == 1, \
        'Should have be called once'
    assert service_manager.auto_play_slides_once.setChecked.call_count == 0, 'Should not be called'
    assert service_manager.auto_play_slides_loop.setChecked.call_count == 0, 'Should not be called'
    assert service_manager.timed_slide_interval.setChecked.call_count == 0, 'Should not be called'
    assert service_manager.theme_menu.menuAction().setVisible.call_count == 2, \
        'Should have be called twice'
    # THEN we add a 2nd display frame
    service_item._display_slides.append(MagicMock())
    service_manager.context_menu(1)
    # THEN the following additional calls should have occurred.
    assert service_manager.auto_play_slides_menu.menuAction().setVisible.call_count == 2, \
        'Should have be called twice'
    assert service_manager.auto_play_slides_once.setChecked.call_count == 1, 'Should have be called once'
    assert service_manager.auto_play_slides_loop.setChecked.call_count == 1, 'Should have be called once'
    assert service_manager.timed_slide_interval.setChecked.call_count == 1, 'Should have be called once'


def test_build_image_context_menu(settings):
    """
    Test the creation of a context menu from service item of type Image from Image.
    """
    # GIVEN: A new service manager instance and a default service item.
    Registry().register('plugin_manager', MagicMock())
    Registry().register('renderer', MagicMock())
    service_manager = ServiceManager(None)
    item = MagicMock()
    item.parent.return_value = False
    item.data.return_value = 0
    service_manager.service_manager_list = MagicMock()
    service_manager.service_manager_list.itemAt.return_value = item
    service_item = ServiceItem(None)
    service_item.add_capability(ItemCapabilities.CanMaintain)
    service_item.add_capability(ItemCapabilities.CanPreview)
    service_item.add_capability(ItemCapabilities.CanLoop)
    service_item.add_capability(ItemCapabilities.CanAppend)
    service_item.add_capability(ItemCapabilities.CanEditTitle)
    service_item.service_item_type = ServiceItemType.Image
    service_item.edit_id = 1
    service_item.slides.append(MagicMock())
    service_manager.service_items.insert(1, {'service_item': service_item})
    service_manager.edit_action = MagicMock()
    service_manager.rename_action = MagicMock()
    service_manager.create_custom_action = MagicMock()
    service_manager.maintain_action = MagicMock()
    service_manager.notes_action = MagicMock()
    service_manager.time_action = MagicMock()
    service_manager.auto_start_action = MagicMock()
    service_manager.auto_play_slides_menu = MagicMock()
    service_manager.auto_play_slides_once = MagicMock()
    service_manager.auto_play_slides_loop = MagicMock()
    service_manager.timed_slide_interval = MagicMock()
    service_manager.theme_menu = MagicMock()
    service_manager.menu = MagicMock()
    # WHEN I define a context menu
    service_manager.context_menu(1)
    # THEN the following calls should have occurred.
    assert service_manager.edit_action.setVisible.call_count == 1, 'Should have be called once'
    assert service_manager.rename_action.setVisible.call_count == 2, 'Should have be called twice'
    assert service_manager.create_custom_action.setVisible.call_count == 1, 'Should have be called once'
    assert service_manager.maintain_action.setVisible.call_count == 2, 'Should have be called twice'
    assert service_manager.notes_action.setVisible.call_count == 1, 'Should have be called once'
    assert service_manager.time_action.setVisible.call_count == 1, 'Should have be called once'
    assert service_manager.auto_start_action.setVisible.call_count == 1, 'Should have be called once'
    assert service_manager.auto_play_slides_menu.menuAction().setVisible.call_count == 1, \
        'Should have be called once'
    assert service_manager.auto_play_slides_once.setChecked.call_count == 0, 'Should not be called'
    assert service_manager.auto_play_slides_loop.setChecked.call_count == 0, 'Should not be called'
    assert service_manager.timed_slide_interval.setChecked.call_count == 0, 'Should not be called'
    assert service_manager.theme_menu.menuAction().setVisible.call_count == 1, \
        'Should have be called once'
    # THEN we add a 2nd display frame and regenerate the menu.
    service_item.slides.append(MagicMock())
    service_manager.context_menu(1)
    # THEN the following additional calls should have occurred.
    assert service_manager.auto_play_slides_menu.menuAction().setVisible.call_count == 2, \
        'Should have be called twice'
    assert service_manager.auto_play_slides_once.setChecked.call_count == 1, 'Should have be called once'
    assert service_manager.auto_play_slides_loop.setChecked.call_count == 1, 'Should have be called once'
    assert service_manager.timed_slide_interval.setChecked.call_count == 1, 'Should have be called once'


def test_build_media_context_menu(settings):
    """
    Test the creation of a context menu from service item of type Command from Media.
    """
    # GIVEN: A new service manager instance and a default service item.
    Registry().register('plugin_manager', MagicMock())
    Registry().register('renderer', MagicMock())
    service_manager = ServiceManager(None)
    item = MagicMock()
    item.parent.return_value = False
    item.data.return_value = 0
    service_manager.service_manager_list = MagicMock()
    service_manager.service_manager_list.itemAt.return_value = item
    service_item = ServiceItem(None)
    service_item.add_capability(ItemCapabilities.CanAutoStartForLive)
    service_item.add_capability(ItemCapabilities.CanEditTitle)
    service_item.add_capability(ItemCapabilities.RequiresMedia)
    service_item.service_item_type = ServiceItemType.Command
    service_item.edit_id = 1
    service_item.slides.append(MagicMock())
    service_manager.service_items.insert(1, {'service_item': service_item})
    service_manager.edit_action = MagicMock()
    service_manager.rename_action = MagicMock()
    service_manager.create_custom_action = MagicMock()
    service_manager.maintain_action = MagicMock()
    service_manager.notes_action = MagicMock()
    service_manager.time_action = MagicMock()
    service_manager.auto_start_action = MagicMock()
    service_manager.auto_play_slides_menu = MagicMock()
    service_manager.auto_play_slides_once = MagicMock()
    service_manager.auto_play_slides_loop = MagicMock()
    service_manager.timed_slide_interval = MagicMock()
    service_manager.theme_menu = MagicMock()
    service_manager.menu = MagicMock()
    # WHEN I define a context menu
    service_manager.context_menu(1)
    # THEN the following calls should have occurred.
    assert service_manager.edit_action.setVisible.call_count == 1, 'Should have be called once'
    assert service_manager.rename_action.setVisible.call_count == 2, 'Should have be called twice'
    assert service_manager.create_custom_action.setVisible.call_count == 1, 'Should have be called once'
    assert service_manager.maintain_action.setVisible.call_count == 1, 'Should have be called once'
    assert service_manager.notes_action.setVisible.call_count == 1, 'Should have be called once'
    assert service_manager.time_action.setVisible.call_count == 1, 'Should have be called once'
    assert service_manager.auto_start_action.setVisible.call_count == 2, 'Should have be called twice'
    assert service_manager.auto_play_slides_menu.menuAction().setVisible.call_count == 1, \
        'Should have be called once'
    assert service_manager.auto_play_slides_once.setChecked.call_count == 0, 'Should not be called'
    assert service_manager.auto_play_slides_loop.setChecked.call_count == 0, 'Should not be called'
    assert service_manager.timed_slide_interval.setChecked.call_count == 0, 'Should not be called'
    assert service_manager.theme_menu.menuAction().setVisible.call_count == 1, \
        'Should have be called once'
    # THEN I change the length of the media and regenerate the menu.
    service_item.set_media_length(5)
    service_manager.context_menu(1)
    # THEN the following additional calls should have occurred.
    assert service_manager.time_action.setVisible.call_count == 3, 'Should have be called three times'


def test_build_presentation_pdf_context_menu(settings):
    """
    Test the creation of a context menu from service item of type Command with PDF from Presentation.
    """
    # GIVEN: A new service manager instance and a default service item.
    Registry().register('plugin_manager', MagicMock())
    Registry().register('renderer', MagicMock())
    service_manager = ServiceManager(None)
    item = MagicMock()
    item.parent.return_value = False
    item.data.return_value = 0
    service_manager.service_manager_list = MagicMock()
    service_manager.service_manager_list.itemAt.return_value = item
    service_item = ServiceItem(None)
    service_item.add_capability(ItemCapabilities.CanMaintain)
    service_item.add_capability(ItemCapabilities.CanPreview)
    service_item.add_capability(ItemCapabilities.CanLoop)
    service_item.add_capability(ItemCapabilities.CanAppend)
    service_item.service_item_type = ServiceItemType.Command
    service_item.edit_id = 1
    service_item.slides.append(MagicMock())
    service_manager.service_items.insert(1, {'service_item': service_item})
    service_manager.edit_action = MagicMock()
    service_manager.rename_action = MagicMock()
    service_manager.create_custom_action = MagicMock()
    service_manager.maintain_action = MagicMock()
    service_manager.notes_action = MagicMock()
    service_manager.time_action = MagicMock()
    service_manager.auto_start_action = MagicMock()
    service_manager.auto_play_slides_menu = MagicMock()
    service_manager.auto_play_slides_once = MagicMock()
    service_manager.auto_play_slides_loop = MagicMock()
    service_manager.timed_slide_interval = MagicMock()
    service_manager.theme_menu = MagicMock()
    service_manager.menu = MagicMock()
    # WHEN I define a context menu
    service_manager.context_menu(1)
    # THEN the following calls should have occurred.
    assert service_manager.edit_action.setVisible.call_count == 1, 'Should have be called once'
    assert service_manager.rename_action.setVisible.call_count == 1, 'Should have be called once'
    assert service_manager.create_custom_action.setVisible.call_count == 1, 'Should have be called once'
    assert service_manager.maintain_action.setVisible.call_count == 2, 'Should have be called twice'
    assert service_manager.notes_action.setVisible.call_count == 1, 'Should have be called once'
    assert service_manager.time_action.setVisible.call_count == 1, 'Should have be called once'
    assert service_manager.auto_start_action.setVisible.call_count == 1, 'Should have be called once'
    assert service_manager.auto_play_slides_menu.menuAction().setVisible.call_count == 1, \
        'Should have be called once'
    assert service_manager.auto_play_slides_once.setChecked.call_count == 0, 'Should not be called'
    assert service_manager.auto_play_slides_loop.setChecked.call_count == 0, 'Should not be called'
    assert service_manager.timed_slide_interval.setChecked.call_count == 0, 'Should not be called'
    assert service_manager.theme_menu.menuAction().setVisible.call_count == 1, \
        'Should have be called once'


def test_build_presentation_non_pdf_context_menu(settings):
    """
    Test the creation of a context menu from service item of type Command with Impress from Presentation.
    """
    # GIVEN: A new service manager instance and a default service item.
    Registry().register('plugin_manager', MagicMock())
    Registry().register('renderer', MagicMock())
    service_manager = ServiceManager(None)
    item = MagicMock()
    item.parent.return_value = False
    item.data.return_value = 0
    service_manager.service_manager_list = MagicMock()
    service_manager.service_manager_list.itemAt.return_value = item
    service_item = ServiceItem(None)
    service_item.add_capability(ItemCapabilities.ProvidesOwnDisplay)
    service_item.service_item_type = ServiceItemType.Command
    service_item.edit_id = 1
    service_item.slides.append(MagicMock())
    service_manager.service_items.insert(1, {'service_item': service_item})
    service_manager.edit_action = MagicMock()
    service_manager.rename_action = MagicMock()
    service_manager.create_custom_action = MagicMock()
    service_manager.maintain_action = MagicMock()
    service_manager.notes_action = MagicMock()
    service_manager.time_action = MagicMock()
    service_manager.auto_start_action = MagicMock()
    service_manager.auto_play_slides_menu = MagicMock()
    service_manager.auto_play_slides_once = MagicMock()
    service_manager.auto_play_slides_loop = MagicMock()
    service_manager.timed_slide_interval = MagicMock()
    service_manager.theme_menu = MagicMock()
    service_manager.menu = MagicMock()
    # WHEN I define a context menu
    service_manager.context_menu(1)
    # THEN the following calls should have occurred.
    assert service_manager.edit_action.setVisible.call_count == 1, 'Should have be called once'
    assert service_manager.rename_action.setVisible.call_count == 1, 'Should have be called once'
    assert service_manager.create_custom_action.setVisible.call_count == 1, 'Should have be called once'
    assert service_manager.maintain_action.setVisible.call_count == 1, 'Should have be called once'
    assert service_manager.notes_action.setVisible.call_count == 1, 'Should have be called once'
    assert service_manager.time_action.setVisible.call_count == 1, 'Should have be called once'
    assert service_manager.auto_start_action.setVisible.call_count == 1, 'Should have be called once'
    assert service_manager.auto_play_slides_menu.menuAction().setVisible.call_count == 1, \
        'Should have be called once'
    assert service_manager.auto_play_slides_once.setChecked.call_count == 0, 'Should not be called'
    assert service_manager.auto_play_slides_loop.setChecked.call_count == 0, 'Should not be called'
    assert service_manager.timed_slide_interval.setChecked.call_count == 0, 'Should not be called'
    assert service_manager.theme_menu.menuAction().setVisible.call_count == 1, \
        'Should have be called once'


@patch('openlp.core.ui.servicemanager.QtCore.QTimer.singleShot')
def test_single_click_preview_true(mocked_singleShot, settings):
    """
    Test that when "Preview items when clicked in Service Manager" enabled the preview timer starts
    """
    # GIVEN: A setting to enable "Preview items when clicked in Service Manager" and a service manager.
    settings.setValue('advanced/single click service preview', True)
    service_manager = ServiceManager(None)
    # WHEN: on_single_click_preview() is called
    service_manager.on_single_click_preview()
    # THEN: timer should have been started
    mocked_singleShot.assert_called_with(QtWidgets.QApplication.instance().doubleClickInterval(),
                                         service_manager.on_single_click_preview_timeout)


@patch('openlp.core.ui.servicemanager.QtCore.QTimer.singleShot')
def test_single_click_preview_false(mocked_singleShot, settings):
    """
    Test that when "Preview items when clicked in Service Manager" disabled the preview timer doesn't start
    """
    # GIVEN: A setting to enable "Preview items when clicked in Service Manager" and a service manager.
    settings.setValue('advanced/single click service preview', False)
    service_manager = ServiceManager(None)
    # WHEN: on_single_click_preview() is called
    service_manager.on_single_click_preview()
    # THEN: timer should not be started
    assert mocked_singleShot.call_count == 0, 'Should not be called'


@patch('openlp.core.ui.servicemanager.QtCore.QTimer.singleShot')
@patch('openlp.core.ui.servicemanager.ServiceManager.make_live')
def test_single_click_preview_double(mocked_make_live, mocked_singleShot, settings):
    """
    Test that when a double click has registered the preview timer doesn't start
    """
    # GIVEN: A setting to enable "Preview items when clicked in Service Manager" and a service manager.
    settings.setValue('advanced/single click service preview', True)
    service_manager = ServiceManager(None)
    # WHEN: on_single_click_preview() is called following a double click
    service_manager.on_double_click_live()
    service_manager.on_single_click_preview()
    # THEN: timer should not be started
    mocked_make_live.assert_called_with()
    assert mocked_singleShot.call_count == 0, 'Should not be called'


@patch('openlp.core.ui.servicemanager.ServiceManager.make_preview')
def test_single_click_timeout_single(mocked_make_preview, settings):
    """
    Test that when a single click has been registered, the item is sent to preview
    """
    # GIVEN: A service manager.
    service_manager = ServiceManager(None)
    # WHEN: on_single_click_preview() is called
    service_manager.on_single_click_preview_timeout()
    # THEN: make_preview() should have been called
    assert mocked_make_preview.call_count == 1, 'ServiceManager.make_preview() should have been called once'


@patch('openlp.core.ui.servicemanager.ServiceManager.make_preview')
@patch('openlp.core.ui.servicemanager.ServiceManager.make_live')
def test_single_click_timeout_double(mocked_make_live, mocked_make_preview, settings):
    """
    Test that when a double click has been registered, the item does not goes to preview
    """
    # GIVEN: A service manager.
    service_manager = ServiceManager(None)
    # WHEN: on_single_click_preview() is called after a double click
    service_manager.on_double_click_live()
    service_manager.on_single_click_preview_timeout()
    # THEN: make_preview() should not have been called
    assert mocked_make_preview.call_count == 0, 'ServiceManager.make_preview() should not be called'


@patch('openlp.core.ui.servicemanager.zipfile')
@patch('openlp.core.ui.servicemanager.ServiceManager.save_file_as')
@patch('openlp.core.ui.servicemanager.os')
@patch('openlp.core.ui.servicemanager.shutil')
@patch('openlp.core.ui.servicemanager.NamedTemporaryFile')
def test_save_file_raises_permission_error(mocked_temp_file, mocked_shutil, mocked_os, mocked_save_file_as,
                                           mocked_zipfile, settings):
    """
    Test that when a PermissionError is raised when trying to save a file, it is handled correctly
    """
    # GIVEN: A service manager, a service to save
    mocked_main_window = MagicMock()
    Registry().register('main_window', mocked_main_window)
    service_manager = ServiceManager(None)
    service_manager._service_path = MagicMock()
    service_manager._save_lite = False
    service_manager.service_items = []
    service_manager.service_theme = 'Default'
    service_manager.service_manager_list = MagicMock()
    mocked_save_file_as.return_value = False
    mocked_zipfile.ZipFile.return_value = MagicMock()
    mocked_os.link.side_effect = PermissionError
    mocked_shutil.copyfile.side_effect = PermissionError

    # WHEN: The service is saved and a PermissionError is raised
    result = service_manager.save_file()

    # THEN: The "save_as" method is called to save the service
    assert result is False
    mocked_save_file_as.assert_called_with()


@patch('openlp.core.ui.servicemanager.zipfile')
@patch('openlp.core.ui.servicemanager.ServiceManager.save_file_as')
@patch('openlp.core.ui.servicemanager.os')
@patch('openlp.core.ui.servicemanager.shutil')
@patch('openlp.core.ui.servicemanager.len')
@patch('openlp.core.ui.servicemanager.NamedTemporaryFile')
def test_save_file_large_file(mocked_temp_file, mocked_len, mocked_shutil, mocked_os, mocked_save_file_as,
                              mocked_zipfile, registry):
    """
    Test that when a file size size larger than a 32bit signed int is attempted to save, the progress bar
    should be provided a value that fits in a 32bit int (because it's passed to C++ as a 32bit unsigned int)
    """
    # GIVEN: A service manager, a service to save, and len() returns a huge value (file size)
    def check_for_i32_overflow(val):
        if val > 2147483647:
            raise OverflowError
    mocked_main_window = MagicMock()
    mocked_main_window.display_progress_bar.side_effect = check_for_i32_overflow
    Registry().register('main_window', mocked_main_window)
    Registry().register('application', MagicMock())
    Registry().register('settings', MagicMock())
    service_manager = ServiceManager(None)
    service_manager._service_path = MagicMock()
    service_manager._save_lite = False
    service_manager.service_items = []
    service_manager.service_theme = 'Default'
    service_manager.service_manager_list = MagicMock()
    mocked_save_file_as.return_value = False
    mocked_zipfile.ZipFile.return_value = MagicMock()
    mocked_len.return_value = 10000000000000

    # WHEN: The service is saved and no error is raised
    result = service_manager.save_file()

    # THEN: The "save_as" method is called to save the service
    assert result is True
    mocked_save_file_as.assert_not_called()


@patch('openlp.core.ui.servicemanager.zipfile')
@patch('openlp.core.ui.servicemanager.ServiceManager.save_file_as')
@patch('openlp.core.ui.servicemanager.os')
@patch('openlp.core.ui.servicemanager.shutil')
@patch('openlp.core.ui.servicemanager.NamedTemporaryFile')
def test_save_file_falls_back_to_shutil(mocked_temp_file, mocked_shutil, mocked_os, mocked_save_file_as, mocked_zipfile,
                                        registry):
    """
    Test that when a PermissionError is raised when trying to save a file, it is handled correctly
    """
    # GIVEN: A service manager, a service to save
    mocked_main_window = MagicMock()
    Registry().register('main_window', mocked_main_window)
    Registry().register('application', MagicMock())
    Registry().register('settings', MagicMock())
    service_manager = ServiceManager(None)
    service_manager._service_path = MagicMock()
    service_manager._save_lite = False
    service_manager.service_items = []
    service_manager.service_theme = 'Default'
    service_manager.service_manager_list = MagicMock()
    mocked_save_file_as.return_value = False
    mocked_zipfile.ZipFile.return_value = MagicMock()
    mocked_os.link.side_effect = OSError

    # WHEN: The service is saved and a PermissionError is raised
    result = service_manager.save_file()

    # THEN: The result is true
    assert result is True
    mocked_shutil.copyfile.assert_called_once()


@patch('openlp.core.ui.servicemanager.ServiceManager.regenerate_service_items')
def test_theme_change_global(mocked_regenerate_service_items, settings):
    """
    Test that when a Toolbar theme combobox displays correctly when the theme is set to Global
    """
    # GIVEN: A service manager, settings set to Global theme
    service_manager = ServiceManager(None)
    service_manager.toolbar = OpenLPToolbar(None)
    service_manager.toolbar.add_toolbar_action('theme_combo_box', triggers=MagicMock())
    service_manager.toolbar.add_toolbar_action('theme_label', triggers=MagicMock())
    settings.setValue('themes/theme level', ThemeLevel.Global)

    # WHEN: theme_change is called
    service_manager.on_theme_level_changed()

    # THEN: The the theme toolbar should not be visible
    assert service_manager.toolbar.actions['theme_combo_box'].isVisible() is False, \
        'The visibility should be False'


@patch('openlp.core.ui.servicemanager.ServiceManager.regenerate_service_items')
def test_theme_change_service(mocked_regenerate_service_items, settings):
    """
    Test that when a Toolbar theme combobox displays correctly when the theme is set to Theme
    """
    # GIVEN: A service manager, settings set to Service theme
    service_manager = ServiceManager(None)
    service_manager.toolbar = OpenLPToolbar(None)
    service_manager.toolbar.add_toolbar_action('theme_combo_box', triggers=MagicMock())
    service_manager.toolbar.add_toolbar_action('theme_label', triggers=MagicMock())
    settings.setValue('themes/theme level', ThemeLevel.Service)

    # WHEN: theme_change is called
    service_manager.on_theme_level_changed()

    # THEN: The the theme toolbar should be visible
    assert service_manager.toolbar.actions['theme_combo_box'].isVisible() is True, \
        'The visibility should be True'


@patch('openlp.core.ui.servicemanager.ServiceManager.regenerate_service_items')
def test_theme_change_song(mocked_regenerate_service_items, settings):
    """
    Test that when a Toolbar theme combobox displays correctly when the theme is set to Song
    """
    # GIVEN: A service manager, settings set to Song theme
    service_manager = ServiceManager(None)
    service_manager.toolbar = OpenLPToolbar(None)
    service_manager.toolbar.add_toolbar_action('theme_combo_box', triggers=MagicMock())
    service_manager.toolbar.add_toolbar_action('theme_label', triggers=MagicMock())
    settings.setValue('themes/theme level', ThemeLevel.Song)

    # WHEN: theme_change is called
    service_manager.on_theme_level_changed()

    # THEN: The the theme toolbar should be visible
    assert service_manager.toolbar.actions['theme_combo_box'].isVisible() is True, \
        'The visibility should be True'


@patch('PyQt5.QtWidgets.QTreeWidgetItemIterator')
def test_regenerate_service_items(mocked_tree, settings):
    """
    test that an unmodified service item that is regenerated is still unmodified
    """
    # GIVEN: A service manager and a service item
    mocked_main_window = MagicMock()
    Registry().register('main_window', mocked_main_window)
    service_manager = ServiceManager(None)
    service_item = ServiceItem(None)
    service_item.service_item_type = ServiceItemType.Command
    service_item.edit_id = 1
    service_item.icon = MagicMock(pixmap=MagicMock())
    service_item.slides.append(MagicMock())
    service_manager.service_items.insert(1, {'service_item': service_item, 'expanded': False})
    service_manager._modified = False
    service_manager.service_manager_list = MagicMock()
    service_manager.repaint_service_list = MagicMock()
    mocked_tree.return_value = MagicMock(value=MagicMock(return_value=None))

    # WHEN: regenerate_service_items is called
    service_manager.regenerate_service_items()

    # THEN: The the service should be repainted and not be marked as modified
    assert service_manager.is_modified() is False
    service_manager.repaint_service_list.assert_called_once()


@patch('PyQt5.QtWidgets.QTreeWidgetItemIterator')
def test_regenerate_service_items_modified(mocked_tree, settings):
    """
    test that an unmodified service item that is regenerated is still unmodified
    """
    # GIVEN: A service manager and a service item
    mocked_main_window = MagicMock()
    Registry().register('main_window', mocked_main_window)
    service_manager = ServiceManager(None)
    service_item = ServiceItem(None)
    service_item.service_item_type = ServiceItemType.Command
    service_item.edit_id = 1
    service_item.icon = MagicMock(pixmap=MagicMock())
    service_item.slides.append(MagicMock())
    service_manager.service_items.insert(1, {'service_item': service_item, 'expanded': False})
    service_manager._modified = True
    service_manager.service_manager_list = MagicMock()
    service_manager.repaint_service_list = MagicMock()
    mocked_tree.return_value = MagicMock(value=MagicMock(return_value=None))

    # WHEN: regenerate_service_items is called
    service_manager.regenerate_service_items()

    # THEN: The the service should be repainted and still be marked as modified
    assert service_manager.is_modified() is True
    service_manager.repaint_service_list.assert_called_once()


@patch('PyQt5.QtWidgets.QTreeWidgetItemIterator')
def test_regenerate_service_items_set_modified(mocked_tree, settings):
    """
    test that a service item that is regenerated with the modified argument becomes modified
    """
    # GIVEN: A service manager and a service item
    mocked_main_window = MagicMock()
    Registry().register('main_window', mocked_main_window)
    service_manager = ServiceManager(None)
    service_item = ServiceItem(None)
    service_item.service_item_type = ServiceItemType.Command
    service_item.edit_id = 1
    service_item.icon = MagicMock(pixmap=MagicMock())
    service_item.slides.append(MagicMock())
    service_manager.service_items.insert(1, {'service_item': service_item, 'expanded': False})
    service_manager._modified = False
    service_manager.service_manager_list = MagicMock()
    service_manager.repaint_service_list = MagicMock()
    mocked_tree.return_value = MagicMock(value=MagicMock(return_value=None))

    # WHEN: regenerate_service_items is called
    service_manager.regenerate_service_items(True)

    # THEN: The the service should be repainted and now be marked as modified
    assert service_manager.is_modified() is True
    service_manager.repaint_service_list.assert_called_once()


def test_service_manager_list_drag_enter_event():
    """
    Test that the ServiceManagerList.dragEnterEvent slot accepts the event
    """
    # GIVEN: A service manager and a mocked event
    service_manager_list = ServiceManagerList(None)
    mocked_event = MagicMock()

    # WHEN: The dragEnterEvent method is called
    service_manager_list.dragEnterEvent(mocked_event)

    # THEN: The accept() method on the event is called
    mocked_event.accept.assert_called_once_with()


def test_service_manager_list_drag_move_event():
    """
    Test that the ServiceManagerList.dragMoveEvent slot accepts the event
    """
    # GIVEN: A service manager and a mocked event
    service_manager_list = ServiceManagerList(None)
    mocked_event = MagicMock()

    # WHEN: The dragMoveEvent method is called
    service_manager_list.dragMoveEvent(mocked_event)

    # THEN: The accept() method on the event is called
    mocked_event.accept.assert_called_once_with()


def test_service_manager_list_key_press_event():
    """
    Test that the ServiceManagerList.keyPressEvent slot ignores the event
    """
    # GIVEN: A service manager and a mocked event
    service_manager_list = ServiceManagerList(None)
    mocked_event = MagicMock()

    # WHEN: The keyPressEvent method is called
    service_manager_list.keyPressEvent(mocked_event)

    # THEN: The ignore() method on the event is called
    mocked_event.ignore.assert_called_once_with()


def test_service_manager_list_mouse_move_event_not_left_button():
    """
    Test that the ServiceManagerList.mouseMoveEvent slot ignores the event if it's not a left-click
    """
    # GIVEN: A service manager and a mocked event
    service_manager_list = ServiceManagerList(None)
    mocked_event = MagicMock()
    mocked_event.buttons.return_value = QtCore.Qt.RightButton

    # WHEN: The mouseMoveEvent method is called
    service_manager_list.mouseMoveEvent(mocked_event)

    # THEN: The ignore() method on the event is called
    mocked_event.ignore.assert_called_once_with()


@patch('openlp.core.ui.servicemanager.QtGui.QCursor')
def test_service_manager_list_mouse_move_event_no_item(MockQCursor):
    """
    Test that the ServiceManagerList.mouseMoveEvent slot ignores the event if it's not over an item
    """
    # GIVEN: A service manager and a mocked event
    service_manager_list = ServiceManagerList(None)
    service_manager_list.itemAt = MagicMock(return_value=None)
    service_manager_list.mapFromGlobal = MagicMock()
    mocked_event = MagicMock()
    mocked_event.buttons.return_value = QtCore.Qt.LeftButton

    # WHEN: The mouseMoveEvent method is called
    service_manager_list.mouseMoveEvent(mocked_event)

    # THEN: The ignore() method on the event is called
    mocked_event.ignore.assert_called_once_with()


@patch('openlp.core.ui.servicemanager.QtGui.QCursor')
@patch('openlp.core.ui.servicemanager.QtGui.QDrag')
@patch('openlp.core.ui.servicemanager.QtCore.QMimeData')
def test_service_manager_list_mouse_move_event(MockQMimeData, MockQDrag, MockQCursor):
    """
    Test that the ServiceManagerList.mouseMoveEvent slot ignores the event if it's not over an item
    """
    # GIVEN: A service manager and a mocked event
    service_manager_list = ServiceManagerList(None)
    service_manager_list.itemAt = MagicMock(return_value=True)
    service_manager_list.mapFromGlobal = MagicMock()
    mocked_event = MagicMock()
    mocked_event.buttons.return_value = QtCore.Qt.LeftButton
    mocked_drag = MagicMock()
    MockQDrag.return_value = mocked_drag
    mocked_mime_data = MagicMock()
    MockQMimeData.return_value = mocked_mime_data

    # WHEN: The mouseMoveEvent method is called
    service_manager_list.mouseMoveEvent(mocked_event)

    # THEN: The ignore() method on the event is called
    mocked_drag.setMimeData.assert_called_once_with(mocked_mime_data)
    mocked_mime_data.setText.assert_called_once_with('ServiceManager')
    mocked_drag.exec.assert_called_once_with(QtCore.Qt.CopyAction)


def test_on_new_service_clicked_not_saved_cancel(registry):
    """Test that when you click on the new service button, you're asked to save any modified documents"""
    # GIVEN: A Service manager and some mocks
    service_manager = ServiceManager(None)
    service_manager.is_modified = MagicMock(return_value=True)
    service_manager.save_modified_service = MagicMock(return_value=QtWidgets.QMessageBox.Cancel)

    # WHEN: on_new_service_clicked() is called
    result = service_manager.on_new_service_clicked()

    # THEN: The method should have exited early (hence the False return)
    assert result is False, 'The method should have returned early'


def test_on_new_service_clicked_not_saved_false_save(registry):
    """Test that when you click on the new service button, you're asked to save any modified documents"""
    # GIVEN: A Service manager and some mocks
    service_manager = ServiceManager(None)
    service_manager.is_modified = MagicMock(return_value=True)
    service_manager.save_modified_service = MagicMock(return_value=QtWidgets.QMessageBox.Save)
    service_manager.decide_save_method = MagicMock(return_value=False)

    # WHEN: on_new_service_clicked() is called
    result = service_manager.on_new_service_clicked()

    # THEN: The method should have exited early (hence the False return)
    assert result is False, 'The method should have returned early'


@patch('openlp.core.ui.servicemanager.QtWidgets.QMessageBox')
def test_on_new_service_clicked_unmodified_blank_service(MockQMessageBox, registry):
    """Test that when the click the new button with an unmodified service, it shows you a message"""
    # GIVEN: A service manager with no service items and a bunch of mocks
    mocked_message_box = MagicMock()
    mocked_message_box.checkbox.return_value.isChecked.return_value = True
    MockQMessageBox.return_value = mocked_message_box
    mocked_settings = MagicMock()
    mocked_settings.value.return_value = True
    registry.register('settings', mocked_settings)
    service_manager = ServiceManager(None)
    service_manager.is_modified = MagicMock(return_value=False)
    service_manager.service_items = []
    service_manager.new_file = MagicMock()

    # WHEN: on_new_service_clicked() is called
    service_manager.on_new_service_clicked()

    # THEN: The message box should have been shown, and the message supressed
    mocked_settings.value.assert_called_once_with('advanced/new service message')
    assert mocked_message_box.setCheckBox.call_count == 1, 'setCheckBox was called to place the checkbox'
    mocked_message_box.exec.assert_called_once_with()
    mocked_settings.setValue.assert_called_once_with('advanced/new service message', False)
    service_manager.new_file.assert_called_once_with()


def _create_mock_action(parent, name, **kwargs):
    """
    Create a fake action with some "real" attributes
    """
    action = QtWidgets.QAction(parent)
    action.setObjectName(name)
    if kwargs.get('triggers'):
        action.triggered.connect(kwargs.pop('triggers'))
    return action


def _add_service_item(s_manager):
    "adds a mocked service item to the passed service manager"
    mocked_plugin = MagicMock()
    mocked_plugin.name = 'songs'
    service_item = ServiceItem(mocked_plugin)
    service_item.add_icon()
    slide = "Test slide"
    service_item.add_from_text(slide)
    service_item.title = "Test item"
    s_manager.add_service_item(service_item, rebuild=True, selected=True)


@pytest.fixture()
def service_manager(registry, settings):
    """Setup a service manager with a service item and a few mocked registry entries"""
    # Mocked registry entries
    Registry().register('main_window', MagicMock())
    Registry().register('live_controller', MagicMock())
    Registry().register('renderer', MagicMock())

    # Service manager
    service_manager = ServiceManager()
    add_toolbar_action_patcher = patch('openlp.core.ui.servicemanager.OpenLPToolbar.add_toolbar_action')
    mocked_add_toolbar_action = add_toolbar_action_patcher.start()
    mocked_add_toolbar_action.side_effect = \
        lambda name, **kwargs: _create_mock_action(service_manager.toolbar, name, **kwargs)
    service_manager.setup_ui(service_manager)

    yield service_manager
    del service_manager

    add_toolbar_action_patcher.stop()


def test_on_delete_from_service_confirmation_disabled(settings, service_manager):
    """
    Test that when the on_delete_from_service function is called and
    confirmation for deleting items is disabled, the currently selected
    item is removed.
    """
    # GIVEN delete item confirmation is disabled and a mock service item
    settings.setValue('advanced/delete service item confirmation', False)
    _add_service_item(service_manager)

    # WHEN the on_delete_from_service function is called
    service_manager.on_delete_from_service()

    # THEN the service_items list should be empty
    assert len(service_manager.service_items) == 0


def test_on_delete_from_service_confirmation_enabled_choose_delete(settings, service_manager):
    """
    Test that when the on_delete_from_service function is called and
    confirmation for deleting items is enabled, and the user confirms
    deletion, the currently selected item is removed from the service.
    """
    # GIVEN delete item confirmation is enabled and a mock service item
    settings.setValue('advanced/delete service item confirmation', True)
    _add_service_item(service_manager)

    # WHEN the on_delete_from_service function is called and the user chooses to delete
    service_manager._delete_confirmation_dialog = MagicMock(return_value=QtWidgets.QMessageBox.Close)
    service_manager.on_delete_from_service()

    # THEN the service_items list should be empty
    assert len(service_manager.service_items) == 0


def test_on_delete_from_service_confirmation_enabled_choose_cancel(settings, service_manager):
    """
    Test that when the on_delete_from_service function is called and
    confirmation for deleting items is enabled, and the user confirms
    deletion, the service remains unchanged.
    """
    # GIVEN delete item confirmation is enabled a mock service item
    settings.setValue('advanced/delete service item confirmation', True)
    _add_service_item(service_manager)
    service_items_copy = service_manager.service_items.copy()

    # WHEN the on_delete_from_service function is called and the user cancels
    service_manager._delete_confirmation_dialog = MagicMock(return_value=QtWidgets.QMessageBox.Cancel)
    service_manager.on_delete_from_service()

    # THEN the service_items list should be unchanged
    assert service_manager.service_items == service_items_copy


def test_on_load_service_clicked(registry):
    """Test that a service is loaded when you click the button"""
    # GIVEN: A service manager
    service_manager = ServiceManager(None)

    # THEN: Check that we have a load_service method first, before mocking it
    assert hasattr(service_manager, 'load_service'), 'ServiceManager.load_service() should exist'

    # GIVEN: A mocked out load_service() method
    service_manager.load_service = MagicMock()

    # WHEN: The load button is clicked
    service_manager.on_load_service_clicked(False)

    # THEN: load_service() should have been called
    service_manager.load_service.assert_called_once_with()


def test_load_service_modified_cancel_save(registry):
    """Test that the load_service() method exits early when the service is modified, but the save is canceled"""
    # GIVEN: A modified ServiceManager
    service_manager = ServiceManager(None)
    service_manager.is_modified = MagicMock(return_value=True)
    service_manager.save_modified_service = MagicMock(return_value=QtWidgets.QMessageBox.Cancel)

    # WHEN: A service is loaded
    result = service_manager.load_service()

    # THEN: The result should be False because of an early exit
    assert result is False, 'The method did not exit early'


@patch('openlp.core.ui.servicemanager.FileDialog.getOpenFileName')
def test_load_service_without_file_path_canceled(mocked_get_open_file_name, registry):
    """Test that the load_service() method does nothing when no file is loaded and the load dialog is canceled"""
    # GIVEN: A modified ServiceManager
    mocked_settings = MagicMock()
    registry.register('settings', mocked_settings)
    service_manager = ServiceManager(None)
    service_manager.is_modified = MagicMock(return_value=False)
    mocked_get_open_file_name.return_value = None, None

    # WHEN: A service is loaded but not path specified, and the load dialog is canceled
    result = service_manager.load_service(file_path=None)

    # THEN: The result should be False
    mocked_get_open_file_name.assert_called_once()
    assert result is False


def test_load_service_modified_saved_with_file_path(registry):
    """Test that the load_service() method saves the file and loads the specified file"""
    # GIVEN: A modified ServiceManager
    mocked_settings = MagicMock()
    registry.register('settings', mocked_settings)
    service_manager = ServiceManager(None)
    service_manager.is_modified = MagicMock(return_value=True)
    service_manager.save_modified_service = MagicMock(return_value=QtWidgets.QMessageBox.Save)
    service_manager.decide_save_method = MagicMock()
    service_manager.load_file = MagicMock()

    # WHEN: A service is loaded
    service_manager.load_service(Path.home() / 'service.osz')

    # THEN: The service should be loaded
    service_manager.decide_save_method.assert_called_once_with()
    mocked_settings.setValue.assert_called_once_with('servicemanager/last directory', Path.home())
    service_manager.load_file.assert_called_once_with(Path.home() / 'service.osz')


@patch('openlp.core.ui.servicemanager.FileDialog.getOpenFileName')
def test_load_service_no_file_path_passed_or_selected(mocked_get_open_file_name, mock_settings):
    """Test that the load_service() method exits early when no file is passed and no file is selected in the dialog"""
    # GIVEN: A modified ServiceManager
    service_manager = ServiceManager(None)
    mocked_get_open_file_name.return_value = (None, None)

    # WHEN: A service is loaded
    result = service_manager.load_service()

    # THEN: The result should be False because of an early exit
    assert result is False, 'The method did not exit early'


@patch('openlp.core.ui.servicemanager.FileDialog.getOpenFileName')
def test_load_service_no_file_path_passed_file_selected(mocked_get_open_file_name, mock_settings):
    """Test that the load_service() method loads a file chosen in the dialog when no file is passed"""
    # GIVEN: A modified ServiceManager
    service_manager = ServiceManager(None)
    mocked_get_open_file_name.return_value = (Path.home() / 'service.osz', None)
    service_manager.load_file = MagicMock()

    # WHEN: A service is loaded
    service_manager.load_service()

    # THEN: The service should be loaded
    service_manager.load_file.assert_called_once_with(Path.home() / 'service.osz')


def test_on_recent_service_clicked_modified_cancel_save(registry):
    """Test that the on_recent_service_clicked() method exits early when the service is modified,
    but the save is canceled"""
    # GIVEN: A modified ServiceManager
    service_manager = ServiceManager(None)
    service_manager.is_modified = MagicMock(return_value=True)
    service_manager.save_modified_service = MagicMock(return_value=QtWidgets.QMessageBox.Cancel)

    # WHEN: on_recent_service_clicked is called
    result = service_manager.on_recent_service_clicked(True)

    # THEN: The result should be False because of an early exit
    assert result is False, 'The method did not exit early'


def test_on_recent_service_clicked_modified_saved_with_file_path(registry):
    """Test that the on_recent_service_clicked() method saves the file and loads the file"""
    # GIVEN: A modified ServiceManager
    mocked_settings = MagicMock()
    registry.register('settings', mocked_settings)
    service_manager = ServiceManager(None)
    service_manager.is_modified = MagicMock(return_value=True)
    service_manager.save_modified_service = MagicMock(return_value=QtWidgets.QMessageBox.Save)
    service_manager.decide_save_method = MagicMock()
    service_manager.load_file = MagicMock()
    service_manager.sender = MagicMock(return_value=MagicMock())

    # WHEN: on_recent_service_clicked is called
    service_manager.on_recent_service_clicked(True)

    # THEN: The recent service should be loaded
    service_manager.decide_save_method.assert_called_once_with()
    service_manager.load_file.assert_called_once()


def test_on_recent_service_clicked_unmodified(registry):
    # GIVEN: A modified ServiceManager
    service_manager = ServiceManager(None)
    service_manager.load_file = MagicMock()
    service_manager.sender = MagicMock(return_value=MagicMock())

    # WHEN: on_recent_service_clicked is called
    service_manager.on_recent_service_clicked(True)

    # THEN: The recent service should be loaded
    service_manager.load_file.assert_called_once()


@patch('openlp.core.ui.servicemanager.Path', autospec=True)
def test_service_manager_load_file_str(MockPath, registry):
    """Test the service manager's load_file method when it is given a str"""
    # GIVEN: A service manager and a mocked path object
    service_manager = ServiceManager(None)
    MockPath.__class__ = Path.__class__
    MockPath.return_value.exists.return_value = False

    # WHEN: A str filename is passed to load_file
    result = service_manager.load_file('service.osz')

    # THEN: False should be returned, but a valid Path object created
    assert result is False, 'ServiceManager.load_file should return false for a non-existant file'
    MockPath.assert_called_once_with('service.osz')
    MockPath.return_value.exists.assert_called_once()


@patch('openlp.core.ui.servicemanager.QtWidgets.QMessageBox')
def test_service_manager_delete_confirmation_dialog(MockMessageBox, registry):
    """Test the _delete_confirmation_dialog() method"""
    # GIVEN: A service manager and a mocked QMessageBox class
    service_manager = ServiceManager(None)
    mocked_message_box = MagicMock()
    MockMessageBox.return_value = mocked_message_box
    # Restore a couple of items for a more realistic situation
    MockMessageBox.Question = QtWidgets.QMessageBox.Question
    MockMessageBox.Close = QtWidgets.QMessageBox.Close
    MockMessageBox.Cancel = QtWidgets.QMessageBox.Cancel
    MockMessageBox.StandardButtons = QtWidgets.QMessageBox.StandardButtons

    # WHEN: _delete_confirmation_dialog() is called
    service_manager._delete_confirmation_dialog()

    # THEN: All the correct things should have been called
    MockMessageBox.assert_called_once_with(QtWidgets.QMessageBox.Question, 'Delete item from service',
                                           'Are you sure you want to delete this item from the service?',
                                           QtWidgets.QMessageBox.StandardButtons(QtWidgets.QMessageBox.Close |
                                                                                 QtWidgets.QMessageBox.Cancel),
                                           service_manager)
    mocked_message_box.button.assert_called_once_with(QtWidgets.QMessageBox.Close)
    mocked_message_box.setDefaultButton.assert_called_once_with(QtWidgets.QMessageBox.Close)
    mocked_message_box.exec.assert_called_once()


@patch('openlp.core.ui.servicemanager.QtWidgets.QMessageBox.question')
def test_service_manager_save_modified_service(mocked_question, registry):
    """Test the save_modified_service() method"""
    # GIVEN: A service manager and a mocked main window
    mocked_main_window = MagicMock()
    registry.register('main_window', mocked_main_window)
    service_manager = ServiceManager(None)

    # WHEN: save_modified_service() is called
    service_manager.save_modified_service()

    # THEN: All the correct things should have been called
    mocked_question.assert_called_once_with(mocked_main_window, 'Modified Service',
                                            'The current service has been modified. '
                                            'Would you like to save this service?',
                                            QtWidgets.QMessageBox.Save | QtWidgets.QMessageBox.Discard |
                                            QtWidgets.QMessageBox.Cancel, QtWidgets.QMessageBox.Save)


def test_service_manager_on_recent_service_clicked_cancel(registry):
    """Test the on_recent_service_clicked() method"""
    # GIVEN: A service manager with some methods mocked out
    service_manager = ServiceManager(None)
    service_manager.is_modified = lambda: True
    service_manager.save_modified_service = lambda: QtWidgets.QMessageBox.Cancel

    # WHEN: on_recent_service_clicked() is called
    result = service_manager.on_recent_service_clicked(True)

    # THEN: The result should be False
    assert result is False, 'on_recent_service_clicked() should have returned False'


def test_service_manager_on_recent_service_clicked_save(registry):
    """Test the on_recent_service_clicked() method"""
    # GIVEN: A service manager with some methods mocked out
    service_manager = ServiceManager(None)
    service_manager.is_modified = lambda: True
    service_manager.save_modified_service = lambda: QtWidgets.QMessageBox.Save
    service_manager.decide_save_method = lambda: None
    service_manager.sender = lambda: MagicMock(**{'data.return_value': '/path/to/service'})
    service_manager.load_file = MagicMock()

    # WHEN: on_recent_service_clicked() is called
    result = service_manager.on_recent_service_clicked(True)

    # THEN: The result should be None
    assert result is None, 'on_recent_service_clicked() should have returned None'
    service_manager.load_file.assert_called_once_with(Path('/path/to/service'))


def test_service_manager_decide_save_method_save(registry):
    """Test the decide_save_method() method"""
    # GIVEN: A service manager with some methods mocked out
    service_manager = ServiceManager(None)
    service_manager.file_name = lambda: 'filename.osz'
    service_manager.save_file = MagicMock()
    service_manager.save_file_as = MagicMock()

    # WHEN: decide_save_method() is called
    service_manager.decide_save_method()

    # THEN: The correct methods should have been called
    service_manager.save_file.assert_called_once()
    assert service_manager.save_file_as.call_count == 0, 'The save_file_as method should not have been called'


def test_service_manager_decide_save_method_save_as(registry):
    """Test the decide_save_method() method"""
    # GIVEN: A service manager with some methods mocked out
    service_manager = ServiceManager(None)
    service_manager.file_name = lambda: None
    service_manager.save_file = MagicMock()
    service_manager.save_file_as = MagicMock()

    # WHEN: decide_save_method() is called
    service_manager.decide_save_method()

    # THEN: The correct methods should have been called
    service_manager.save_file_as.assert_called_once()
    assert service_manager.save_file.call_count == 0, 'The save_file method should not have been called'


def test_load_last_file(registry):
    """Test the load_last_file() method"""
    # GIVEN: Mocked out settings and a ServiceManager
    mocked_settings = MagicMock()
    mocked_settings.value.return_value = Path('filename.osz')
    registry.register('settings', mocked_settings)
    service_manager = ServiceManager(None)
    service_manager.load_file = MagicMock()

    # WHEN: load_last_file() is called
    service_manager.load_last_file()

    # THEN: The file should have been loaded
    service_manager.load_file.assert_called_once_with(Path('filename.osz'))


class TestServiceManager(TestCase, TestMixin):
    """
    Test the service manager
    """

    def _create_mock_action(self, name, **kwargs):
        """
        Create a fake action with some "real" attributes
        """
        action = QtWidgets.QAction(self.service_manager)
        action.setObjectName(name)
        if kwargs.get('triggers'):
            action.triggered.connect(kwargs.pop('triggers'))
        self.service_manager.toolbar.actions[name] = action
        return action

    def setUp(self):
        """
        Create the UI
        """
        Registry.create()
        self.setup_application()
        Registry().register('application', MagicMock())
        Registry().register('main_window', MagicMock())
        Registry().register('settings', Settings())
        self.service_manager = ServiceManager()
        self.add_toolbar_action_patcher = patch('openlp.core.ui.servicemanager.OpenLPToolbar.add_toolbar_action')
        self.mocked_add_toolbar_action = self.add_toolbar_action_patcher.start()
        self.mocked_add_toolbar_action.side_effect = self._create_mock_action

    def tearDown(self):
        """
        Delete all the C++ objects at the end so that we don't have a segfault
        """
        self.add_toolbar_action_patcher.stop()
        del self.service_manager

    def test_bootstrap_initialise(self):
        """
        Test the bootstrap_initialise method
        """
        # GIVEN: Mocked out stuff
        self.service_manager.setup_ui = MagicMock()
        self.service_manager.servicemanager_set_item = MagicMock()
        self.service_manager.servicemanager_set_item_by_uuid = MagicMock()
        self.service_manager.servicemanager_next_item = MagicMock()
        self.service_manager.servicemanager_previous_item = MagicMock()
        self.service_manager.servicemanager_new_file = MagicMock()
        self.service_manager.theme_update_service = MagicMock()

        # WHEN: bootstrap_initialise is called
        self.service_manager.bootstrap_initialise()

        # THEN: The correct calls should have been made
        self.service_manager.setup_ui.assert_called_once_with(self.service_manager)
        self.service_manager.servicemanager_set_item.connect.assert_called_once_with(
            self.service_manager.on_set_item)
        self.service_manager.servicemanager_set_item_by_uuid.connect.assert_called_once_with(
            self.service_manager.set_item_by_uuid)
        self.service_manager.servicemanager_next_item.connect.assert_called_once_with(
            self.service_manager.next_item)
        self.service_manager.servicemanager_previous_item.connect.assert_called_once_with(
            self.service_manager.previous_item)
        self.service_manager.servicemanager_new_file.connect.assert_called_once_with(
            self.service_manager.new_file)
        self.service_manager.theme_update_service.connect.assert_called_once_with(
            self.service_manager.on_service_theme_change)

    @patch('openlp.core.ui.servicemanager.ServiceNoteForm')
    @patch('openlp.core.ui.servicemanager.ServiceItemEditForm')
    @patch('openlp.core.ui.servicemanager.StartTimeForm')
    def test_bootstrap_post_set_up(self, MockStartTimeForm, MockServiceItemEditForm, MockServiceNoteForm):
        """
        Test the post bootstrap setup
        """
        # GIVEN: Mocked forms and a ServiceManager object
        mocked_service_note_form = MagicMock()
        MockServiceNoteForm.return_value = mocked_service_note_form
        mocked_service_item_edit_form = MagicMock()
        MockServiceItemEditForm.return_value = mocked_service_item_edit_form
        mocked_start_time_form = MagicMock()
        MockStartTimeForm.return_value = mocked_start_time_form

        # WHEN: bootstrap_post_set_up is run
        self.service_manager.bootstrap_post_set_up()

        # THEN: The forms should have been created
        assert self.service_manager.service_note_form == mocked_service_note_form
        assert self.service_manager.service_item_edit_form == mocked_service_item_edit_form
        assert self.service_manager.start_time_form == mocked_start_time_form

    def test_set_file_name_osz(self):
        """
        Test setting the file name
        """
        # GIVEN: A service manager, some mocks and a file name
        self.service_manager.set_modified = MagicMock()
        self.service_manager.settings.setValue = MagicMock()
        file_path = Path('servicefile.osz')

        # WHEN: The filename is set
        self.service_manager.set_file_name(file_path)

        # THEN: Various things should have been called and set
        assert self.service_manager._service_path == file_path
        self.service_manager.set_modified.assert_called_once_with(False)
        self.service_manager.settings.setValue.assert_called_once_with('servicemanager/last file', file_path)
        assert self.service_manager._save_lite is False

    def test_set_file_name_oszl(self):
        """
        Test setting the file name
        """
        # GIVEN: A service manager, some mocks and a file name
        self.service_manager.set_modified = MagicMock()
        self.service_manager.settings.setValue = MagicMock()
        file_path = Path('servicefile.oszl')

        # WHEN: The filename is set
        self.service_manager.set_file_name(file_path)

        # THEN: Various things should have been called and set
        assert self.service_manager._service_path == file_path
        self.service_manager.set_modified.assert_called_once_with(False)
        self.service_manager.settings.setValue.assert_called_once_with('servicemanager/last file', file_path)
        assert self.service_manager._save_lite is True

    def test_short_file_name(self):
        """
        Test the short_file_name method
        """
        # GIVEN: A service manager and a file name
        self.service_manager._service_path = Path('/home/user/service.osz')

        # WHEN: short_file_name is called
        result = self.service_manager.short_file_name()

        # THEN: The result should be correct
        assert result == 'service.osz'

    def test_basic_service_manager(self):
        """
        Test the Service Manager UI Functionality
        """
        # GIVEN: A New Service Manager instance
        # WHEN I have set up the display
        self.service_manager.setup_ui(self.service_manager)

        # THEN the count of items should be zero
        assert self.service_manager.service_manager_list.topLevelItemCount() == 0, \
            'The service manager list should be empty '

    @patch('openlp.core.ui.servicemanager.QtWidgets.QTreeWidget.itemAt')
    @patch('openlp.core.ui.servicemanager.QtWidgets.QWidget.mapToGlobal')
    @patch('openlp.core.ui.servicemanager.QtWidgets.QMenu.exec')
    def test_default_context_menu(self, mocked_exec, mocked_mapToGlobal, mocked_item_at_method):
        """
        Test the context_menu() method with a default service item
        """
        # GIVEN: A service item added
        mocked_item = MagicMock()
        mocked_item.parent.return_value = None
        mocked_item_at_method.return_value = mocked_item
        mocked_item.data.return_value = 1
        self.service_manager.setup_ui(self.service_manager)
        # A service item without capabilities.
        service_item = ServiceItem()
        self.service_manager.service_items = [{'service_item': service_item}]
        q_point = None
        # Mocked actions.
        self.service_manager.edit_action.setVisible = MagicMock()
        self.service_manager.create_custom_action.setVisible = MagicMock()
        self.service_manager.maintain_action.setVisible = MagicMock()
        self.service_manager.notes_action.setVisible = MagicMock()
        self.service_manager.time_action.setVisible = MagicMock()
        self.service_manager.auto_start_action.setVisible = MagicMock()

        # WHEN: Show the context menu.
        self.service_manager.context_menu(q_point)

        # THEN: The following actions should be not visible.
        self.service_manager.edit_action.setVisible.assert_called_once_with(False), \
            'The action should be set invisible.'
        self.service_manager.create_custom_action.setVisible.assert_called_once_with(False), \
            'The action should be set invisible.'
        self.service_manager.maintain_action.setVisible.assert_called_once_with(False), \
            'The action should be set invisible.'
        self.service_manager.notes_action.setVisible.assert_called_with(True), 'The action should be set visible.'
        self.service_manager.time_action.setVisible.assert_called_once_with(False), \
            'The action should be set invisible.'
        self.service_manager.auto_start_action.setVisible.assert_called_once_with(False), \
            'The action should be set invisible.'

    def test_edit_context_menu(self):
        """
        Test the context_menu() method with a edit service item
        """
        # GIVEN: A service item added
        self.service_manager.setup_ui(self.service_manager)
        with patch('openlp.core.ui.servicemanager.QtWidgets.QTreeWidget.itemAt') as mocked_item_at_method, \
                patch('openlp.core.ui.servicemanager.QtWidgets.QWidget.mapToGlobal'), \
                patch('openlp.core.ui.servicemanager.QtWidgets.QMenu.exec'):
            mocked_item = MagicMock()
            mocked_item.parent.return_value = None
            mocked_item_at_method.return_value = mocked_item
            # We want 1 to be returned for the position
            mocked_item.data.return_value = 1
            # A service item without capabilities.
            service_item = ServiceItem()
            service_item.add_capability(ItemCapabilities.CanEdit)
            service_item.edit_id = 1
            self.service_manager.service_items = [{'service_item': service_item}]
            q_point = None
            # Mocked actions.
            self.service_manager.edit_action.setVisible = MagicMock()
            self.service_manager.create_custom_action.setVisible = MagicMock()
            self.service_manager.maintain_action.setVisible = MagicMock()
            self.service_manager.notes_action.setVisible = MagicMock()
            self.service_manager.time_action.setVisible = MagicMock()
            self.service_manager.auto_start_action.setVisible = MagicMock()

            # WHEN: Show the context menu.
            self.service_manager.context_menu(q_point)

            # THEN: The following actions should be not visible.
            self.service_manager.edit_action.setVisible.assert_called_with(True), \
                'The action should be set visible.'
            self.service_manager.create_custom_action.setVisible.assert_called_once_with(False), \
                'The action should be set invisible.'
            self.service_manager.maintain_action.setVisible.assert_called_once_with(False), \
                'The action should be set invisible.'
            self.service_manager.notes_action.setVisible.assert_called_with(True), 'The action should be set visible.'
            self.service_manager.time_action.setVisible.assert_called_once_with(False), \
                'The action should be set invisible.'
            self.service_manager.auto_start_action.setVisible.assert_called_once_with(False), \
                'The action should be set invisible.'

    def test_maintain_context_menu(self):
        """
        Test the context_menu() method with a maintain
        """
        # GIVEN: A service item added
        self.service_manager.setup_ui(self.service_manager)
        with patch('openlp.core.ui.servicemanager.QtWidgets.QTreeWidget.itemAt') as mocked_item_at_method, \
                patch('openlp.core.ui.servicemanager.QtWidgets.QWidget.mapToGlobal'), \
                patch('openlp.core.ui.servicemanager.QtWidgets.QMenu.exec'):
            mocked_item = MagicMock()
            mocked_item.parent.return_value = None
            mocked_item_at_method.return_value = mocked_item
            # We want 1 to be returned for the position
            mocked_item.data.return_value = 1
            # A service item without capabilities.
            service_item = ServiceItem()
            service_item.add_capability(ItemCapabilities.CanMaintain)
            self.service_manager.service_items = [{'service_item': service_item}]
            q_point = None
            # Mocked actions.
            self.service_manager.edit_action.setVisible = MagicMock()
            self.service_manager.create_custom_action.setVisible = MagicMock()
            self.service_manager.maintain_action.setVisible = MagicMock()
            self.service_manager.notes_action.setVisible = MagicMock()
            self.service_manager.time_action.setVisible = MagicMock()
            self.service_manager.auto_start_action.setVisible = MagicMock()

            # WHEN: Show the context menu.
            self.service_manager.context_menu(q_point)

            # THEN: The following actions should be not visible.
            self.service_manager.edit_action.setVisible.assert_called_once_with(False), \
                'The action should be set invisible.'
            self.service_manager.create_custom_action.setVisible.assert_called_once_with(False), \
                'The action should be set invisible.'
            self.service_manager.maintain_action.setVisible.assert_called_with(True), \
                'The action should be set visible.'
            self.service_manager.notes_action.setVisible.assert_called_with(True), 'The action should be set visible.'
            self.service_manager.time_action.setVisible.assert_called_once_with(False), \
                'The action should be set invisible.'
            self.service_manager.auto_start_action.setVisible.assert_called_once_with(False), \
                'The action should be set invisible.'

    def test_loopy_context_menu(self):
        """
        Test the context_menu() method with a loop
        """
        # GIVEN: A service item added
        self.service_manager.setup_ui(self.service_manager)
        with patch('openlp.core.ui.servicemanager.QtWidgets.QTreeWidget.itemAt') as mocked_item_at_method, \
                patch('openlp.core.ui.servicemanager.QtWidgets.QWidget.mapToGlobal'), \
                patch('openlp.core.ui.servicemanager.QtWidgets.QMenu.exec'):
            mocked_item = MagicMock()
            mocked_item.parent.return_value = None
            mocked_item_at_method.return_value = mocked_item
            # We want 1 to be returned for the position
            mocked_item.data.return_value = 1
            # A service item without capabilities.
            service_item = ServiceItem()
            service_item.add_capability(ItemCapabilities.CanLoop)
            service_item.slides.append("One")
            service_item.slides.append("Two")
            self.service_manager.service_items = [{'service_item': service_item}]
            q_point = None
            # Mocked actions.
            self.service_manager.edit_action.setVisible = MagicMock()
            self.service_manager.create_custom_action.setVisible = MagicMock()
            self.service_manager.maintain_action.setVisible = MagicMock()
            self.service_manager.notes_action.setVisible = MagicMock()
            self.service_manager.time_action.setVisible = MagicMock()
            self.service_manager.auto_start_action.setVisible = MagicMock()

            # WHEN: Show the context menu.
            self.service_manager.context_menu(q_point)

            # THEN: The following actions should be not visible.
            self.service_manager.edit_action.setVisible.assert_called_once_with(False), \
                'The action should be set invisible.'
            self.service_manager.create_custom_action.setVisible.assert_called_once_with(False), \
                'The action should be set invisible.'
            self.service_manager.maintain_action.setVisible.assert_called_once_with(False), \
                'The action should be set invisible.'
            self.service_manager.notes_action.setVisible.assert_called_with(True), 'The action should be set visible.'
            self.service_manager.time_action.setVisible.assert_called_once_with(False), \
                'The action should be set invisible.'
            self.service_manager.auto_start_action.setVisible.assert_called_once_with(False), \
                'The action should be set invisible.'

    def test_start_time_context_menu(self):
        """
        Test the context_menu() method with a start time
        """
        # GIVEN: A service item added
        self.service_manager.setup_ui(self.service_manager)
        with patch('openlp.core.ui.servicemanager.QtWidgets.QTreeWidget.itemAt') as mocked_item_at_method, \
                patch('openlp.core.ui.servicemanager.QtWidgets.QWidget.mapToGlobal'), \
                patch('openlp.core.ui.servicemanager.QtWidgets.QMenu.exec'):
            mocked_item = MagicMock()
            mocked_item.parent.return_value = None
            mocked_item_at_method.return_value = mocked_item
            # We want 1 to be returned for the position
            mocked_item.data.return_value = 1
            # A service item without capabilities.
            service_item = ServiceItem()
            service_item.add_capability(ItemCapabilities.HasVariableStartTime)
            self.service_manager.service_items = [{'service_item': service_item}]
            q_point = None
            # Mocked actions.
            self.service_manager.edit_action.setVisible = MagicMock()
            self.service_manager.create_custom_action.setVisible = MagicMock()
            self.service_manager.maintain_action.setVisible = MagicMock()
            self.service_manager.notes_action.setVisible = MagicMock()
            self.service_manager.time_action.setVisible = MagicMock()
            self.service_manager.auto_start_action.setVisible = MagicMock()

            # WHEN: Show the context menu.
            self.service_manager.context_menu(q_point)

            # THEN: The following actions should be not visible.
            self.service_manager.edit_action.setVisible.assert_called_once_with(False), \
                'The action should be set invisible.'
            self.service_manager.create_custom_action.setVisible.assert_called_once_with(False), \
                'The action should be set invisible.'
            self.service_manager.maintain_action.setVisible.assert_called_once_with(False), \
                'The action should be set invisible.'
            self.service_manager.notes_action.setVisible.assert_called_with(True), 'The action should be set visible.'
            self.service_manager.time_action.setVisible.assert_called_with(True), \
                'The action should be set visible.'
            self.service_manager.auto_start_action.setVisible.assert_called_once_with(False), \
                'The action should be set invisible.'

    def test_auto_start_context_menu(self):
        """
        Test the context_menu() method with can auto start
        """
        # GIVEN: A service item added
        self.service_manager.setup_ui(self.service_manager)
        with patch('openlp.core.ui.servicemanager.QtWidgets.QTreeWidget.itemAt') as mocked_item_at_method, \
                patch('openlp.core.ui.servicemanager.QtWidgets.QWidget.mapToGlobal'), \
                patch('openlp.core.ui.servicemanager.QtWidgets.QMenu.exec'):
            mocked_item = MagicMock()
            mocked_item.parent.return_value = None
            mocked_item_at_method.return_value = mocked_item
            # We want 1 to be returned for the position
            mocked_item.data.return_value = 1
            # A service item without capabilities.
            service_item = ServiceItem()
            service_item.add_capability(ItemCapabilities.CanAutoStartForLive)
            self.service_manager.service_items = [{'service_item': service_item}]
            q_point = None
            # Mocked actions.
            self.service_manager.edit_action.setVisible = MagicMock()
            self.service_manager.create_custom_action.setVisible = MagicMock()
            self.service_manager.maintain_action.setVisible = MagicMock()
            self.service_manager.notes_action.setVisible = MagicMock()
            self.service_manager.time_action.setVisible = MagicMock()
            self.service_manager.auto_start_action.setVisible = MagicMock()
            self.service_manager.rename_action.setVisible = MagicMock()

            # WHEN: Show the context menu.
            self.service_manager.context_menu(q_point)

            # THEN: The following actions should be not visible.
            self.service_manager.edit_action.setVisible.assert_called_once_with(False), \
                'The action should be set invisible.'
            self.service_manager.create_custom_action.setVisible.assert_called_once_with(False), \
                'The action should be set invisible.'
            self.service_manager.maintain_action.setVisible.assert_called_once_with(False), \
                'The action should be set invisible.'
            self.service_manager.notes_action.setVisible.assert_called_with(True), 'The action should be set visible.'
            self.service_manager.time_action.setVisible.assert_called_once_with(False), \
                'The action should be set invisible.'
            self.service_manager.auto_start_action.setVisible.assert_called_with(True), \
                'The action should be set visible.'
            self.service_manager.rename_action.setVisible.assert_called_once_with(False), \
                'The action should be set invisible.'

    def test_click_on_new_service(self):
        """
        Test the on_new_service event handler is called by the UI
        """
        # GIVEN: An initial form
        mocked_event = MagicMock()
        self.service_manager.on_new_service_clicked = mocked_event
        self.service_manager.setup_ui(self.service_manager)

        # WHEN displaying the UI and pressing cancel
        new_service = self.service_manager.toolbar.actions['newService']
        new_service.trigger()

        assert mocked_event.call_count == 1, 'The on_new_service_clicked method should have been called once'

    def test_expand_selection_on_right_arrow(self):
        """
        Test that a right arrow key press event calls the on_expand_selection function
        """
        # GIVEN a mocked expand function
        self.service_manager.on_expand_selection = MagicMock()

        # WHEN the right arrow key event is called
        self.service_manager.setup_ui(self.service_manager)
        event = QtGui.QKeyEvent(QtCore.QEvent.KeyPress, QtCore.Qt.Key_Right, QtCore.Qt.NoModifier)
        self.service_manager.service_manager_list.keyPressEvent(event)

        # THEN the on_expand_selection function should have been called.
        self.service_manager.on_expand_selection.assert_called_once_with()

    def test_on_expand_selection_item_none(self):
        """
        Test that on_expand_selection exits early when there is no item selected.
        """
        # GIVEN a mocked expand function
        self.service_manager.service_manager_list = MagicMock(**{'currentItem.return_value': None})

        # WHEN on_expand_selection is called
        self.service_manager.on_expand_selection()

        # THEN on_expand_selection should have exited early
        self.service_manager.service_manager_list.isExpanded.assert_not_called()

    def test_collapse_selection_on_left_arrow(self):
        """
        Test that a left arrow key press event calls the on_collapse_selection function
        """
        # GIVEN a mocked collapse function
        self.service_manager.on_collapse_selection = MagicMock()

        # WHEN the left arrow key event is called
        self.service_manager.setup_ui(self.service_manager)
        event = QtGui.QKeyEvent(QtCore.QEvent.KeyPress, QtCore.Qt.Key_Left, QtCore.Qt.NoModifier)
        self.service_manager.service_manager_list.keyPressEvent(event)

        # THEN the on_collapse_selection function should have been called.
        self.service_manager.on_collapse_selection.assert_called_once_with()

    def test_move_selection_down_on_down_arrow(self):
        """
        Test that a down arrow key press event calls the on_move_selection_down function
        """
        # GIVEN a mocked move down function
        self.service_manager.on_move_selection_down = MagicMock()

        # WHEN the down arrow key event is called
        self.service_manager.setup_ui(self.service_manager)
        event = QtGui.QKeyEvent(QtCore.QEvent.KeyPress, QtCore.Qt.Key_Down, QtCore.Qt.NoModifier)
        self.service_manager.service_manager_list.keyPressEvent(event)

        # THEN the on_move_selection_down function should have been called.
        self.service_manager.on_move_selection_down.assert_called_once_with()

    def test_move_selection_up_on_up_arrow(self):
        """
        Test that an up arrow key press event calls the on_move_selection_up function
        """
        # GIVEN a mocked move up function
        self.service_manager.on_move_selection_up = MagicMock()

        # WHEN the up arrow key event is called
        self.service_manager.setup_ui(self.service_manager)
        event = QtGui.QKeyEvent(QtCore.QEvent.KeyPress, QtCore.Qt.Key_Up, QtCore.Qt.NoModifier)
        self.service_manager.service_manager_list.keyPressEvent(event)

        # THEN the on_move_selection_up function should have been called.
        self.service_manager.on_move_selection_up.assert_called_once_with()

    def test_delete_selection_on_delete_key(self):
        """
        Test that a delete key press event calls the on_delete_from_service function
        """
        # GIVEN a mocked on_delete_from_service function
        self.service_manager.on_delete_from_service = MagicMock()

        # WHEN the delete key event is called
        self.service_manager.setup_ui(self.service_manager)
        event = QtGui.QKeyEvent(QtCore.QEvent.KeyPress, QtCore.Qt.Key_Delete, QtCore.Qt.NoModifier)
        self.service_manager.service_manager_list.keyPressEvent(event)

        # THEN the on_delete_from_service function should have been called.
        self.service_manager.on_delete_from_service.assert_called_once_with()

    def _setup_service_manager_list(self):
        self.service_manager.expanded = MagicMock()
        self.service_manager.collapsed = MagicMock()
        verse_1 = QtWidgets.QTreeWidgetItem(0)
        verse_2 = QtWidgets.QTreeWidgetItem(0)
        song_item = QtWidgets.QTreeWidgetItem(0)
        song_item.addChild(verse_1)
        song_item.addChild(verse_2)
        self.service_manager.setup_ui(self.service_manager)
        self.service_manager.service_manager_list.addTopLevelItem(song_item)
        return verse_1, verse_2, song_item

    def test_on_expand_selection(self):
        """
        Test that the on_expand_selection function successfully expands an item and moves to its first child
        """
        # GIVEN a mocked servicemanager list
        verse_1, verse_2, song_item = self._setup_service_manager_list()
        self.service_manager.service_manager_list.setCurrentItem(song_item)
        # Reset expanded function in case it has been called and/or changed in initialisation of the service manager.
        self.service_manager.expanded = MagicMock()

        # WHEN on_expand_selection is called
        self.service_manager.on_expand_selection()

        # THEN selection should be expanded
        selected_index = self.service_manager.service_manager_list.currentIndex()
        above_selected_index = self.service_manager.service_manager_list.indexAbove(selected_index)
        assert self.service_manager.service_manager_list.isExpanded(above_selected_index) is True, \
            'Item should have been expanded'
        self.service_manager.expanded.assert_called_once_with(song_item)

    def test_on_collapse_selection_with_parent_selected(self):
        """
        Test that the on_collapse_selection function successfully collapses an item
        """
        # GIVEN a mocked servicemanager list
        verse_1, verse_2, song_item = self._setup_service_manager_list()
        self.service_manager.service_manager_list.setCurrentItem(song_item)
        self.service_manager.service_manager_list.expandItem(song_item)

        # Reset collapsed function in case it has been called and/or changed in initialisation of the service manager.
        self.service_manager.collapsed = MagicMock()

        # WHEN on_expand_selection is called
        self.service_manager.on_collapse_selection()

        # THEN selection should be expanded
        selected_index = self.service_manager.service_manager_list.currentIndex()
        assert self.service_manager.service_manager_list.isExpanded(selected_index) is False, \
            'Item should have been collapsed'
        assert self.service_manager.service_manager_list.currentItem() == song_item, \
            'Top item should have been selected'
        self.service_manager.collapsed.assert_called_once_with(song_item)

    def test_on_collapse_selection_with_child_selected(self):
        """
        Test that the on_collapse_selection function successfully collapses child's parent item
        and moves selection to its parent.
        """
        # GIVEN a mocked servicemanager list
        verse_1, verse_2, song_item = self._setup_service_manager_list()
        self.service_manager.service_manager_list.setCurrentItem(verse_2)
        self.service_manager.service_manager_list.expandItem(song_item)
        # Reset collapsed function in case it has been called and/or changed in initialisation of the service manager.
        self.service_manager.collapsed = MagicMock()

        # WHEN on_expand_selection is called
        self.service_manager.on_collapse_selection()

        # THEN selection should be expanded
        selected_index = self.service_manager.service_manager_list.currentIndex()
        assert self.service_manager.service_manager_list.isExpanded(selected_index) is False, \
            'Item should have been collapsed'
        assert self.service_manager.service_manager_list.currentItem() == song_item, \
            'Top item should have been selected'
        self.service_manager.collapsed.assert_called_once_with(song_item)

    def test_replace_service_item(self):
        """
        Tests that the replace_service_item function replaces items as expected
        """
        # GIVEN a service item list and a new item which name and edit_id match a service item
        self.service_manager.repaint_service_list = MagicMock()
        Registry().register('live_controller', MagicMock())
        item1 = MagicMock()
        item1.edit_id = 'abcd'
        item1.name = 'itemA'
        item2 = MagicMock()
        item2.edit_id = 'abcd'
        item2.name = 'itemB'
        item3 = MagicMock()
        item3.edit_id = 'cfgh'
        item3.name = 'itemA'
        self.service_manager.service_items = [
            {'service_item': item1},
            {'service_item': item2},
            {'service_item': item3}
        ]
        new_item = MagicMock()
        new_item.edit_id = 'abcd'
        new_item.name = 'itemA'

        # WHEN replace_service_item is called
        self.service_manager.replace_service_item(new_item)

        # THEN new_item should replace item1, and only replaces that one item
        assert self.service_manager.service_items[0]['service_item'] == new_item
        new_item.merge.assert_called_once_with(item1)
