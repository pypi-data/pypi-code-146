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
This module contains tests for the lib submodule of the Images plugin.
"""
import pytest
from pathlib import Path
from unittest.mock import ANY, MagicMock, patch

from PyQt5 import QtCore, QtWidgets

from openlp.core.common.registry import Registry
from openlp.core.common.enum import ImageThemeMode
from openlp.core.lib.serviceitem import ItemCapabilities
from openlp.plugins.images.lib.db import ImageFilenames, ImageGroups
from openlp.plugins.images.lib.mediaitem import ImageMediaItem


@pytest.fixture
def media_item(mock_settings):
    """Local test setup"""
    mocked_main_window = MagicMock()
    Registry().register('service_list', MagicMock())
    Registry().register('main_window', mocked_main_window)
    Registry().register('live_controller', MagicMock())
    mocked_plugin = MagicMock()
    with patch('openlp.plugins.images.lib.mediaitem.MediaManagerItem._setup'), \
            patch('openlp.plugins.images.lib.mediaitem.ImageMediaItem.setup_item'):
        m_item = ImageMediaItem(None, mocked_plugin)
        m_item.settings_section = 'images'
    return m_item


def _recursively_delete_group_side_effect(*args, **kwargs):
    """
    Side effect method that creates custom return values for the recursively_delete_group method
    """
    if args[0] == ImageFilenames and args[1]:
        # Create some fake objects that should be removed
        returned_object1 = ImageFilenames()
        returned_object1.id = 1
        returned_object1.file_path = Path('/', 'tmp', 'test_file_1.jpg')
        returned_object1.file_hash = 'abcd1'
        returned_object2 = ImageFilenames()
        returned_object2.id = 2
        returned_object2.file_path = Path('/', 'tmp', 'test_file_2.jpg')
        returned_object2.file_hash = 'abcd2'
        returned_object3 = ImageFilenames()
        returned_object3.id = 3
        returned_object3.file_path = Path('/', 'tmp', 'test_file_3.jpg')
        returned_object3.file_hash = 'abcd3'
        return [returned_object1, returned_object2, returned_object3]
    if args[0] == ImageGroups and args[1]:
        # Change the parent_id that is matched so we don't get into an endless loop
        ImageGroups.parent_id = 0
        # Create a fake group that will be used in the next run
        returned_object1 = ImageGroups()
        returned_object1.id = 1
        return [returned_object1]
    return []


@patch('openlp.plugins.images.lib.mediaitem.ImageMediaItem.load_full_list')
def test_save_new_images_list_empty_list(mocked_load_full_list, media_item):
    """
    Test that the save_new_images_list() method handles empty lists gracefully
    """
    # GIVEN: An empty image_list
    image_list = []
    media_item.manager = MagicMock()

    # WHEN: We run save_new_images_list with the empty list
    media_item.save_new_images_list(image_list)

    # THEN: The save_object() method should not have been called
    assert media_item.manager.save_object.call_count == 0, \
        'The save_object() method should not have been called'


@patch('openlp.plugins.images.lib.mediaitem.ImageMediaItem.load_full_list')
@patch('openlp.plugins.images.lib.mediaitem.sha256_file_hash')
def test_save_new_images_list_single_image_with_reload(mocked_sha256_file_hash, mocked_load_full_list, media_item):
    """
    Test that the save_new_images_list() calls load_full_list() when reload_list is set to True
    """
    # GIVEN: A list with 1 image and a mocked out manager
    image_list = [Path('test_image.jpg')]
    ImageFilenames.file_path = None
    media_item.manager = MagicMock()
    mocked_sha256_file_hash.return_value = 'abcd'

    # WHEN: We run save_new_images_list with reload_list=True
    media_item.save_new_images_list(image_list, reload_list=True)

    # THEN: load_full_list() should have been called
    assert mocked_load_full_list.call_count == 1, 'load_full_list() should have been called'

    # CLEANUP: Remove added attribute from ImageFilenames
    delattr(ImageFilenames, 'file_path')


@patch('openlp.plugins.images.lib.mediaitem.ImageMediaItem.load_full_list')
@patch('openlp.plugins.images.lib.mediaitem.sha256_file_hash')
def test_save_new_images_list_single_image_without_reload(mocked_sha256_file_hash, mocked_load_full_list, media_item):
    """
    Test that the save_new_images_list() doesn't call load_full_list() when reload_list is set to False
    """
    # GIVEN: A list with 1 image and a mocked out manager
    image_list = [Path('test_image.jpg')]
    media_item.manager = MagicMock()
    mocked_sha256_file_hash.return_value = 'abcd'

    # WHEN: We run save_new_images_list with reload_list=False
    media_item.save_new_images_list(image_list, reload_list=False)

    # THEN: load_full_list() should not have been called
    assert mocked_load_full_list.call_count == 0, 'load_full_list() should not have been called'


@patch('openlp.plugins.images.lib.mediaitem.ImageMediaItem.load_full_list')
@patch('openlp.plugins.images.lib.mediaitem.sha256_file_hash')
def test_save_new_images_list_multiple_images(mocked_sha256_file_hash, mocked_load_full_list, media_item):
    """
    Test that the save_new_images_list() saves all images in the list
    """
    # GIVEN: A list with 3 images
    image_list = [Path('test_image_1.jpg'), Path('test_image_2.jpg'), Path('test_image_3.jpg')]
    media_item.manager = MagicMock()
    mocked_sha256_file_hash.return_value = 'abcd'

    # WHEN: We run save_new_images_list with the list of 3 images
    media_item.save_new_images_list(image_list, reload_list=False)

    # THEN: load_full_list() should not have been called
    assert media_item.manager.save_object.call_count == 3, \
        'load_full_list() should have been called three times'


@patch('openlp.plugins.images.lib.mediaitem.ImageMediaItem.load_full_list')
@patch('openlp.plugins.images.lib.mediaitem.sha256_file_hash')
def test_save_new_images_list_other_objects_in_list(mocked_sha256_file_hash, mocked_load_full_list, media_item):
    """
    Test that the save_new_images_list() ignores everything in the provided list except strings
    """
    # GIVEN: A list with images and objects
    image_list = [Path('test_image_1.jpg'), None, True, ImageFilenames(), Path('test_image_2.jpg')]
    media_item.manager = MagicMock()
    mocked_sha256_file_hash.return_value = 'abcd'

    # WHEN: We run save_new_images_list with the list of images and objects
    media_item.save_new_images_list(image_list, reload_list=False)

    # THEN: load_full_list() should not have been called
    assert media_item.manager.save_object.call_count == 2, 'load_full_list() should have been called only once'


def test_on_reset_click(media_item):
    """
    Test that on_reset_click() actually resets the background
    """
    # GIVEN: A mocked version of reset_action
    media_item.reset_action = MagicMock()
    media_item.reset_action_context = MagicMock()

    # WHEN: on_reset_click is called
    media_item.on_reset_click()

    # THEN: the reset_action should be set invisible, and the image should be reset
    media_item.reset_action.setVisible.assert_called_with(False)
    media_item.reset_action_context.setVisible.assert_called_with(False)
    media_item.live_controller.reload_theme.assert_called_with()


def test_on_display_changed(media_item):
    """
    Test that on_display_changed() hides the reset background button
    """
    # GIVEN: A mocked version of reset_action
    media_item.reset_action = MagicMock()
    media_item.reset_action_context = MagicMock()

    # WHEN: on_display_changed is called
    media_item.on_display_changed()

    # THEN: the reset_action should be set invisible
    media_item.reset_action.setVisible.assert_called_with(False)
    media_item.reset_action_context.setVisible.assert_called_with(False)


def test_generate_slide_data_default_theme(media_item):
    """
    Test that the generated service item provides the corect theme
    """
    # GIVEN: A mocked service item and settings
    mocked_service_item = MagicMock()
    media_item.list_view = MagicMock()
    Registry().get('settings').value.side_effect = [ImageThemeMode.Black]

    # WHEN: generate_slide_data is called
    media_item.generate_slide_data(mocked_service_item)

    # THEN: The service item should force the theme, and use the default theme
    mocked_service_item.add_capability.assert_any_call(ItemCapabilities.ProvidesOwnTheme)
    assert mocked_service_item.theme == -1


def test_generate_slide_data_custom_theme(media_item):
    """
    Test that the generated service item provides the corect theme
    """
    # GIVEN: A mocked service item and settings
    mocked_service_item = MagicMock()
    media_item.list_view = MagicMock()
    Registry().get('settings').value.side_effect = [ImageThemeMode.CustomTheme, 'theme_name']

    # WHEN: generate_slide_data is called
    media_item.generate_slide_data(mocked_service_item)

    # THEN: The service item should force the theme, and use the theme in the settings
    mocked_service_item.add_capability.assert_any_call(ItemCapabilities.ProvidesOwnTheme)
    assert mocked_service_item.theme == 'theme_name'


@patch('openlp.plugins.images.lib.mediaitem.check_item_selected')
@patch('openlp.plugins.images.lib.mediaitem.isinstance')
@patch('openlp.plugins.images.lib.mediaitem.Path.exists')
def test_on_replace_click(mocked_exists, mocked_isinstance, mocked_check_item_selected, media_item):
    """
    Test that on_replace_click() actually sets the background
    """
    # GIVEN: A mocked version of reset_action, and a (faked) existing selected image file
    media_item.reset_action = MagicMock()
    media_item.reset_action_context = MagicMock()
    media_item.list_view = MagicMock()
    mocked_check_item_selected.return_value = True
    mocked_isinstance.return_value = True
    mocked_exists.return_value = True

    # WHEN: on_replace_click is called
    media_item.on_replace_click()

    # THEN: the reset_action should be set visible, and the image should be set
    media_item.reset_action.setVisible.assert_called_with(True)
    media_item.reset_action_context.setVisible.assert_called_with(True)
    media_item.live_controller.set_background_image.assert_called_with(ANY)


@patch('openlp.plugins.images.lib.mediaitem.delete_file')
@patch('openlp.core.lib.serviceitem.sha256_file_hash')
def test_recursively_delete_group(mocked_sha256_file_hash, mocked_delete_file, media_item):
    """
    Test that recursively_delete_group() works
    """
    # GIVEN: An ImageGroups object and mocked functions
    ImageFilenames.group_id = 1
    ImageGroups.parent_id = 1
    media_item.manager = MagicMock()
    media_item.manager.get_all_objects.side_effect = _recursively_delete_group_side_effect
    media_item.service_path = Path()
    test_group = ImageGroups()
    test_group.id = 1
    mocked_sha256_file_hash.return_value = 'abcd'

    # WHEN: recursively_delete_group() is called
    media_item.recursively_delete_group(test_group)

    # THEN: delete_file() should have been called 12 times and manager.delete_object() 7 times.
    assert mocked_delete_file.call_count == 12, 'delete_file() should have been called 12 times'
    assert media_item.manager.delete_object.call_count == 7, \
        'manager.delete_object() should be called exactly 7 times'

    # CLEANUP: Remove added attribute from Image Filenames and ImageGroups
    delattr(ImageFilenames, 'group_id')
    delattr(ImageGroups, 'parent_id')


@patch('openlp.plugins.images.lib.mediaitem.delete_file')
@patch('openlp.plugins.images.lib.mediaitem.check_item_selected')
@patch('openlp.core.lib.serviceitem.sha256_file_hash')
def test_on_delete_click(mocked_sha256_file_hash, mocked_check_item_selected, mocked_delete_file, media_item):
    """
    Test that on_delete_click() works
    """
    # GIVEN: An ImageGroups object and mocked functions
    mocked_check_item_selected.return_value = True
    test_image = ImageFilenames()
    test_image.id = 1
    test_image.group_id = 1
    test_image.file_path = Path('imagefile.png')
    test_image.file_hash = 'abcd'
    media_item.manager = MagicMock()
    media_item.service_path = Path()
    media_item.list_view = MagicMock()
    mocked_row_item = MagicMock()
    mocked_row_item.data.return_value = test_image
    mocked_row_item.text.return_value = ''
    media_item.list_view.selectedItems.return_value = [mocked_row_item]
    mocked_sha256_file_hash.return_value = 'abcd'

    # WHEN: Calling on_delete_click
    media_item.on_delete_click()

    # THEN: delete_file should have been called twice
    assert mocked_delete_file.call_count == 2, 'delete_file() should have been called twice'


def test_create_item_from_id(media_item):
    """
    Test that the create_item_from_id() method returns a valid QTreeWidgetItem with a pre-created ImageFilenames
    """
    # GIVEN: An ImageFilenames that already exists in the database
    image_file = ImageFilenames()
    image_file.id = 1
    image_file.file_path = Path('/', 'tmp', 'test_file_1.jpg')
    media_item.manager = MagicMock()
    media_item.manager.get_object_filtered.return_value = image_file
    ImageFilenames.file_path = None

    # WHEN: create_item_from_id() is called
    item = media_item.create_item_from_id('1')

    # THEN: A QTreeWidgetItem should be created with the above model object as it's data
    assert isinstance(item, QtWidgets.QTreeWidgetItem)
    assert 'test_file_1.jpg' == item.text(0)
    item_data = item.data(0, QtCore.Qt.UserRole)
    assert isinstance(item_data, ImageFilenames)
    assert 1 == item_data.id
    assert Path('/', 'tmp', 'test_file_1.jpg') == item_data.file_path


@patch('openlp.plugins.images.lib.mediaitem.ImageMediaItem.load_list')
def test_validate_and_load(mocked_load_list, media_item):
    """
    Test that the validate_and_load_test() method when called without a group
    """
    # GIVEN: A list of files
    file_list = [Path('path1', 'image1.jpg'), Path('path2', 'image2.jpg')]

    # WHEN: Calling validate_and_load with the list of files
    media_item.validate_and_load(file_list)

    # THEN: load_list should have been called with the file list and None,
    #       the directory should have been saved to the settings
    mocked_load_list.assert_called_once_with(file_list, None)
    Registry().get('settings').setValue.assert_called_once_with(ANY, Path('path1'))


@patch('openlp.plugins.images.lib.mediaitem.ImageMediaItem.load_list')
def test_validate_and_load_group(mocked_load_list, media_item):
    """
    Test that the validate_and_load_test() method when called with a group
    """
    # GIVEN: A list of files
    file_list = [Path('path1', 'image1.jpg'), Path('path2', 'image2.jpg')]

    # WHEN: Calling validate_and_load with the list of files and a group
    media_item.validate_and_load(file_list, 'group')

    # THEN: load_list should have been called with the file list and the group name,
    #       the directory should have been saved to the settings
    mocked_load_list.assert_called_once_with(file_list, 'group')
    Registry().get('settings').setValue.assert_called_once_with(ANY, Path('path1'))


def test_generate_thumbnail_path_hash(media_item):
    """
    Test that the thumbnail path is correctly generated with the file hash
    """
    # GIVEN: A media item and an Image object
    mocked_image = MagicMock(file_path=Path('myimage.jpg'), file_hash='c3986a0bd8e1ec9da406df142950c67e7d435410')
    media_item.service_path = Path('.')

    # WHEN: generate_thumbnail_path() is called
    result = media_item.generate_thumbnail_path(mocked_image)

    # THEN: The path should be correct
    assert result == Path('.') / 'c3986a0bd8e1ec9da406df142950c67e7d435410.jpg'


def test_generate_thumbnail_path_filename(media_item):
    """
    Test that the thumbnail path is correctly generated with the file name
    """
    # GIVEN: A media item and an Image object
    mocked_image = MagicMock(file_path=Path('myimage.jpg'), file_hash=None)
    media_item.service_path = Path('.')

    # WHEN: generate_thumbnail_path() is called
    result = media_item.generate_thumbnail_path(mocked_image)

    # THEN: The path should be correct
    assert result == Path('.') / 'myimage.jpg'
