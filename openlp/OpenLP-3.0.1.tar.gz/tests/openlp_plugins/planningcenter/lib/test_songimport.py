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
Package to test the openlp.plugins.planningcenter.lib.songimport package.
"""
import datetime
from unittest import TestCase
from unittest.mock import MagicMock, patch

from openlp.core.common.registry import Registry
from openlp.plugins.planningcenter.lib.songimport import PlanningCenterSongImport
from tests.helpers.testmixin import TestMixin


class TestSongImport(TestCase, TestMixin):
    """
    Test the PlanningcenterPlugin class
    """
    def setUp(self):
        """
        Create the class
        """
        mocked_settings = MagicMock()
        mocked_settings.value.return_value = 'english'
        Registry.create()
        self.registry = Registry()
        self.registry.register('settings', mocked_settings)
        self.registry.register('songs', MagicMock())
        self.song_import = PlanningCenterSongImport()

    def tearDown(self):
        """
        Delete all the C++ objects at the end so that we don't have a segfault
        """
        del self.song_import

    def test_add_song_without_lyrics(self):
        """
        Test that a song can be added with None lyrics
        """
        # GIVEN: A PlanningCenterSongImport Class
        # WHEN:  A song is added without lyrics
        item_title = 'Title'
        author = 'Author'
        lyrics = None
        theme_name = 'Theme Name'
        last_modified = datetime.datetime.now()
        with patch('openlp.plugins.songs.lib.importers.songimport.Song') as mock_song, \
                patch('openlp.plugins.songs.lib.importers.songimport.Author'):
            self.song_import.add_song(item_title, author, lyrics, theme_name, last_modified)
        # THEN:  A mock song has valid title, lyrics, and theme_name values
        self.assertEqual(mock_song.return_value.title, item_title, "Mock Song Title matches input title")
        self.assertTrue(item_title in mock_song.return_value.lyrics, "Mock Song Lyrics contain input title")
        self.assertEqual(mock_song.return_value.theme_name, theme_name, "Mock Song Theme matches input theme")

    def test_add_song_with_lyrics(self):
        """
        Test that a song can be added with lyrics
        """
        # GIVEN: A PlanningCenterSongImport Class
        # WHEN:  A song is added without lyrics
        item_title = 'Title'
        author = 'Author'
        lyrics = 'This is my song!'
        theme_name = 'Theme Name'
        last_modified = datetime.datetime.now()
        with patch('openlp.plugins.songs.lib.importers.songimport.Song') as mock_song, \
                patch('openlp.plugins.songs.lib.importers.songimport.Author'):
            self.song_import.add_song(item_title, author, lyrics, theme_name, last_modified)
        # THEN:  A mock song has valid title, lyrics, and theme_name values
        self.assertEqual(mock_song.return_value.title, item_title, "Mock Song Title matches input title")
        self.assertTrue(lyrics in mock_song.return_value.lyrics, "Mock Song Lyrics contain input lyrics")
        self.assertEqual(mock_song.return_value.theme_name, theme_name, "Mock Song Theme matches input theme")

    def test_add_song_with_verse(self):
        """
        Test that a song can be added with lyrics that contain a verse header
        """
        # GIVEN: A PlanningCenterSongImport Class
        # WHEN:  A song is added with lyrics that contain a verse tag
        item_title = 'Title'
        author = 'Author'
        lyrics = 'V1\nThis is my song!'
        theme_name = 'Theme Name'
        last_modified = datetime.datetime.now()
        with patch('openlp.plugins.songs.lib.importers.songimport.Song') as mock_song, \
                patch('openlp.plugins.songs.lib.importers.songimport.Author'):
            self.song_import.add_song(item_title, author, lyrics, theme_name, last_modified)
        # THEN:  A mock song has valid title, lyrics, and theme_name values
        self.assertEqual(mock_song.return_value.title, item_title,
                         "Mock Song Title matches input title")
        self.assertTrue("This is my song!" in mock_song.return_value.lyrics,
                        "Mock Song Lyrics contain input lyrics")
        self.assertTrue("type=\"v\"" in mock_song.return_value.lyrics,
                        "Mock Song Lyrics contain input verse")
        self.assertEqual(mock_song.return_value.theme_name, theme_name,
                         "Mock Song Theme matches input theme")

    def test_parse_lyrics_with_end_marker(self):
        """
        Test that a lyrics after an END marker are skipped
        """
        # GIVEN: A PlanningCenterSongImport Class
        # WHEN:  _split_lyrics_into_verses is called with lyrics that contain an END marker
        lyrics = 'This is my song!\n\n{<b>END</b>}\n\nSkip this part of the song'
        output_verses = self.song_import._split_lyrics_into_verses(lyrics)
        # THEN:  A mock song has valid title, lyrics, and theme_name values
        self.assertEqual(len(output_verses), 1, "A single verse is returned")
        self.assertTrue("This is my song!" in output_verses[0]['verse_text'], "Output lyrics contain input lyrics")
        self.assertFalse("END" in output_verses[0]['verse_text'], "Output Lyrics do not contain END")
        self.assertFalse("Skip this part of the song" in output_verses[0]['verse_text'], "Output Lyrics stop at end")

    def test_parse_lyrics_with_multiple_verses(self):
        """
        Test lyrics with verse marker inside
        """
        # GIVEN: A PlanningCenterSongImport Class
        # WHEN:  _split_lyrics_into_verses is called with lyrics that contain a verse marker inside (chorus)
        lyrics = 'First Verse\n\nChorus\nThis is my Chorus\n'
        output_verses = self.song_import._split_lyrics_into_verses(lyrics)
        # THEN:  A mock song has valid title, lyrics, and theme_name values
        self.assertEqual(len(output_verses), 2, "Two output verses are returned")
        self.assertEqual(output_verses[1]['verse_type'], 'c', "Second verse is a chorus")

    def test_parse_lyrics_with_single_spaced_verse_tags(self):
        """
        Test lyrics with verse marker inside
        """
        # GIVEN: A PlanningCenterSongImport Class
        # WHEN:  _split_lyrics_into_verses is called with lyrics that contain a verse marker inside (chorus)
        lyrics = 'V1\nFirst Verse\nV2\nSecondVerse\n'
        output_verses = self.song_import._split_lyrics_into_verses(lyrics)
        # THEN:  A mock song has valid title, lyrics, and theme_name values
        self.assertEqual(len(output_verses), 2, "Two output verses are returned")
