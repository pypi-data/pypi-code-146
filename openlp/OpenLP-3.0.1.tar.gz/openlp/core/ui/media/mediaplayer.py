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
The :mod:`~openlp.core.ui.media.mediaplayer` module contains the MediaPlayer class.
"""
from openlp.core.common.mixins import RegistryProperties
from openlp.core.ui.media import MediaState


class MediaPlayer(RegistryProperties):
    """
    This is the base class media Player class to provide OpenLP with a pluggable media display framework.
    """

    def __init__(self, parent, name='media_player'):
        """
        Constructor
        """
        self.parent = parent
        self.name = name
        self.available = self.check_available()
        self.can_background = False
        self.can_folder = False
        self.state = {0: MediaState.Off, 1: MediaState.Off}
        self.has_own_widget = False

    def check_available(self):
        """
        Player is available on this machine
        """
        return False

    def setup(self, controller, display):
        """
        Create the related widgets for the current display

        :param controller: Which Controller is running the show.
        :param display: The display to be updated.
        """
        pass

    def load(self, controller, display, file):
        """
        Load a new media file and check if it is valid
        :param controller: Which Controller is running the show.
        :param display: The display to be updated.
        :param file: The file to be loaded
        """
        return True

    def resize(self, controller):
        """
        If the main display size or position is changed, the media widgets
        should also resized
        :param controller: Which Controller is running the show.
        """
        pass

    def play(self, controller, display):
        """
        Starts playing of current Media File, media player is expected to loop automatically

        :param controller: Which Controller is running the show.
        :param display: The display to be updated.
        """
        pass

    def pause(self, controller):
        """
        Pause of current Media File

        :param controller: Which Controller is running the show.
        """
        pass

    def stop(self, controller):
        """
        Stop playing of current Media File

        :param controller: Which Controller is running the show.
        """
        pass

    def volume(self, controller, volume):
        """
        Change volume of current Media File

        :param controller: Which Controller is running the show.
        :param volume: The volume to set.
        """
        pass

    def seek(self, controller, seek_value):
        """
        Change playing position of current Media File

        :param controller: Which Controller is running the show.
        :param seek_value: The where to seek to.
        """
        pass

    def reset(self, controller):
        """
        Remove the current loaded video

        :param controller: Which Controller is running the show.
        """
        pass

    def set_visible(self, controller, status):
        """
        Show/Hide the media widgets

        :param controller: Which Controller is running the show.
        :param status: The status to be set.
        """
        pass

    def update_ui(self, controller, output_display):
        """
        Do some ui related stuff (e.g. update the seek slider)

        :param controller: Which Controller is running the show.
        :param output_display: The display where the media is
        """
        pass

    def get_media_display_css(self):
        """
        Add css style sheets to htmlbuilder
        """
        return ''

    def get_media_display_javascript(self):
        """
        Add javascript functions to htmlbuilder
        """
        return ''

    def get_media_display_html(self):
        """
        Add html code to htmlbuilder
        """
        return ''

    def get_live_state(self):
        """
        Get the state of the live player
        :return: Live state
        """
        return self.state[0]

    def set_live_state(self, state):
        """
        Set the State of the Live player
        :param state: State to be set
        :return: None
        """
        self.state[0] = state

    def get_preview_state(self):
        """
        Get the state of the preview player
        :return: Preview State
        """
        return self.state[1]

    def set_preview_state(self, state):
        """
        Set the state of the Preview Player
        :param state: State to be set
        :return: None
        """
        self.state[1] = state

    def set_state(self, state, controller):
        """
        Set the State based on the display being processed within the controller
        :param state: State to be set
        :param controller: Identify the Display type
        :return: None
        """
        if controller.is_live:
            self.set_live_state(state)
        else:
            self.set_preview_state(state)
