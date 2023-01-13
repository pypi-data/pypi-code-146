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
The :mod:`~openlp.core.display.window` module contains the display window
"""
import json
import logging
import os
import copy
import re

from PyQt5 import QtCore, QtWebChannel, QtWidgets

from openlp.core.common.applocation import AppLocation
from openlp.core.common.enum import ServiceItemType
from openlp.core.common.i18n import translate
from openlp.core.common.mixins import LogMixin, RegistryProperties
from openlp.core.common.path import path_to_str
from openlp.core.common.platform import is_win, is_macosx
from openlp.core.common.registry import Registry
from openlp.core.common.utils import wait_for
from openlp.core.display.screens import ScreenList
from openlp.core.ui import HideMode


FONT_FOUNDRY = re.compile(r'(.*?) \[(.*?)\]')
TRANSITION_END_EVENT_NAME = 'transparent_transition_end'
log = logging.getLogger(__name__)


class DisplayWatcher(QtCore.QObject):
    """
    This facilitates communication from the Display object in the browser back to the Python
    """
    initialised = QtCore.pyqtSignal(bool)

    def __init__(self, parent):
        super().__init__()
        self._display_window = parent
        self._transient_dispatch_events = {}
        self._permanent_dispatch_events = {}
        self._event_counter = 0

    @QtCore.pyqtSlot(bool)
    def setInitialised(self, is_initialised):
        """
        This method is called from the JS in the browser to set the _is_initialised attribute
        """
        log.info('Display is initialised: {init}'.format(init=is_initialised))
        self.initialised.emit(is_initialised)

    @QtCore.pyqtSlot()
    def pleaseRepaint(self):
        """
        Called from the js in the webengine view when it's requesting a repaint by Qt
        """
        self._display_window.webview.update()

    @QtCore.pyqtSlot(str, 'QJsonObject')
    def dispatchEvent(self, event_name, event_data):
        """
        Called from the js in the webengine view for event dispatches
        """
        transient_dispatch_events = self._transient_dispatch_events
        permanent_dispatch_events = self._permanent_dispatch_events
        if event_name in transient_dispatch_events:
            event = transient_dispatch_events[event_name]
            del transient_dispatch_events[event_name]
            event(event_data)
        if event_name in permanent_dispatch_events:
            permanent_dispatch_events[event_name](event_data)

    def register_event_listener(self, event_name, callback, transient=True):
        """
        Register an event listener from webengine view
        :param event_name: Event name
        :param callback: Callback listener when event happens
        :param transient: If the event listener should be unregistered after being run
        """
        if transient:
            events = self._transient_dispatch_events
        else:
            events = self._permanent_dispatch_events

        events[event_name] = callback

    def unregister_event_listener(self, event_name, transient=True):
        """
        Unregisters an event listener from webengine view
        :param event_name: Event name
        :param transient: If the event listener was registered as transient
        """
        if transient:
            events = self._transient_dispatch_events
        else:
            events = self._permanent_dispatch_events

        if event_name in events:
            del events[event_name]

    def get_unique_event_name(self):
        """
        Generates an unique event name
        :returns: Unique event name
        """
        event_count = self._event_counter
        self._event_counter += 1
        return 'event_' + str(event_count)


class DisplayWindow(QtWidgets.QWidget, RegistryProperties, LogMixin):
    """
    This is a window to show the output
    """
    def __init__(self, parent=None, screen=None, can_show_startup_screen=True, start_hidden=False,
                 after_loaded_callback=None):
        """
        Create the display window
        """
        super(DisplayWindow, self).__init__(parent)
        self.after_loaded_callback = after_loaded_callback
        # Gather all flags for the display window
        flags = QtCore.Qt.FramelessWindowHint | QtCore.Qt.Tool | QtCore.Qt.WindowStaysOnTopHint
        if self.settings.value('advanced/x11 bypass wm'):
            flags |= QtCore.Qt.X11BypassWindowManagerHint
        else:
            # This helps the window not being hidden by KDE's "Hide utility windows for inactive applications" option
            self.setAttribute(QtCore.Qt.WidgetAttribute.WA_X11NetWmWindowTypeDialog)
        if is_macosx():
            self.setAttribute(QtCore.Qt.WA_MacAlwaysShowToolWindow, True)
        # Need to import this inline to get around a QtWebEngine issue
        from openlp.core.display.webengine import WebEngineView
        self._is_initialised = False
        self._is_manual_close = False
        self._can_show_startup_screen = can_show_startup_screen
        self._fbo = None
        self.setWindowTitle(translate('OpenLP.DisplayWindow', 'Display Window'))
        self.setWindowFlags(flags)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setAutoFillBackground(True)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.webview = WebEngineView(self)
        self.webview.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.webview.page().setBackgroundColor(QtCore.Qt.transparent)
        self.webview.display_clicked = self.disable_display
        self.layout.addWidget(self.webview)
        self.webview.loadFinished.connect(self.after_loaded)
        display_base_path = AppLocation.get_directory(AppLocation.AppDir) / 'core' / 'display' / 'html'
        self.display_path = display_base_path / 'display.html'
        self.checkerboard_path = display_base_path / 'checkerboard.png'
        self.openlp_splash_screen_path = display_base_path / 'openlp-splash-screen.png'
        self.channel = QtWebChannel.QWebChannel(self)
        self.display_watcher = DisplayWatcher(self)
        self.channel.registerObject('displayWatcher', self.display_watcher)
        self.webview.page().setWebChannel(self.channel)
        self.display_watcher.initialised.connect(self.on_initialised)
        self.set_url(QtCore.QUrl.fromLocalFile(path_to_str(self.display_path)))
        self.is_display = False
        self.scale = 1
        self.hide_mode = None
        self.__script_done = True
        self.__script_result = None
        if screen and screen.is_display:
            # use log_debug to set up function wrapping before registering functions
            self.log_debug('registering live display show/hide functions')
            Registry().register_function('live_display_hide', self.hide_display)
            Registry().register_function('live_display_show', self.show_display)
            self.update_from_screen(screen)
            self.is_display = True
            # Only make visible on single monitor setup if setting enabled.
            if not start_hidden and (len(ScreenList()) > 1 or self.settings.value('core/display on monitor')):
                self.show()

    def closeEvent(self, event):
        """
        Override the closeEvent method to prevent the window from being closed by the user
        """
        if not self._is_manual_close:
            event.ignore()

    def _fix_font_name(self, font_name):
        """
        Do some font machinations to see if we can fix the font name
        """
        # Some fonts on Windows that end in "Bold" are made into a base font that is bold
        if is_win() and font_name.endswith(' Bold'):
            font_name = font_name.split(' Bold')[0]
        # Some fonts may have the Foundry name in their name. Remove the foundry name
        match = FONT_FOUNDRY.match(font_name)
        if match:
            font_name = match.group(1)
        return font_name

    def deregister_display(self):
        """
        De-register this displays callbacks in the registry to be able to remove it
        """
        if self.is_display:
            Registry().remove_function('live_display_hide', self.hide_display)
            Registry().remove_function('live_display_show', self.show_display)
        self._is_manual_close = True

    @property
    def is_initialised(self):
        return self._is_initialised

    def on_initialised(self, is_initialised):
        """
        Update the initialised status
        """
        self._is_initialised = is_initialised

    def update_from_screen(self, screen):
        """
        Update the number and the geometry from the screen.

        :param Screen screen: A `~openlp.core.display.screens.Screen` instance
        """
        self.setGeometry(screen.display_geometry)
        self.screen_number = screen.number

    def set_background_image(self, image_path):
        image_uri = image_path.as_uri()
        self.run_javascript('Display.setBackgroundImage("{image}");'.format(image=image_uri))

    def set_single_image(self, bg_color, image_path):
        """
        :param str bg_color: Background color
        :param Path image_path: Path to the image
        """
        image_uri = image_path.as_uri()
        self.run_javascript('Display.setFullscreenImage("{bg_color}", "{image}");'.format(bg_color=bg_color,
                                                                                          image=image_uri))

    def set_single_image_data(self, bg_color, image_data):
        self.run_javascript('Display.setFullscreenImageFromData("{bg_color}", '
                            '"{image_data}");'.format(bg_color=bg_color, image_data=image_data))

    def set_startup_screen(self):
        bg_color = self.settings.value('core/logo background color')
        image = self.settings.value('core/logo file')
        if path_to_str(image).startswith(':'):
            image = self.openlp_splash_screen_path
        try:
            image_uri = image.as_uri()
        except Exception:
            image_uri = ''
        # if set to hide logo on startup, do not send the logo
        if self.settings.value('core/logo hide on startup'):
            image_uri = ''
        self.run_javascript('Display.setStartupSplashScreen("{bg_color}", "{image}");'.format(bg_color=bg_color,
                                                                                              image=image_uri))

    def set_url(self, url):
        """
        Set the URL of the webview

        :param QtCore.QUrl | str url: The URL to set
        """
        if not isinstance(url, QtCore.QUrl):
            url = QtCore.QUrl(url)
        self.webview.setUrl(url)

    def set_html(self, html):
        """
        Set the html
        """
        self.webview.setHtml(html)

    def after_loaded(self):
        """
        Add stuff after page initialisation
        """
        js_is_display = str(self.is_display).lower()
        item_transitions = str(self.settings.value('themes/item transitions')).lower()
        hide_mouse = str(self.settings.value('advanced/hide mouse') and self.is_display).lower()
        slide_numbers_in_footer = str(self.settings.value('advanced/slide numbers in footer')).lower()
        self.run_javascript('Display.init({{'
                            'isDisplay: {is_display},'
                            'doItemTransitions: {do_item_transitions},'
                            'slideNumbersInFooter: {slide_numbers_in_footer},'
                            'hideMouse: {hide_mouse}'
                            '}});'
                            .format(is_display=js_is_display, do_item_transitions=item_transitions,
                                    slide_numbers_in_footer=slide_numbers_in_footer, hide_mouse=hide_mouse))
        wait_for(lambda: self._is_initialised)
        if self.scale != 1:
            self.set_scale(self.scale)
        if self._can_show_startup_screen:
            self.set_startup_screen()
        if self.after_loaded_callback:
            self.after_loaded_callback()

    def run_javascript(self, script, is_sync=False):
        """
        Run some Javascript in the WebView

        :param script: The script to run, a string
        :param is_sync: Run the script synchronously. Defaults to False
        """
        log.debug((script[:80] + '..') if len(script) > 80 else script)
        # Wait for previous scripts to finish
        wait_for(lambda: self.__script_done)
        if is_sync:
            self.__script_done = False
            self.__script_result = None

            def handle_result(result):
                """
                Handle the result from the asynchronous call
                """
                self.__script_done = True
                self.__script_result = result

            self.webview.page().runJavaScript(script, handle_result)
            # Wait for script to finish
            if not wait_for(lambda: self.__script_done):
                self.__script_done = True
            return self.__script_result
        else:
            self.webview.page().runJavaScript(script)
        self.raise_()

    def go_to_slide(self, verse):
        """
        Go to a particular slide.

        :param str verse: The verse to go to, e.g. "V1" for songs, or just "0" for other types
        """
        self.run_javascript('Display.goToSlide("{verse}");'.format(verse=verse))

    def load_verses(self, verses, is_sync=False):
        """
        Set verses in the display
        """
        json_verses = json.dumps(verses)
        self.run_javascript('Display.setTextSlides({verses});'.format(verses=json_verses), is_sync=is_sync)

    def load_images(self, images):
        """
        Set images in the display
        """
        imagesr = copy.deepcopy(images)
        for image in imagesr:
            image['path'] = image['path'].as_uri()
            # Not all images has a dedicated thumbnail (such as images loaded from old or local servicefiles),
            # in that case reuse the image
            if image.get('thumbnail', None):
                image['thumbnail'] = image['thumbnail'].as_uri()
            else:
                image['thumbnail'] = image['path']
        json_images = json.dumps(imagesr)
        self.run_javascript('Display.setImageSlides({images});'.format(images=json_images))

    def load_video(self, video):
        """
        Load video in the display
        """
        video = copy.deepcopy(video)
        video['path'] = video['path'].as_uri()
        json_video = json.dumps(video)
        self.run_javascript('Display.setVideo({video});'.format(video=json_video))

    def play_video(self):
        """
        Play the currently loaded video
        """
        self.run_javascript('Display.playVideo();')

    def pause_video(self):
        """
        Pause the currently playing video
        """
        self.run_javascript('Display.pauseVideo();')

    def stop_video(self):
        """
        Stop the currently playing video
        """
        self.run_javascript('Display.stopVideo();')

    def set_video_playback_rate(self, rate):
        """
        Set the playback rate of the current video.

        The rate can be any valid float, with 0.0 being stopped, 1.0 being normal speed,
        over 1.0 is faster, under 1.0 is slower, and negative is backwards.

        :param rate: A float indicating the playback rate.
        """
        self.run_javascript('Display.setPlaybackRate({rate});'.format(rate=rate))

    def set_video_volume(self, level):
        """
        Set the volume of the current video.

        The volume should be an int from 0 to 100, where 0 is no sound and 100 is maximum volume. Any
        values outside this range will raise a ``ValueError``.

        :param level: A number between 0 and 100
        """
        if level < 0 or level > 100:
            raise ValueError('Volume should be from 0 to 100, was "{}"'.format(level))
        self.run_javascript('Display.setVideoVolume({level});'.format(level=level))

    def toggle_video_mute(self):
        """
        Toggle the mute of the current video
        """
        self.run_javascript('Display.toggleVideoMute();')

    def save_screenshot(self, fname=None):
        """
        Save a screenshot, either returning it or saving it to file
        """
        pixmap = self.grab()
        if fname:
            ext = os.path.splitext(fname)[-1][1:]
            pixmap.save(fname, ext)
        else:
            return pixmap

    def set_theme(self, theme, is_sync=False, service_item_type=False):
        """
        Set the theme of the display
        """
        theme_copy = copy.deepcopy(theme)
        if self.is_display:
            if service_item_type == ServiceItemType.Text:
                if theme.background_type == 'video' or theme.background_type == 'stream':
                    theme_copy.background_type = 'transparent'
        else:
            # If preview Display with media background we just show the background color, no media
            if theme.background_type == 'stream' or theme.background_type == 'video':
                theme_copy.background_type = 'solid'
                theme_copy.background_start_color = theme.background_border_color
                theme_copy.background_end_color = theme.background_border_color
                theme_copy.background_main_color = theme.background_border_color
                theme_copy.background_footer_color = theme.background_border_color
                theme_copy.background_color = theme.background_border_color
            # If preview Display for media so we need to display black box.
            elif service_item_type == ServiceItemType.Command or theme.background_type == 'live':
                theme_copy.background_type = 'solid'
                theme_copy.background_start_color = '#590909'
                theme_copy.background_end_color = '#590909'
                theme_copy.background_main_color = '#090909'
                theme_copy.background_footer_color = '#090909'
        # Do some font-checking, see https://gitlab.com/openlp/openlp/-/issues/39
        theme_copy.font_main_name = self._fix_font_name(theme.font_main_name)
        theme_copy.font_footer_name = self._fix_font_name(theme.font_footer_name)
        exported_theme = theme_copy.export_theme(is_js=True)
        self.run_javascript('Display.setTheme({theme});'.format(theme=exported_theme), is_sync=is_sync)

    def reload_theme(self):
        """
        Applies the set theme
        DO NOT use this when changing slides. Only use this if you need to force an update
        to the current visible slides.
        """
        self.run_javascript('Display.resetTheme();')

    def get_video_types(self):
        """
        Get the types of videos playable by the embedded media player
        """
        return self.run_javascript('Display.getVideoTypes();', is_sync=True)

    def show_display(self):
        """
        Show the display
        """
        if self.is_display:
            # Only make visible on single monitor setup if setting enabled.
            if len(ScreenList()) == 1 and not self.settings.value('core/display on monitor'):
                return
        # Aborting setVisible(False) call in case the display modes are changed quickly
        self.display_watcher.unregister_event_listener(TRANSITION_END_EVENT_NAME)
        if self.isHidden():
            self.setVisible(True)
        self.run_javascript('Display.show();')
        self.hide_mode = None

    def hide_display(self, mode=HideMode.Screen):
        """
        Hide the display by making all layers transparent Store the images so they can be replaced when required

        :param mode: How the screen is to be hidden
        """
        log.debug('hide_display mode = {mode:d}'.format(mode=mode))
        if self.is_display:
            # Only make visible on single monitor setup if setting enabled.
            if len(ScreenList()) == 1 and not self.settings.value('core/display on monitor'):
                return
        # Aborting setVisible(False) call in case the display modes are changed quickly
        self.display_watcher.unregister_event_listener(TRANSITION_END_EVENT_NAME)
        # Update display to the selected mode
        if mode != HideMode.Screen:
            if self.isHidden():
                self.setVisible(True)
        if mode == HideMode.Screen:
            if self.settings.value('advanced/disable transparent display'):
                # Hide window only after all webview CSS ransitions are done
                self.display_watcher.register_event_listener(TRANSITION_END_EVENT_NAME,
                                                             lambda _: self.setVisible(False))
                self.run_javascript("Display.toTransparent('{}');".format(TRANSITION_END_EVENT_NAME))
            else:
                self.run_javascript('Display.toTransparent();')
        elif mode == HideMode.Blank:
            self.run_javascript('Display.toBlack();')
        elif mode == HideMode.Theme:
            self.run_javascript('Display.toTheme();')
        self.hide_mode = mode

    def disable_display(self):
        """
        Removes the display if showing desktop
        This allows users to click though the screen even if the screen is only transparent
        """
        if self.is_display and self.hide_mode == HideMode.Screen:
            self.setVisible(False)

    def finish_with_current_item(self):
        """
        This is called whenever the song/image display is followed by eg a presentation or video which
        has its own display.
        This function ensures that the current item won't flash momentarily when the webengineview
        is displayed for a subsequent song or image.
        """
        self.run_javascript('Display.finishWithCurrentItem();', True)
        self.webview.update()

    def set_scale(self, scale):
        """
        Set the HTML scale
        """
        self.scale = scale
        # Only scale if initialised (scale run again once initialised)
        if self._is_initialised:
            self.run_javascript('Display.setScale({scale});'.format(scale=scale * 100))

    def alert(self, text, settings):
        """
        Set an alert
        """
        self.run_javascript('Display.alert("{text}", {settings});'.format(text=text, settings=settings))
