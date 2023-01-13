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
The :mod:`~openlp.plugins.songs.forms.songselectform` module contains the GUI for the SongSelect importer
"""
import logging

from PyQt5 import QtCore, QtWidgets
from sqlalchemy.sql import and_

from openlp.core.common.i18n import translate
from openlp.core.common.mixins import RegistryProperties
from openlp.plugins.songs.forms.songselectdialog import Ui_SongSelectDialog
from openlp.plugins.songs.lib.db import Song
from openlp.plugins.songs.lib.songselect import SongSelectImport, Pages

log = logging.getLogger(__name__)


class SongSelectForm(QtWidgets.QDialog, Ui_SongSelectDialog, RegistryProperties):
    """
    The :class:`SongSelectForm` class is the SongSelect dialog.
    """

    def __init__(self, parent=None, plugin=None, db_manager=None):
        QtWidgets.QDialog.__init__(self, parent, QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint |
                                   QtCore.Qt.WindowCloseButtonHint)
        self.plugin = plugin
        self.db_manager = db_manager
        self.setup_ui(self)

    def initialise(self):
        """
        Initialise the SongSelectForm
        """
        self.song = None
        self.song_select_importer = SongSelectImport(self.db_manager, self.webview)
        self.url_bar.returnPressed.connect(self.on_url_bar_return_pressed)
        self.view_button.clicked.connect(self.on_view_button_clicked)
        self.back_button.clicked.connect(self.on_back_button_clicked)
        self.close_button.clicked.connect(self.done)
        self.import_button.clicked.connect(self.on_import_button_clicked)
        self.webview.page().loadStarted.connect(self.page_load_started)
        self.webview.page().loadFinished.connect(self.page_loaded)

    def exec(self):
        """
        Execute the dialog. This method sets everything back to its initial
        values.
        """
        self.song_select_importer.reset_webview()
        self.view_button.setEnabled(False)
        self.back_button.setEnabled(False)
        self.import_button.setEnabled(False)
        self.stacked_widget.setCurrentIndex(0)
        return QtWidgets.QDialog.exec(self)

    def done(self, result_code):
        """
        Log out of SongSelect.

        :param result_code: The result of the dialog.
        """
        return QtWidgets.QDialog.done(self, result_code)

    def page_load_started(self):
        self.song_progress_bar.setMaximum(0)
        self.song_progress_bar.setValue(0)
        self.song_progress_bar.setVisible(True)
        self.url_bar.setVisible(False)
        self.import_button.setEnabled(False)
        self.view_button.setEnabled(False)
        self.back_button.setEnabled(False)
        self.message_area.setText('')

    def page_loaded(self, successful):
        self.song = None
        page_type = self.song_select_importer.get_page_type()
        if page_type == Pages.Login:
            self.signin_page_loaded()
        elif page_type == Pages.Song:
            self.song_progress_bar.setMaximum(3)
            self.song_progress_bar.setValue(0)
            self.song = self.song_select_importer.get_song(self._update_song_progress)
            if self.song:
                self.import_button.setEnabled(True)
                self.view_button.setEnabled(True)
            else:
                message = translate('SongsPlugin.SongSelectForm', 'This song cannot be read. Perhaps your CCLI account '
                                                                  'does not give you access to this song.')
                self.message_area.setText(message)
            self.back_button.setEnabled(True)
        if page_type == Pages.Other:
            self.back_button.setEnabled(True)
        self.song_progress_bar.setVisible(False)
        self.url_bar.setText(self.webview.url().toString())
        self.url_bar.setCursorPosition(0)
        self.url_bar.setVisible(True)

    def signin_page_loaded(self):
        username = self.settings.value('songs/songselect username')
        password = self.settings.value('songs/songselect password')
        self.song_select_importer.set_login_fields(username, password)

    def _update_song_progress(self):
        """
        Update the progress bar.
        """
        self.song_progress_bar.setValue(self.song_progress_bar.value() + 1)
        self.application.process_events()

    def _view_song(self):
        """
        Load a song into the song view.
        """
        if not self.song:
            QtWidgets.QMessageBox.critical(
                self, translate('SongsPlugin.SongSelectForm', 'Incomplete song'),
                translate('SongsPlugin.SongSelectForm', 'This song is missing some information, like the lyrics, '
                                                        'and cannot be imported.'),
                QtWidgets.QMessageBox.StandardButtons(QtWidgets.QMessageBox.Ok), QtWidgets.QMessageBox.Ok)
            return
        # Clear up the UI
        self.author_list_widget.clear()
        self.lyrics_table_widget.clear()
        self.lyrics_table_widget.setRowCount(0)
        # Update the UI
        self.title_edit.setText(self.song['title'])
        self.copyright_edit.setText(self.song['copyright'])
        self.ccli_edit.setText(self.song['ccli_number'])
        for author in self.song['authors']:
            self.author_list_widget.addItem(QtWidgets.QListWidgetItem(author, self.author_list_widget))
        for counter, verse in enumerate(self.song['verses']):
            self.lyrics_table_widget.setRowCount(self.lyrics_table_widget.rowCount() + 1)
            item = QtWidgets.QTableWidgetItem(verse['lyrics'])
            item.setData(QtCore.Qt.UserRole, verse['label'])
            item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
            self.lyrics_table_widget.setItem(counter, 0, item)
        self.lyrics_table_widget.setVerticalHeaderLabels([verse['label'] for verse in self.song['verses']])
        self.lyrics_table_widget.resizeRowsToContents()
        self.lyrics_table_widget.scrollToTop()
        self.stacked_widget.setCurrentIndex(1)

    def on_url_bar_return_pressed(self):
        """
        Go to the url in the url bar
        """
        url = self.url_bar.text()
        self.song_select_importer.set_page(url)

    def on_view_button_clicked(self):
        """
        Import a song from SongSelect.
        """
        self.view_button.setEnabled(False)
        self.url_bar.setEnabled(False)
        self._view_song()

    def on_back_button_clicked(self, force_return_to_home=False):
        """
        Go back to the search page or just to the webview if on the preview screen
        """
        if (self.stacked_widget.currentIndex() == 0 or force_return_to_home):
            self.song_select_importer.set_home_page()
        else:
            self.view_button.setEnabled(True)
            self.url_bar.setEnabled(True)
        self.stacked_widget.setCurrentIndex(0)

    def on_import_button_clicked(self):
        """
        Import a song from SongSelect.
        """
        # Warn user if a song exists in the database with the same ccli_number
        songs_with_same_ccli_number = self.plugin.manager.get_all_objects(
            Song, and_(Song.ccli_number.like(self.song['ccli_number']), Song.ccli_number != ''))
        if len(songs_with_same_ccli_number) > 0:
            continue_import = QtWidgets.QMessageBox.question(self,
                                                             translate('SongsPlugin.SongSelectForm',
                                                                       'Song Duplicate Warning'),
                                                             translate('SongsPlugin.SongSelectForm',
                                                                       'A song with the same CCLI number is already in '
                                                                       'your database.\n\n'
                                                                       'Are you sure you want to import this song?'),
                                                             defaultButton=QtWidgets.QMessageBox.No)
            if continue_import == QtWidgets.QMessageBox.No:
                return
        self.song_select_importer.save_song(self.song)
        self.song = None
        QtWidgets.QMessageBox.information(self, translate('SongsPlugin.SongSelectForm', 'Song Imported'),
                                          translate('SongsPlugin.SongSelectForm',
                                                    'Your song has been imported'))
        self.on_back_button_clicked(True)
