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
This module contains tests for the lib submodule of the Songs plugin.
"""
import pytest
from unittest.mock import MagicMock, patch

from openlp.plugins.songs.forms.editsongform import EditSongForm


@pytest.fixture()
def edit_song_form():
    with patch('openlp.plugins.songs.forms.editsongform.EditSongForm.__init__', return_value=None):
        return EditSongForm(None, MagicMock(), MagicMock())


def test_validate_matching_tags(edit_song_form):
    # Given a set of tags
    tags = ['{r}', '{/r}', '{bl}', '{/bl}', '{su}', '{/su}']

    # WHEN we validate them
    valid = edit_song_form._validate_tags(tags)

    # THEN they should be valid
    assert valid is True, "The tags list should be valid"


def test_validate_nonmatching_tags(edit_song_form):
    # Given a set of tags
    tags = ['{r}', '{/r}', '{bl}', '{/bl}', '{br}', '{su}', '{/su}']

    # WHEN we validate them
    valid = edit_song_form._validate_tags(tags)

    # THEN they should be valid
    assert valid is True, "The tags list should be valid"


@patch('openlp.plugins.songs.forms.editsongform.set_case_insensitive_completer')
def test_load_objects(mocked_set_case_insensitive_completer, edit_song_form, settings):
    """
    Test the _load_objects() method
    """
    # GIVEN: A song edit form and some mocked stuff
    mocked_class = MagicMock()
    mocked_class.name = 'Author'
    mocked_combo = MagicMock()
    mocked_combo.count.return_value = 0
    mocked_cache = MagicMock()
    mocked_object = MagicMock()
    mocked_object.name = 'Charles'
    mocked_object.id = 1
    mocked_manager = MagicMock()
    mocked_manager.get_all_objects.return_value = [mocked_object]
    edit_song_form.manager = mocked_manager

    # WHEN: _load_objects() is called
    edit_song_form._load_objects(mocked_class, mocked_combo, mocked_cache)

    # THEN: All the correct methods should have been called
    edit_song_form.manager.get_all_objects.assert_called_once_with(mocked_class)
    mocked_combo.clear.assert_called_once_with()
    mocked_combo.count.assert_called_once_with()
    mocked_combo.addItem.assert_called_once_with('Charles')
    mocked_cache.append.assert_called_once_with('Charles')
    mocked_combo.setItemData.assert_called_once_with(0, 1)
    mocked_set_case_insensitive_completer.assert_called_once_with(mocked_cache, mocked_combo)
    mocked_combo.setCurrentIndex.assert_called_once_with(-1)
    mocked_combo.setCurrentText.assert_called_once_with('')
