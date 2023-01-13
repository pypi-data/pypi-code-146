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
from unittest.mock import MagicMock

import pytest
from PyQt5 import QtCore, QtWidgets

from openlp.core.ui.library import FolderLibraryItem


class MockItem(MagicMock):
    file_path = 'path/to/video.mp4'


class MockFolder(MagicMock):
    pass


@pytest.fixture
def folder_library_item(registry, settings):
    mocked_item = MagicMock()
    mocked_manager = MagicMock()
    mocked_manager.get_object_filtered.return_value = mocked_item
    library_item = FolderLibraryItem(None, MagicMock(manager=mocked_manager), MockFolder, MockItem)
    return library_item


def test_folderlibrary_retranslate_ui(folder_library_item):
    """Test the retranslate_ui() method"""
    # GIVEN: A FolderLibraryItem object with mocks
    folder_library_item.add_folder_action = MagicMock()

    # WHEN: retranslate_ui() is called
    folder_library_item.retranslate_ui()

    # THEN: there should be no errors and the text should be correct
    folder_library_item.add_folder_action.setText.assert_called_once_with('Add folder')
    folder_library_item.add_folder_action.setToolTip.assert_called_once_with('Add folder.')


def test_folderlibrary_create_item_from_id_path(registry, settings):
    """Test the create_item_from_id method"""
    # GIVEN: An instance of the FolderLibraryItem
    mocked_item = MagicMock()
    mocked_manager = MagicMock()
    mocked_manager.get_object_filtered.return_value = mocked_item
    library_item = FolderLibraryItem(None, MagicMock(manager=mocked_manager), MockFolder, MockItem)

    # WHEN: create_item_from_id is called
    result = library_item.create_item_from_id('path/to/video.mp4')

    # THEN: The result should be a QTreeWidgetItem with a mocked object as data
    assert isinstance(result, QtWidgets.QTreeWidgetItem)
    assert result.data(0, QtCore.Qt.UserRole) is mocked_item


def test_folderlibrary_create_item_from_id_object(registry, settings):
    """Test the create_item_from_id method"""
    # GIVEN: An instance of the FolderLibraryItem
    mocked_item = MagicMock()
    mocked_manager = MagicMock()
    mocked_manager.get_object_filtered.return_value = mocked_item
    library_item = FolderLibraryItem(None, MagicMock(manager=mocked_manager), MockFolder, MockItem)

    # WHEN: create_item_from_id is called
    result = library_item.create_item_from_id(mocked_item)

    # THEN: The result should be a QTreeWidgetItem with a mocked object as data
    assert isinstance(result, QtWidgets.QTreeWidgetItem)
    assert result.data(0, QtCore.Qt.UserRole) is mocked_item


def test_folderlibrary_current_folder(folder_library_item):
    """Test that the current_folder property returns the correct folder"""
    # GIVEN: A whole buncha mocks
    mocked_folder = MockFolder()
    mocked_item = MockItem()
    mocked_list_folder = MagicMock(**{'data.return_value': mocked_folder}, spec=QtWidgets.QTreeWidgetItem)
    mocked_list_item = MagicMock(**{'data.return_value': mocked_item, 'parent.return_value': mocked_list_folder})
    folder_library_item.list_view = MagicMock()
    folder_library_item.list_view.selectedItems.return_value = [mocked_list_item]

    # WHEN: We access the property
    folder = folder_library_item.current_folder

    # THEN: The current folder should be the mocked folder
    assert folder is mocked_folder
