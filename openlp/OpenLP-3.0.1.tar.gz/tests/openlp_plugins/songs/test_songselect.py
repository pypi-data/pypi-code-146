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
This module contains tests for the CCLI SongSelect importer.
It needs re-writing at some point to load real HTML pages from disk and
then test the behaviour based on those. That way if and when CCLI change
their page layout, changing the tests would just be a case of
re-downloading the HTML pages and changing the code to use the new layout.
"""
from unittest import TestCase
from unittest.mock import MagicMock, patch, sentinel

from PyQt5 import QtWidgets, QtCore

from openlp.core.common.registry import Registry
from openlp.plugins.songs.forms.songselectform import SongSelectForm
from openlp.plugins.songs.lib import Song
from openlp.plugins.songs.lib.songselect import BASE_URL, LOGIN_PAGE, Pages, SongSelectImport
from tests.helpers.songfileimport import SongImportTestHelper
from tests.helpers.testmixin import TestMixin
from tests.utils.constants import RESOURCE_PATH


TEST_PATH = RESOURCE_PATH / 'songs' / 'songselect'


class TestSongSelectImport(TestCase, TestMixin):
    """
    Test the :class:`~openlp.plugins.songs.lib.songselect.SongSelectImport` class
    """
    def test_constructor(self):
        """
        Test that constructing a basic SongSelectImport object works correctly
        """
        # GIVEN: The SongSelectImporter class and a mocked out build_opener
        # WHEN: An object is instantiated
        importer = SongSelectImport(sentinel.db_manager, sentinel.webview)

        # THEN: The object should have the correct properties
        assert importer.db_manager is sentinel.db_manager, 'The db_manager should be set'
        assert importer.webview is sentinel.webview, 'The webview should be set'

    def test_get_page_type_login(self):
        """
        Test get_page_type to spot the login page
        """
        # GIVEN: A importer object, and a mocked url
        importer = SongSelectImport(None, None)
        url = QtCore.QUrl('https://profile.ccli.com/account/signin?appContext=SongSelect&'
                          'returnUrl=https%3a%2f%2fsongselect.ccli.com%2f')
        page = MagicMock(url=MagicMock(return_value=url))
        importer.webview = MagicMock(page=MagicMock(return_value=page))

        # WHEN: The method is run
        result = importer.get_page_type()

        # THEN: The correct type should be returned
        assert result == Pages.Login

    def test_get_page_type_home(self):
        """
        Test get_page_type to spot the home page
        """
        # GIVEN: A importer object, and a mocked url
        importer = SongSelectImport(None, None)
        url = QtCore.QUrl('https://songselect.ccli.com')
        page = MagicMock(url=MagicMock(return_value=url))
        importer.webview = MagicMock(page=MagicMock(return_value=page))

        # WHEN: The method is run
        result = importer.get_page_type()

        # THEN: The correct type should be returned
        assert result == Pages.Home

    def test_get_page_type_search(self):
        """
        Test get_page_type to spot the search page
        """
        # GIVEN: A importer object, and a mocked url
        importer = SongSelectImport(None, None)
        url = QtCore.QUrl('https://songselect.ccli.com/search/results?SearchText=test')
        page = MagicMock(url=MagicMock(return_value=url))
        importer.webview = MagicMock(page=MagicMock(return_value=page))

        # WHEN: The method is run
        result = importer.get_page_type()

        # THEN: The correct type should be returned
        assert result == Pages.Search

    def test_get_page_type_song(self):
        """
        Test get_page_type to spot the login page
        """
        # GIVEN: A importer object, and a mocked url
        importer = SongSelectImport(None, None)
        url = QtCore.QUrl('https://songselect.ccli.com/Songs/7115744/song_name/view_lyrics')
        page = MagicMock(url=MagicMock(return_value=url))
        importer.webview = MagicMock(page=MagicMock(return_value=page))

        # WHEN: The method is run
        result = importer.get_page_type()

        # THEN: The correct type should be returned
        assert result == Pages.Song

    def test_get_page_type_other(self):
        """
        Test get_page_type to spot the login page
        """
        # GIVEN: A importer object, and a mocked url
        importer = SongSelectImport(None, None)
        url = QtCore.QUrl('https://openlp.org')
        page = MagicMock(url=MagicMock(return_value=url))
        importer.webview = MagicMock(page=MagicMock(return_value=page))

        # WHEN: The method is run
        result = importer.get_page_type()

        # THEN: The correct type should be returned
        assert result == Pages.Other

    @patch('openlp.plugins.songs.lib.songselect.wait_for')
    def test_run_javascript(self, mocked_wait_for):
        """
        Test run javascript calls the page object
        """
        # GIVEN: A importer object and mocked run js fn
        def runJs(script, handle_result):
            handle_result('processed_{}'.format(script))
        importer = SongSelectImport(None, None)
        importer.webview = MagicMock()
        page = MagicMock()
        page.runJavaScript = runJs
        importer.webview.page.return_value = page

        # WHEN: The set login field method is called
        result = importer._run_javascript('2 + 2')

        # THEN: The javascript should have been called on the page object
        assert result == 'processed_2 + 2'

    def test_reset_webview(self):
        """
        Check that the setUrl method is called when the reset webview method is called
        """
        # GIVEN: A importer object and mock webview
        importer = SongSelectImport(None, None)
        importer.webview = MagicMock()

        # WHEN: The reset_webview method is called
        importer.reset_webview()

        # THEN: The setUrl function should have been called
        importer.webview.setUrl.assert_called_with(QtCore.QUrl(LOGIN_PAGE))

    @patch('openlp.plugins.songs.lib.songselect.SongSelectImport.set_page')
    def test_set_home_page(self, mocked_set_page):
        """
        Test that when the home method is called, it attempts to go to the home page
        """
        # GIVEN: A importer object
        importer = SongSelectImport(None, None)

        # WHEN: The home method is called
        importer.set_home_page()

        # THEN: set_page is called once with the base url
        mocked_set_page.assert_called_with(BASE_URL)

    @patch('openlp.plugins.songs.lib.songselect.SongSelectImport._run_javascript')
    def test_set_page(self, mocked_run_js):
        """
        Test set page runs the correct script
        """
        # GIVEN: A importer object
        importer = SongSelectImport(None, None)

        # WHEN: The set login field method is called
        importer.set_page('my_new_page')

        # THEN: The javascript called should contain the correct values
        mocked_run_js.assert_called_with('document.location = "my_new_page"')

    @patch('openlp.plugins.songs.lib.songselect.SongSelectImport._run_javascript')
    def test_set_login_fields(self, mocked_run_js):
        """
        Test correct js is sent to set login fields
        """
        # GIVEN: A importer object
        importer = SongSelectImport(None, None)

        # WHEN: The set login field method is called
        importer.set_login_fields('my_username', 'my_password')

        # THEN: The javascript called should contain the correct values
        mocked_run_js.assert_called_with(('document.getElementById("EmailAddress").value = "my_username";'
                                          'document.getElementById("Password").value = "my_password";'
                                          ))

    @patch('openlp.plugins.songs.lib.songselect.SongSelectImport._run_javascript')
    @patch('openlp.plugins.songs.lib.songselect.wait_for')
    def test_get_page(self, mocked_wait_for, mocked_run_js):
        """
        Test get page sends js requests
        """
        # GIVEN: A importer object
        importer = SongSelectImport(None, None)
        mocked_run_js.return_value = True

        # WHEN: The get page method is called
        importer.get_page("https://example.com")

        # THEN: The javascript should be run
        assert mocked_run_js.call_count == 2, 'Should be called once for request and once for fetch'
        mocked_wait_for.assert_called_once()

    def test_get_song_number_from_url(self):
        """
        Test the ccli number can be correctly obtained from a url
        """
        # GIVEN: A importer object
        importer = SongSelectImport(None, None)

        # WHEN: The function is called with a valid url
        result = importer.get_song_number_from_url('https://songselect.ccli.com/Songs/7115744/way-maker')

        # THEN: The ccli number is returned
        assert result == '7115744', 'Should have found the ccli number from the url'

    def test_get_song_number_from_url_nonumber(self):
        """
        Test the ccli number function returns None when no number is found
        """
        # GIVEN: A importer object
        importer = SongSelectImport(None, None)

        # WHEN: The function is called with a valid url
        result = importer.get_song_number_from_url('https://songselect.ccli.com/search/results?SearchText=song+7115744')

        # THEN: The returned value should be None
        assert result is None

    @patch('openlp.plugins.songs.lib.songselect.SongSelectImport.get_song_number_from_url')
    @patch('openlp.plugins.songs.lib.songselect.SongSelectImport.get_page')
    def test_get_song_page_raises_exception(self, mocked_get_page, mock_get_num):
        """
        Test that when BeautifulSoup gets a bad song page the get_song() method returns None
        """
        # GIVEN: A mocked callback and an importer object
        mocked_get_page.side_effect = None
        mocked_callback = MagicMock()
        importer = SongSelectImport(None, MagicMock())

        # WHEN: get_song is called
        result = importer.get_song(callback=mocked_callback)

        # THEN: The callback should have been called once and None should be returned
        mocked_callback.assert_called_with()
        assert result is None, 'The get_song() method should have returned None'

    @patch('openlp.plugins.songs.lib.songselect.SongSelectImport.get_song_number_from_url')
    @patch('openlp.plugins.songs.lib.songselect.SongSelectImport.get_page')
    @patch('openlp.plugins.songs.lib.songselect.BeautifulSoup')
    def test_get_song_lyrics_raise_exception(self, MockedBeautifulSoup, mocked_get_page, mock_get_num):
        """
        Test that when BeautifulSoup gets a bad lyrics page the get_song() method returns None
        """
        # GIVEN: A bunch of mocked out stuff and an importer object
        song_page = MagicMock(return_value={'href': '/lyricpage'})
        MockedBeautifulSoup.side_effect = [song_page, TypeError('Test Error')]
        mocked_callback = MagicMock()
        importer = SongSelectImport(None, MagicMock())

        # WHEN: get_song is called
        result = importer.get_song(callback=mocked_callback)

        # THEN: The callback should have been called twice and None should be returned
        assert 2 == mocked_callback.call_count, 'The callback should have been called twice'
        assert result is None, 'The get_song() method should have returned None'

    @patch('openlp.plugins.songs.lib.songselect.log.exception')
    @patch('openlp.plugins.songs.lib.songselect.SongSelectImport.get_song_number_from_url')
    @patch('openlp.plugins.songs.lib.songselect.SongSelectImport.get_page')
    def test_get_song_no_access(self, mocked_get_page, mock_get_num, mock_log_exception):
        """
        Test that the get_song() handles the case when the user's CCLI account has no access to the song
        """
        fake_song_page = '''<!DOCTYPE html><html><body>
        <div class="content-title">
          <h1>Song Title</h1>
          <ul class="authors">
            <li><a>Author 1</a></li>
            <li><a>Author 2</a></li>
          </ul>
        </div>
        <div class="song-content-data"><ul><li><strong>1234_cclinumber_5678</strong></li></ul></div>
        <section class="page-section">
          <a title="View song lyrics" data-open="ssUpgradeModal"></a>
        </section>
        <ul class="song-meta-list">
          <li>Themes</li><li><a>theme1</a></li><li><a>theme2</a></li>
        </ul>
        </body></html>
        '''
        fake_lyrics_page = '''<!DOCTYPE html><html><body>
        <div class="song-viewer lyrics">
            <h3>Verse 1</h3>
            <p>verse thing 1<br>line 2</p>
            <h3>Verse 2</h3>
            <p>verse thing 2</p>
        </div>
        <ul class="copyright">
          <li>Copy thing</li><li>Copy thing 2</li>
        </ul>
        </body></html>
        '''
        mocked_get_page.side_effect = [fake_song_page, fake_lyrics_page]
        mocked_callback = MagicMock()
        importer = SongSelectImport(None, MagicMock())

        # WHEN: get_song is called
        result = importer.get_song(callback=mocked_callback)

        # THEN: None should be returned
        assert result is None, 'The get_song() method should have returned None'

    @patch('openlp.plugins.songs.lib.songselect.SongSelectImport.get_song_number_from_url')
    @patch('openlp.plugins.songs.lib.songselect.SongSelectImport.get_page')
    def test_get_song(self, mocked_get_page, mock_get_num):
        """
        Test that the get_song() method returns the correct song details
        """
        fake_song_page = '''<!DOCTYPE html><html><body>
        <div class="content-title">
          <h1>Song Title</h1>
          <ul class="authors">
            <li><a>Author 1</a></li>
            <li><a>Author 2</a></li>
          </ul>
        </div>
        <div class="song-content-data"><ul><li><strong>1234_cclinumber_5678</strong></li></ul></div>
        <section class="page-section">
          <a title="View song lyrics" href="pretend link"></a>
        </section>
        <ul class="song-meta-list">
          <li>Themes</li><li><a>theme1</a></li><li><a>theme2</a></li>
        </ul>
        </body></html>
        '''
        fake_lyrics_page = '''<!DOCTYPE html><html><body>
        <div class="song-viewer lyrics">
            <h3>Verse 1</h3>
            <p>verse thing 1<br>line 2</p>
            <h3>Verse 2</h3>
            <p>verse thing 2</p>
            <h3>Spoken Words</h3>
            <p>completely custom verse type</p>
        </div>
        <ul class="copyright">
          <li>Copy thing</li><li>Copy thing 2</li>
        </ul>
        </body></html>
        '''
        mocked_get_page.side_effect = [fake_song_page, fake_lyrics_page]
        mocked_callback = MagicMock()
        importer = SongSelectImport(None, MagicMock())

        # WHEN: get_song is called
        result = importer.get_song(callback=mocked_callback)

        # THEN: The callback should have been called three times and the song should be returned
        assert 3 == mocked_callback.call_count, 'The callback should have been called twice'
        assert result is not None, 'The get_song() method should have returned a song dictionary'
        assert result['title'] == 'Song Title'
        assert result['authors'] == ['Author 1', 'Author 2']
        assert result['copyright'] == 'Copy thing/Copy thing 2'
        assert result['topics'] == ['theme1', 'theme2']
        assert result['ccli_number'] == '1234_cclinumber_5678'
        assert result['verses'] == [{'label': 'Verse 1', 'lyrics': 'verse thing 1\nline 2'},
                                    {'label': 'Verse 2', 'lyrics': 'verse thing 2'},
                                    {'label': 'Spoken Words', 'lyrics': 'completely custom verse type'}]

    @patch('openlp.plugins.songs.lib.songselect.clean_song')
    @patch('openlp.plugins.songs.lib.songselect.Topic')
    @patch('openlp.plugins.songs.lib.songselect.Author')
    def test_save_song_new_author(self, MockedAuthor, MockedTopic, mocked_clean_song):
        """
        Test that saving a song with a new author performs the correct actions
        """
        # GIVEN: A song to save, and some mocked out objects
        song_dict = {
            'title': 'Arky Arky',
            'authors': ['Public Domain'],
            'verses': [
                {'label': 'Verse 1', 'lyrics': 'The Lord told Noah: there\'s gonna be a floody, floody'},
                {'label': 'Chorus 1', 'lyrics': 'So, rise and shine, and give God the glory, glory'},
                {'label': 'Verse 2', 'lyrics': 'The Lord told Noah to build him an arky, arky'}
            ],
            'copyright': 'Public Domain',
            'ccli_number': '123456'
        }
        MockedAuthor.display_name.__eq__.return_value = False
        MockedTopic.name.__eq__.return_value = False
        mocked_db_manager = MagicMock()
        mocked_db_manager.get_object_filtered.return_value = None
        importer = SongSelectImport(mocked_db_manager, MagicMock())

        # WHEN: The song is saved to the database
        result = importer.save_song(song_dict)

        # THEN: The return value should be a Song class and the mocked_db_manager should have been called
        assert isinstance(result, Song), 'The returned value should be a Song object'
        mocked_clean_song.assert_called_with(mocked_db_manager, result)
        assert 2 == mocked_db_manager.save_object.call_count, \
            'The save_object() method should have been called twice'
        mocked_db_manager.get_object_filtered.assert_called_with(MockedAuthor, False)
        MockedAuthor.populate.assert_called_with(first_name='Public', last_name='Domain', display_name='Public Domain')
        assert 1 == len(result.authors_songs), 'There should only be one author'

    @patch('openlp.plugins.songs.lib.songselect.clean_song')
    @patch('openlp.plugins.songs.lib.songselect.Author')
    def test_save_song_existing_author(self, MockedAuthor, mocked_clean_song):
        """
        Test that saving a song with an existing author performs the correct actions
        """
        # GIVEN: A song to save, and some mocked out objects
        song_dict = {
            'title': 'Arky Arky',
            'authors': ['Public Domain'],
            'verses': [
                {'label': 'Verse 1', 'lyrics': 'The Lord told Noah: there\'s gonna be a floody, floody'},
                {'label': 'Chorus 1', 'lyrics': 'So, rise and shine, and give God the glory, glory'},
                {'label': 'Verse 2', 'lyrics': 'The Lord told Noah to build him an arky, arky'}
            ],
            'copyright': 'Public Domain',
            'ccli_number': '123456'
        }
        MockedAuthor.display_name.__eq__.return_value = False
        mocked_db_manager = MagicMock()
        mocked_db_manager.get_object_filtered.return_value = MagicMock()
        importer = SongSelectImport(mocked_db_manager, MagicMock())

        # WHEN: The song is saved to the database
        result = importer.save_song(song_dict)

        # THEN: The return value should be a Song class and the mocked_db_manager should have been called
        assert isinstance(result, Song), 'The returned value should be a Song object'
        mocked_clean_song.assert_called_with(mocked_db_manager, result)
        assert 2 == mocked_db_manager.save_object.call_count, \
            'The save_object() method should have been called twice'
        mocked_db_manager.get_object_filtered.assert_called_with(MockedAuthor, False)
        assert 0 == MockedAuthor.populate.call_count, 'A new author should not have been instantiated'
        assert 1 == len(result.authors_songs), 'There should only be one author'

    @patch('openlp.plugins.songs.lib.songselect.clean_song')
    @patch('openlp.plugins.songs.lib.songselect.Author')
    def test_save_song_unknown_author(self, MockedAuthor, mocked_clean_song):
        """
        Test that saving a song with an author name of only one word performs the correct actions
        """
        # GIVEN: A song to save, and some mocked out objects
        song_dict = {
            'title': 'Arky Arky',
            'authors': ['Unknown'],
            'verses': [
                {'label': 'Verse 1', 'lyrics': 'The Lord told Noah: there\'s gonna be a floody, floody'},
                {'label': 'Chorus 1', 'lyrics': 'So, rise and shine, and give God the glory, glory'},
                {'label': 'Verse 2', 'lyrics': 'The Lord told Noah to build him an arky, arky'}
            ],
            'copyright': 'Public Domain',
            'ccli_number': '123456'
        }
        MockedAuthor.display_name.__eq__.return_value = False
        mocked_db_manager = MagicMock()
        mocked_db_manager.get_object_filtered.return_value = None
        importer = SongSelectImport(mocked_db_manager, MagicMock())

        # WHEN: The song is saved to the database
        result = importer.save_song(song_dict)

        # THEN: The return value should be a Song class and the mocked_db_manager should have been called
        assert isinstance(result, Song), 'The returned value should be a Song object'
        mocked_clean_song.assert_called_with(mocked_db_manager, result)
        assert 2 == mocked_db_manager.save_object.call_count, \
            'The save_object() method should have been called twice'
        mocked_db_manager.get_object_filtered.assert_called_with(MockedAuthor, False)
        MockedAuthor.populate.assert_called_with(first_name='Unknown', last_name='', display_name='Unknown')
        assert 1 == len(result.authors_songs), 'There should only be one author'

    @patch('openlp.plugins.songs.lib.songselect.clean_song')
    @patch('openlp.plugins.songs.lib.songselect.Topic')
    @patch('openlp.plugins.songs.lib.songselect.Author')
    def test_save_song_topics(self, MockedAuthor, MockedTopic, mocked_clean_song):
        """
        Test that saving a song with topics performs the correct actions
        Also check that a verse with no number is retitled to 1
        """
        # GIVEN: A song to save, and some mocked out objects
        song_dict = {
            'title': 'Arky Arky',
            'authors': ['Public Domain'],
            'verses': [
                {'label': 'Verse', 'lyrics': 'The Lord told Noah: there\'s gonna be a floody, floody'},
                {'label': 'Chorus 1', 'lyrics': 'So, rise and shine, and give God the glory, glory'},
                {'label': 'Verse 2', 'lyrics': 'The Lord told Noah to build him an arky, arky'}
            ],
            'copyright': 'Public Domain',
            'ccli_number': '123456',
            'topics': ['Old Testement', 'Flood']
        }

        def save_object(b):
            b.topics = []
        MockedAuthor.display_name.__eq__.return_value = False
        MockedTopic.name.__eq__.return_value = False
        mocked_db_manager = MagicMock()
        mocked_db_manager.get_object_filtered.return_value = None
        mocked_db_manager.save_object = save_object
        importer = SongSelectImport(mocked_db_manager, MagicMock())

        # WHEN: The song is saved to the database
        result = importer.save_song(song_dict)

        # THEN: The return value should be a Song class and the topics should have been added
        assert isinstance(result, Song), 'The returned value should be a Song object'
        mocked_clean_song.assert_called_with(mocked_db_manager, result)
        assert MockedTopic.populate.call_count == 2, 'Should have created 2 new topics'
        MockedTopic.populate.assert_called_with(name='Flood')
        assert 1 == len(result.authors_songs), 'There should only be one author'


class TestSongSelectForm(TestCase, TestMixin):
    """
    Test the :class:`~openlp.plugins.songs.forms.songselectform.SongSelectForm` class
    """
    def setUp(self):
        """
        Some set up for this test suite
        """
        self.setup_application()
        self.app.setApplicationVersion('0.0')
        self.app.process_events = lambda: None
        Registry.create()
        Registry().register('application', self.app)
        Registry().register('settings', MagicMock())
        self.grid_patcher = patch('openlp.plugins.songs.forms.songselectdialog.QtWidgets.QGridLayout')
        self.web_patcher = patch('openlp.plugins.songs.forms.songselectdialog.WebEngineView')
        self.vbox_patcher = patch('openlp.plugins.songs.forms.songselectdialog.QtWidgets.QVBoxLayout')
        self.grid_patcher.start()
        self.web_patcher.start()
        self.vbox_patcher.start()

    def tearDown(self):
        self.grid_patcher.stop()
        self.web_patcher.stop()
        self.vbox_patcher.stop()

    def test_create_form(self):
        """
        Test that we can create the SongSelect form
        """
        # GIVEN: The SongSelectForm class and a mocked db manager
        mocked_plugin = MagicMock()
        mocked_db_manager = MagicMock()

        # WHEN: We create an instance
        ssform = SongSelectForm(None, mocked_plugin, mocked_db_manager)

        # THEN: The correct properties should have been assigned
        assert mocked_plugin == ssform.plugin, 'The correct plugin should have been assigned'
        assert mocked_db_manager == ssform.db_manager, 'The correct db_manager should have been assigned'

    @patch('openlp.plugins.songs.lib.songselect.SongSelectImport')
    def test_initialise(self, mocked_ss_import):
        """
        Test the initialise method
        """
        # GIVEN: The SongSelectForm
        ssform = SongSelectForm(None, MagicMock(), MagicMock())

        # WHEN: The initialise method is run
        ssform.initialise()

        # THEN: The import object should exist, song var should be None, and the page hooked up
        assert ssform.song is None
        assert isinstance(ssform.song_select_importer, SongSelectImport), 'SongSelectImport object should be created'
        assert ssform.webview.page.call_count == 2, 'Page should be called twice, once for each load handler'

    @patch('openlp.plugins.songs.forms.songselectform.QtWidgets.QDialog.exec')
    def test_exec(self, mocked_exec):
        """
        Test the exec method
        """
        # GIVEN: The SongSelectForm
        ssform = SongSelectForm(None, MagicMock(), MagicMock())
        ssform.song_select_importer = MagicMock()
        ssform.stacked_widget = MagicMock()

        # WHEN: The initialise method is run
        ssform.exec()

        # THEN: Should have reset webview, set stack to 0 and pass on the event
        ssform.song_select_importer.reset_webview.assert_called_once()
        ssform.stacked_widget.setCurrentIndex.assert_called_with(0)
        mocked_exec.assert_called_once()

    @patch('openlp.plugins.songs.forms.songselectform.QtWidgets.QDialog.done')
    @patch('openlp.plugins.songs.forms.songselectform.QtWidgets.QProgressDialog')
    def test_done(self, mocked_prog_dialog, mocked_done):
        """
        Test the done method closes th dialog
        """
        # GIVEN: The SongSelectForm
        ssform = SongSelectForm(None, MagicMock(), MagicMock())
        ssform.song_select_importer = MagicMock()

        # WHEN: The initialise method is run
        ssform.done('result')

        # THEN: Should have passed on the event
        mocked_done.assert_called_once()

    def test_page_load_started(self):
        """
        Test the page_load_started method
        """
        # GIVEN: The SongSelectForm
        ssform = SongSelectForm(None, MagicMock(), MagicMock())
        ssform.song_progress_bar = MagicMock()
        ssform.import_button = MagicMock()
        ssform.view_button = MagicMock()
        ssform.back_button = MagicMock()
        ssform.url_bar = MagicMock()
        ssform.message_area = MagicMock()

        # WHEN: The method is run
        ssform.page_load_started()

        # THEN: The UI should be set up accordingly (working bar and disabled buttons)
        ssform.song_progress_bar.setMaximum.assert_called_with(0)
        ssform.song_progress_bar.setVisible.assert_called_with(True)
        ssform.import_button.setEnabled.assert_called_with(False)
        ssform.view_button.setEnabled.assert_called_with(False)
        ssform.back_button.setEnabled.assert_called_with(False)
        ssform.message_area.setText.assert_called_with('')

    def test_page_loaded_login(self):
        """
        Test the page_loaded method for a "Login" page
        """
        # GIVEN: The SongSelectForm and mocked login page
        ssform = SongSelectForm(None, MagicMock(), MagicMock())
        ssform.song_select_importer = MagicMock()
        ssform.song_select_importer.get_page_type.return_value = Pages.Login
        ssform.signin_page_loaded = MagicMock()
        ssform.url_bar = MagicMock()

        # WHEN: The method is run
        ssform.page_loaded(True)

        # THEN: The signin page method should be called
        ssform.signin_page_loaded.assert_called_once()

    def test_page_loaded_song(self):
        """
        Test the page_loaded method for a "Song" page
        """
        # GIVEN: The SongSelectForm and mocked song page
        ssform = SongSelectForm(None, MagicMock(), MagicMock())
        ssform.song_select_importer = MagicMock()
        ssform.song_select_importer.get_page_type.return_value = Pages.Song
        ssform.song_progress_bar = MagicMock()
        ssform.url_bar = MagicMock()

        # WHEN: The method is run
        ssform.page_loaded(True)

        # THEN: Progress bar should have been set max 3 (for loading song)
        ssform.song_progress_bar.setMaximum.assert_called_with(3)
        ssform.song_progress_bar.setVisible.call_count == 2

    @patch('openlp.plugins.songs.forms.songselectform.translate')
    def test_page_loaded_song_no_access(self, mocked_translate):
        """
        Test the page_loaded method for a "Song" page to which the CCLI account has no access
        """
        # GIVEN: The SongSelectForm and mocked song page and translate function
        ssform = SongSelectForm(None, MagicMock(), MagicMock())
        ssform.song_select_importer = MagicMock()
        ssform.song_select_importer.get_page_type.return_value = Pages.Song
        ssform.song_select_importer.get_song.return_value = None
        ssform.song_progress_bar = MagicMock()
        ssform.url_bar = MagicMock()
        ssform.message_area = MagicMock()
        mocked_translate.return_value = 'some message'

        # WHEN: The method is run
        ssform.page_loaded(True)

        # THEN: The no access message should be shown and the progress bar should be less than 3
        ssform.message_area.setText.assert_called_with('some message')
        ssform.song_progress_bar.setValue.call_count < 4

    def test_page_loaded_other(self):
        """
        Test the page_loaded method for an "Other" page
        """
        # GIVEN: The SongSelectForm and mocked other page
        ssform = SongSelectForm(None, MagicMock(), MagicMock())
        ssform.song_select_importer = MagicMock()
        ssform.song_select_importer.get_page_type.return_value = Pages.Other
        ssform.song_progress_bar = MagicMock()
        ssform.back_button = MagicMock()
        ssform.url_bar = MagicMock()

        # WHEN: The method is run
        ssform.page_loaded(True)

        # THEN: Back button should be available
        ssform.back_button.setEnabled.assert_called_with(True)

    def test_signin_page_loaded(self):
        """
        Test that the signin_page_loaded method calls the appropriate method
        """
        # GIVEN: The SongSelectForm and mocked settings
        ssform = SongSelectForm(None, MagicMock(), MagicMock())
        ssform.song_select_importer = MagicMock()
        ssform.settings.value = MagicMock(side_effect=['user', 'pass'])

        # WHEN: The method is run
        ssform.signin_page_loaded()

        # THEN: Correct values should have been sent from the settings
        ssform.song_select_importer.set_login_fields.assert_called_with('user', 'pass')

    @patch('openlp.plugins.songs.forms.songselectdialog.QtWidgets.QListWidgetItem')
    def test_view_song(self, mock_qtlist):
        """
        Test that the _view_song method does the important stuff
        """
        # GIVEN: The SongSelectForm, mocks and a song
        ssform = SongSelectForm(None, MagicMock(), MagicMock())
        ssform.stacked_widget = MagicMock()
        ssform.title_edit = MagicMock()
        ssform.copyright_edit = MagicMock()
        ssform.ccli_edit = MagicMock()
        ssform.lyrics_table_widget = MagicMock()
        ssform.author_list_widget = MagicMock()
        ssform.song = {
            'title': 'Song Title',
            'copyright': 'copy thing',
            'ccli_number': '1234',
            'authors': ['Bob', 'Jo'],
            'verses': [{'lyrics': 'hello', 'label': 'Verse 1'}]
        }

        # WHEN: The method is run
        ssform._view_song()

        # THEN: Page should have changed in the stacked widget and ui should have been updated
        ssform.stacked_widget.setCurrentIndex.assert_called_with(1)
        ssform.title_edit.setText.assert_called_with('Song Title')
        ssform.copyright_edit.setText.assert_called_with('copy thing')
        ssform.ccli_edit.setText.assert_called_with('1234')
        assert ssform.lyrics_table_widget.setItem.call_count > 0
        assert ssform.author_list_widget.addItem.call_count > 0

    @patch('openlp.plugins.songs.forms.songselectform.QtWidgets.QMessageBox.critical')
    def test_view_song_invalid(self, mock_message):
        """
        Test that the _view_song doesn't mess up when the song doesn't exist
        """
        # GIVEN: The SongSelectForm, mocks and a song
        ssform = SongSelectForm(None, MagicMock(), MagicMock())
        ssform.stacked_widget = MagicMock()
        ssform.song = None

        # WHEN: The method is run
        ssform._view_song()

        # THEN: Page should not have changed and a warning should show
        assert ssform.stacked_widget.setCurrentIndex.call_count == 0
        mock_message.assert_called_once()

    def test_on_url_bar_return_pressed(self):
        """
        Test that the on_url_bar_return_pressed method changes the page
        """
        # GIVEN: The SongSelectForm, mocks and a song
        ssform = SongSelectForm(None, MagicMock(), MagicMock())
        ssform.url_bar = MagicMock()
        ssform.url_bar.text.return_value = "test"
        ssform.song_select_importer = MagicMock()

        # WHEN: The method is run
        ssform.on_url_bar_return_pressed()

        # THEN: Page should not have changed and a warning should show
        ssform.song_select_importer.set_page.assert_called_with("test")

    @patch('openlp.plugins.songs.forms.songselectform.and_')
    @patch('openlp.plugins.songs.forms.songselectform.Song')
    @patch('openlp.plugins.songs.forms.songselectform.QtWidgets.QMessageBox.information')
    @patch('openlp.plugins.songs.forms.songselectform.QtWidgets.QMessageBox.question')
    @patch('openlp.plugins.songs.forms.songselectform.translate')
    def test_on_import(self, mocked_trans, mocked_quest, mocked_info, mocked_song, mocked_and):
        """
        Test that when a song is imported and the user clicks the "yes" button, the UI goes back to the previous page
        """
        # GIVEN: A valid SongSelectForm with a mocked out QMessageBox.question() method
        mocked_trans.side_effect = lambda *args: args[1]
        mocked_quest.return_value = QtWidgets.QMessageBox.Yes
        ssform = SongSelectForm(None, MagicMock(), MagicMock())
        mocked_song_select_importer = MagicMock()
        ssform.song_select_importer = mocked_song_select_importer
        ssform.song = {'ccli_number': '1234'}

        # WHEN: The import button is clicked, and the user clicks Yes
        with patch.object(ssform, 'on_back_button_clicked') as mocked_on_back_button_clicked:
            ssform.on_import_button_clicked()

        # THEN: The on_back_button_clicked() method should have been called
        mocked_song_select_importer.save_song.assert_called_with({'ccli_number': '1234'})
        mocked_quest.assert_not_called()
        mocked_info.assert_called_once()
        mocked_on_back_button_clicked.assert_called_with(True)
        assert ssform.song is None

    @patch('openlp.plugins.songs.forms.songselectform.len')
    @patch('openlp.plugins.songs.forms.songselectform.and_')
    @patch('openlp.plugins.songs.forms.songselectform.Song')
    @patch('openlp.plugins.songs.forms.songselectform.QtWidgets.QMessageBox.information')
    @patch('openlp.plugins.songs.forms.songselectform.QtWidgets.QMessageBox.question')
    @patch('openlp.plugins.songs.forms.songselectform.translate')
    def test_on_import_duplicate_yes_clicked(self, mock_trans, mock_q, mocked_info, mock_song, mock_and, mock_len):
        """
        Test that when a duplicate song is imported and the user clicks the "yes" button, the song is imported
        """
        # GIVEN: A valid SongSelectForm with a mocked out QMessageBox.question() method
        mock_len.return_value = 1
        mock_trans.side_effect = lambda *args: args[1]
        mock_q.return_value = QtWidgets.QMessageBox.Yes
        ssform = SongSelectForm(None, MagicMock(), MagicMock())
        mocked_song_select_importer = MagicMock()
        ssform.song_select_importer = mocked_song_select_importer
        ssform.song = {'ccli_number': '1234'}

        # WHEN: The import button is clicked, and the user clicks Yes
        with patch.object(ssform, 'on_back_button_clicked') as mocked_on_back_button_clicked:
            ssform.on_import_button_clicked()

        # THEN: Should have been saved and the on_back_button_clicked() method should have been called
            mocked_song_select_importer.save_song.assert_called_with({'ccli_number': '1234'})
            mock_q.assert_called_once()
            mocked_info.assert_called_once()
            mocked_on_back_button_clicked.assert_called_once()
            assert ssform.song is None

    @patch('openlp.plugins.songs.forms.songselectform.len')
    @patch('openlp.plugins.songs.forms.songselectform.and_')
    @patch('openlp.plugins.songs.forms.songselectform.Song')
    @patch('openlp.plugins.songs.forms.songselectform.QtWidgets.QMessageBox.information')
    @patch('openlp.plugins.songs.forms.songselectform.QtWidgets.QMessageBox.question')
    @patch('openlp.plugins.songs.forms.songselectform.translate')
    def test_on_import_duplicate_no_clicked(self, mock_trans, mock_q, mocked_info, mock_song, mock_and, mock_len):
        """
        Test that when a duplicate song is imported and the user clicks the "no" button, the UI exits
        """
        # GIVEN: A valid SongSelectForm with a mocked out QMessageBox.question() method
        mock_len.return_value = 1
        mock_trans.side_effect = lambda *args: args[1]
        mock_q.return_value = QtWidgets.QMessageBox.No
        ssform = SongSelectForm(None, MagicMock(), MagicMock())
        mocked_song_select_importer = MagicMock()
        ssform.song_select_importer = mocked_song_select_importer
        ssform.song = {'ccli_number': '1234'}

        # WHEN: The import button is clicked, and the user clicks No
        with patch.object(ssform, 'on_back_button_clicked') as mocked_on_back_button_clicked:
            ssform.on_import_button_clicked()

        # THEN: Should have not been saved
            assert mocked_song_select_importer.save_song.call_count == 0
            mock_q.assert_called_once()
            mocked_info.assert_not_called()
            mocked_on_back_button_clicked.assert_not_called()
            assert ssform.song is not None

    def test_on_back_button_clicked_preview(self):
        """
        Test that when the back button is clicked on preview screen, the stacked widget is set back one page
        """
        # GIVEN: A SongSelect form, stacked widget on page 1
        ssform = SongSelectForm(None, MagicMock(), MagicMock())
        ssimporter = MagicMock()
        ssform.song_select_importer = MagicMock()
        ssform.song_select_importer.set_home_page = ssimporter
        with patch.object(ssform, 'stacked_widget') as mocked_stacked_widget:
            mocked_stacked_widget.currentIndex.return_value = 1

        # WHEN: The preview back button is clicked
            ssform.on_back_button_clicked()

        # THEN: The stacked widget should be set back one page and webpage is NOT put back to the home page
        mocked_stacked_widget.setCurrentIndex.assert_called_with(0)
        ssimporter.assert_not_called()

    def test_on_back_button_clicked_force(self):
        """
        Test that when the back button method is triggered with the force param set,
        the page should be changed
        """
        # GIVEN: A SongSelect form, stacked widget on page 1
        ssform = SongSelectForm(None, MagicMock(), MagicMock())
        ssimporter = MagicMock()
        ssform.song_select_importer = MagicMock()
        ssform.song_select_importer.set_home_page = ssimporter
        with patch.object(ssform, 'stacked_widget') as mocked_stacked_widget:
            mocked_stacked_widget.currentIndex.return_value = 1

        # WHEN: The preview back button is clicked with force param
            ssform.on_back_button_clicked(True)

        # THEN: The stacked widget should be set back one page and webpage is NOT put back to the home page
        mocked_stacked_widget.setCurrentIndex.assert_called_with(0)
        ssimporter.assert_called_once()

    def test_on_back_button_clicked(self):
        """
        Test that when the back button is clicked, the stacked widget is set to page 0
        and set to home page
        """
        # GIVEN: A SongSelect form, stacked widget on page 0
        ssform = SongSelectForm(None, MagicMock(), MagicMock())
        ssimporter = MagicMock()
        ssform.song_select_importer = MagicMock()
        ssform.song_select_importer.set_home_page = ssimporter
        with patch.object(ssform, 'stacked_widget') as mocked_stacked_widget:
            mocked_stacked_widget.currentIndex.return_value = 0

        # WHEN: The back button is clicked
            ssform.on_back_button_clicked()

        # THEN: The stacked widget should be set back one page
        mocked_stacked_widget.setCurrentIndex.assert_called_with(0)
        ssimporter.assert_called_with()

    def test_update_song_progress(self):
        """
        Test the _update_song_progress() method
        """
        # GIVEN: A SongSelect form
        ssform = SongSelectForm(None, MagicMock(), MagicMock())

        # WHEN: _update_song_progress() is called
        with patch.object(ssform, 'song_progress_bar') as mocked_song_progress_bar:
            mocked_song_progress_bar.value.return_value = 2
            ssform._update_song_progress()

        # THEN: The song progress bar should be updated
            mocked_song_progress_bar.setValue.assert_called_with(3)

    def test_on_view_button_clicked(self):
        """
        Test that view song function is run when the view button is clicked
        """
        # GIVEN: A SongSelect form
        ssform = SongSelectForm(None, MagicMock(), MagicMock())

        # WHEN: A song result is double-clicked
        with patch.object(ssform, '_view_song') as mocked_view_song:
            ssform.on_view_button_clicked()

        # THEN: The song is fetched and shown to the user
        mocked_view_song.assert_called_with()


def test_songselect_file_import():
    """
    Test that loading a SongSelect file works correctly on various files
    """
    with SongImportTestHelper('CCLIFileImport', 'cclifile') as helper:
        helper.file_import([TEST_PATH / 'TestSong.bin'],
                           helper.load_external_result_data(TEST_PATH / 'TestSong-bin.json'))
        helper.file_import([TEST_PATH / 'TestSong.txt'],
                           helper.load_external_result_data(TEST_PATH / 'TestSong-txt.json'))
