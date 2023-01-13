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
This module contains tests for the openlp.core.widgets.edits module
"""
import os
import pytest
from pathlib import Path
from unittest.mock import MagicMock, PropertyMock, patch, call

from PyQt5 import QtCore, QtGui, QtTest, QtWidgets

from openlp.core.common.registry import Registry
from openlp.core.widgets.dialogs import FileDialog
from openlp.core.widgets.edits import PathEdit, HistoryComboBox, SearchEdit
from openlp.core.widgets.enums import PathEditType


class SearchTypes(object):
    """
    Types of search
    """
    First = 0
    Second = 1


SECOND_PLACEHOLDER_TEXT = "Second Placeholder Text"
SEARCH_TYPES = [(SearchTypes.First, QtGui.QIcon(), "First", "First Placeholder Text"),
                (SearchTypes.Second, QtGui.QIcon(), "Second", SECOND_PLACEHOLDER_TEXT)]


@pytest.fixture()
def search_edit(mock_settings):
    main_window = QtWidgets.QMainWindow()
    Registry().register('main_window', main_window)
    Registry().remove('settings')
    Registry().register('settings', MagicMock(**{'value.return_value': SearchTypes.First}))

    s_edit = SearchEdit(main_window, 'settings_section')
    # To complete set up we have to set the search types.
    s_edit.set_search_types(SEARCH_TYPES)
    return s_edit


@pytest.fixture()
def combo(mock_settings):
    main_window = QtWidgets.QMainWindow()
    Registry().register('main_window', main_window)
    s_combo = HistoryComboBox(main_window)
    return s_combo


@pytest.fixture()
def widget():
    with patch('openlp.core.widgets.edits.PathEdit._setup'):
        return PathEdit()


def test_path_getter(widget):
    """
    Test the `path` property getter.
    """
    # GIVEN: An instance of PathEdit with the `_path` instance variable set
    widget._path = Path('getter', 'test', 'pat.h')

    # WHEN: Reading the `path` property
    # THEN: The value that we set should be returned
    assert widget.path == Path('getter', 'test', 'pat.h')


def test_path_setter(widget):
    """
    Test the `path` property setter.
    """
    # GIVEN: An instance of the PathEdit object and a mocked `line_edit`
    widget.line_edit = MagicMock()

    # WHEN: Writing to the `path` property
    widget.path = Path('setter', 'test', 'pat.h')

    # THEN: The `_path` instance variable should be set with the test data. The `line_edit` text and tooltip
    #       should have also been set.
    assert widget._path == Path('setter', 'test', 'pat.h')
    widget.line_edit.setToolTip.assert_called_once_with(os.path.join('setter', 'test', 'pat.h'))
    widget.line_edit.setText.assert_called_once_with(os.path.join('setter', 'test', 'pat.h'))


def test_path_type_getter(widget):
    """
    Test the `path_type` property getter.
    """
    # GIVEN: An instance of PathEdit
    # WHEN: Reading the `path` property
    # THEN: The default value should be returned
    assert widget.path_type == PathEditType.Files


def test_path_type_setter(widget):
    """
    Test the `path_type` property setter.
    """
    # GIVEN: An instance of the PathEdit object and a mocked `update_button_tool_tips` method.
    with patch.object(widget, 'update_button_tool_tips') as mocked_update_button_tool_tips:

        # WHEN: Writing to a different value than default to the `path_type` property
        widget.path_type = PathEditType.Directories

        # THEN: The `_path_type` instance variable should be set with the test data and not the default. The
        #       update_button_tool_tips should have been called.
        assert widget._path_type == PathEditType.Directories
        mocked_update_button_tool_tips.assert_called_once_with()


def test_update_button_tool_tips_directories(widget):
    """
    Test the `update_button_tool_tips` method.
    """
    # GIVEN: An instance of PathEdit with the `path_type` set to `Directories`
    widget.browse_button = MagicMock()
    widget.revert_button = MagicMock()
    widget._path_type = PathEditType.Directories

    # WHEN: Calling update_button_tool_tips
    widget.update_button_tool_tips()

    widget.browse_button.setToolTip.assert_called_once_with('Browse for directory.')
    widget.revert_button.setToolTip.assert_called_once_with('Revert to default directory.')


def test_update_button_tool_tips_files(widget):
    """
    Test the `update_button_tool_tips` method.
    """
    # GIVEN: An instance of PathEdit with the `path_type` set to `Files`
    widget.browse_button = MagicMock()
    widget.revert_button = MagicMock()
    widget._path_type = PathEditType.Files

    # WHEN: Calling update_button_tool_tips
    widget.update_button_tool_tips()

    widget.browse_button.setToolTip.assert_called_once_with('Browse for file.')
    widget.revert_button.setToolTip.assert_called_once_with('Revert to default file.')


@patch('openlp.core.widgets.edits.FileDialog.getExistingDirectory', return_value=None)
@patch('openlp.core.widgets.edits.FileDialog.getOpenFileName')
def test_on_browse_button_clicked_directory(mocked_get_open_file_name, mocked_get_existing_directory, widget):
    """
    Test the `browse_button` `clicked` handler on_browse_button_clicked when the `path_type` is set to Directories.
    """
    # GIVEN: An instance of PathEdit with the `path_type` set to `Directories` and a mocked
    #        QFileDialog.getExistingDirectory
    widget._path_type = PathEditType.Directories
    widget._path = Path('test', 'path')

    # WHEN: Calling on_browse_button_clicked
    widget.on_browse_button_clicked()

    # THEN: The FileDialog.getExistingDirectory should have been called with the default caption
    mocked_get_existing_directory.assert_called_once_with(widget, 'Select Directory',
                                                          Path('test', 'path'),
                                                          FileDialog.ShowDirsOnly)
    assert mocked_get_open_file_name.called is False


def test_on_browse_button_clicked_directory_custom_caption(widget):
    """
    Test the `browse_button` `clicked` handler on_browse_button_clicked when the `path_type` is set to Directories,
    and `dialog_caption` is set.
    """
    # GIVEN: An instance of PathEdit with the `path_type` set to `Directories` and a mocked
    #        QFileDialog.getExistingDirectory with `default_caption` set.
    with patch('openlp.core.widgets.edits.FileDialog.getExistingDirectory', return_value=None) as \
            mocked_get_existing_directory, \
            patch('openlp.core.widgets.edits.FileDialog.getOpenFileName') as mocked_get_open_file_name:
        widget._path_type = PathEditType.Directories
        widget._path = Path('test', 'path')
        widget.dialog_caption = 'Directory Caption'

        # WHEN: Calling on_browse_button_clicked
        widget.on_browse_button_clicked()

        # THEN: The FileDialog.getExistingDirectory should have been called with the custom caption
        mocked_get_existing_directory.assert_called_once_with(widget, 'Directory Caption',
                                                              Path('test', 'path'),
                                                              FileDialog.ShowDirsOnly)
        assert mocked_get_open_file_name.called is False


def test_on_browse_button_clicked_file(widget):
    """
    Test the `browse_button` `clicked` handler on_browse_button_clicked when the `path_type` is set to Files.
    """
    # GIVEN: An instance of PathEdit with the `path_type` set to `Files` and a mocked QFileDialog.getOpenFileName
    with patch('openlp.core.widgets.edits.FileDialog.getExistingDirectory') as mocked_get_existing_directory, \
            patch('openlp.core.widgets.edits.FileDialog.getOpenFileName', return_value=(None, '')) as \
            mocked_get_open_file_name:
        widget._path_type = PathEditType.Files
        widget._path = Path('test', 'pat.h')

        # WHEN: Calling on_browse_button_clicked
        widget.on_browse_button_clicked()

        # THEN: The FileDialog.getOpenFileName should have been called with the default caption
        mocked_get_open_file_name.assert_called_once_with(widget, 'Select File', Path('test', 'pat.h'),
                                                          widget.filters)
        assert mocked_get_existing_directory.called is False


def test_on_browse_button_clicked_file_custom_caption(widget):
    """
    Test the `browse_button` `clicked` handler on_browse_button_clicked when the `path_type` is set to Files and
    `dialog_caption` is set.
    """
    # GIVEN: An instance of PathEdit with the `path_type` set to `Files` and a mocked QFileDialog.getOpenFileName
    #        with `default_caption` set.
    with patch('openlp.core.widgets.edits.FileDialog.getExistingDirectory') as mocked_get_existing_directory, \
            patch('openlp.core.widgets.edits.FileDialog.getOpenFileName', return_value=(None, '')) as \
            mocked_get_open_file_name:
        widget._path_type = PathEditType.Files
        widget._path = Path('test', 'pat.h')
        widget.dialog_caption = 'File Caption'

        # WHEN: Calling on_browse_button_clicked
        widget.on_browse_button_clicked()

        # THEN: The FileDialog.getOpenFileName should have been called with the custom caption
        mocked_get_open_file_name.assert_called_once_with(widget, 'File Caption', Path('test', 'pat.h'),
                                                          widget.filters)
        assert mocked_get_existing_directory.called is False


def test_on_browse_button_clicked_user_cancels(widget):
    """
    Test the `browse_button` `clicked` handler on_browse_button_clicked when the user cancels the FileDialog (an
    empty str is returned)
    """
    # GIVEN: An instance of PathEdit with a mocked QFileDialog.getOpenFileName which returns an empty str for the
    #        file path.
    with patch('openlp.core.widgets.edits.FileDialog.getOpenFileName', return_value=(None, '')) as \
            mocked_get_open_file_name:

        # WHEN: Calling on_browse_button_clicked
        widget.on_browse_button_clicked()

        # THEN: normpath should not have been called
        assert mocked_get_open_file_name.called is True


def test_on_browse_button_clicked_user_accepts(widget):
    """
    Test the `browse_button` `clicked` handler on_browse_button_clicked when the user accepts the FileDialog (a path
    is returned)
    """
    # GIVEN: An instance of PathEdit with a mocked QFileDialog.getOpenFileName which returns a str for the file
    #        path.
    with patch('openlp.core.widgets.edits.FileDialog.getOpenFileName',
               return_value=(Path('test', 'pat.h'), '')) as mocked_get_open_file_name, \
            patch.object(widget, 'on_new_path'):

        # WHEN: Calling on_browse_button_clicked
        widget.on_browse_button_clicked()

        # THEN: normpath and `on_new_path` should have been called
        assert mocked_get_open_file_name.called is True
        assert widget.on_new_path.called is True


def test_on_revert_button_clicked(widget):
    """
    Test that the default path is set as the path when the `revert_button.clicked` handler is called.
    """
    # GIVEN: An instance of PathEdit with a mocked `on_new_path`, and the `default_path` set.
    with patch.object(widget, 'on_new_path') as mocked_on_new_path:
        widget.default_path = Path('default', 'pat.h')

        # WHEN: Calling `on_revert_button_clicked`
        widget.on_revert_button_clicked()

        # THEN: on_new_path should have been called with the default path
        mocked_on_new_path.assert_called_once_with(Path('default', 'pat.h'))


def test_on_line_edit_editing_finished(widget):
    """
    Test that the new path is set as the path when the `line_edit.editingFinished` handler is called.
    """
    # GIVEN: An instance of PathEdit with a mocked `line_edit` and `on_new_path`.
    with patch.object(widget, 'on_new_path') as mocked_on_new_path:
        widget.line_edit = MagicMock(**{'text.return_value': 'test/pat.h'})

        # WHEN: Calling `on_line_edit_editing_finished`
        widget.on_line_edit_editing_finished()

        # THEN: on_new_path should have been called with the path enetered in `line_edit`
        mocked_on_new_path.assert_called_once_with(Path('test', 'pat.h'))


def test_on_new_path_no_change(widget):
    """
    Test `on_new_path` when called with a path that is the same as the existing path.
    """
    # GIVEN: An instance of PathEdit with a test path and mocked `pathChanged` signal
    with patch('openlp.core.widgets.edits.PathEdit.path', new_callable=PropertyMock):
        widget._path = Path('/old', 'test', 'pat.h')
        widget.pathChanged = MagicMock()

        # WHEN: Calling `on_new_path` with the same path as the existing path
        widget.on_new_path(Path('/old', 'test', 'pat.h'))

        # THEN: The `pathChanged` signal should not be emitted
        assert widget.pathChanged.emit.called is False


def test_on_new_path_change(widget):
    """
    Test `on_new_path` when called with a path that is the different to the existing path.
    """
    # GIVEN: An instance of PathEdit with a test path and mocked `pathChanged` signal
    with patch('openlp.core.widgets.edits.PathEdit.path', new_callable=PropertyMock):
        widget._path = Path('/old', 'test', 'pat.h')
        widget.pathChanged = MagicMock()

        # WHEN: Calling `on_new_path` with the a new path
        widget.on_new_path(Path('/new', 'test', 'pat.h'))

        # THEN: The `pathChanged` signal should be emitted
        widget.pathChanged.emit.assert_called_once_with(Path('/new', 'test', 'pat.h'))


def test_set_search_types(search_edit):
    """
    Test setting the search types of the search edit.
    """
    # GIVEN: The search edit with the search types set. NOTE: The set_search_types(types) is called in the setUp()
    # method!

    # WHEN:

    # THEN: The first search type should be the first one in the list. The selected type should be saved in the
    #       settings
    assert search_edit.current_search_type() == SearchTypes.First, \
        "The first search type should be selected."
    Registry().get('settings').setValue.assert_called_once_with('settings_section/last used search type', 0)


def test_set_current_search_type(search_edit):
    """
    Test if changing the search type works.
    """
    # GIVEN:
    # WHEN: Change the search type
    result = search_edit.set_current_search_type(SearchTypes.Second)

    # THEN:
    assert result is True, "The call should return success (True)."
    assert search_edit.current_search_type() == SearchTypes.Second, \
        "The search type should be SearchTypes.Second"
    assert search_edit.placeholderText() == SECOND_PLACEHOLDER_TEXT, \
        "The correct placeholder text should be 'Second Placeholder Text'."
    Registry().get('settings').setValue.assert_has_calls(
        [call('settings_section/last used search type', 0), call('settings_section/last used search type', 1)])


def test_clear_button_visibility(search_edit):
    """
    Test if the clear button is hidden/shown correctly.
    """
    # GIVEN: Everything is left to its defaults (hidden).
    assert search_edit.clear_button.isHidden(), "Pre condition not met. Button should be hidden."

    # WHEN: Type something in the search edit.
    QtTest.QTest.keyPress(search_edit, QtCore.Qt.Key_A)
    QtTest.QTest.keyRelease(search_edit, QtCore.Qt.Key_A)

    # THEN: The clear button should not be hidden any more.
    assert not search_edit.clear_button.isHidden(), "The clear button should be visible."


def test_press_clear_button(search_edit):
    """
    Check if the search edit behaves correctly when pressing the clear button.
    """
    # GIVEN: A search edit with text.
    QtTest.QTest.keyPress(search_edit, QtCore.Qt.Key_A)
    QtTest.QTest.keyRelease(search_edit, QtCore.Qt.Key_A)

    # WHEN: Press the clear button.
    QtTest.QTest.mouseClick(search_edit.clear_button, QtCore.Qt.LeftButton)

    # THEN: The search edit text should be cleared and the button be hidden.
    assert not search_edit.text(), "The search edit should not have any text."
    assert search_edit.clear_button.isHidden(), "The clear button should be hidden."


def test_history_combo_get_items(combo):
    """
    Test the getItems() method
    """
    # GIVEN: The combo.

    # WHEN: Add two items.
    combo.addItem('test1')
    combo.addItem('test2')

    # THEN: The list of items should contain both strings.
    assert combo.getItems() == ['test1', 'test2']
