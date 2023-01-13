#!/usr/bin/python3
# -*- coding: utf-8 -*-

""" pycontrolgui_plugin_timeline.trials_plot"""

from pyforms.controls import ControlEventsGraph
from pyforms.controls import ControlCheckBoxList
from pyforms.controls import ControlButton
from pyforms.basewidget import BaseWidget

from pybpodapi.com.messaging.state_occurrence import StateOccurrence
from pybpodapi.com.messaging.event_occurrence import EventOccurrence
from pybpodapi.com.messaging.event_resume import EventResume
from pybpodapi.com.messaging.session_info import SessionInfo
from pybpodgui_api.exceptions.run_setup import RunSetupError

import logging
import math
from datetime import datetime as datetime_now

from confapp import conf

from AnyQt.QtCore import QTimer, QEventLoop

logger = logging.getLogger(__name__)


class TrialsPlotWindow(BaseWidget):
    """ Show all boxes live state for an experiment"""

    EVENTS_TO_SHOW = [
        StateOccurrence,
        EventOccurrence
    ]

    def __init__(self, session):
        """
        :param session: session reference
        :type session: pycontrolgui.windows.detail.entities.session_window.SessionWindow
        """
        BaseWidget.__init__(self, session.name)
        self.session = session

        self._refreshbtn = ControlButton('Refresh Timeline')
        self._list = ControlCheckBoxList('Events to show')
        self._events = ControlEventsGraph(session.name)

        self._list.hide()
        self._events.add_popup_menu_option(
            'Show / Hide Events', self.__toggle_events_to_show_evt)
        self._events.add_track('')
        # for state_id, state_name in sorted(self.session.setup.board_task.states.items(), key=lambda x: x[0]):
        #	self._events.add_track(state_name)

        self._history_index = 0
        self._last_event = None
        self._session_start_timestamp = datetime_now.now()

        self.formset = ['_refreshbtn', '_list', '=', '_events']

        self._list_of_states_colors = [
            '#E0E0E0', '#FFCC99', '#FFFF99', 'CCFF99', '#99FFFF', '#99CCFF', '#FF99CC']

        self._states_names = {}

        self._timer = QTimer()
        self._timer.timeout.connect(self.read_message_queue)

        self._refreshbtn.value = self.__refresh_evt
        self._list.value = [
            (evt_type.__name__, True) for evt_type in self.EVENTS_TO_SHOW]
        self._list.changed_event = self.__list_changed_evt

        self._available_events = dict([
            (evt_type.__name__, evt_type) for evt_type in self.EVENTS_TO_SHOW])

        self.__list_changed_evt()

    def __refresh_evt(self):
        """Clears the entire timeline and re-draws all the checked events from T = 0 """
        self._events.clear()
        self._history_index = 0
        self.read_message_queue()

    def __list_changed_evt(self):
        self._events_2_draw = tuple([self._available_events[event_name]
                                     for event_name in self._list.value] + [SessionInfo])

    def __toggle_events_to_show_evt(self):
        if self._list.visible:
            self._list.hide()
        else:
            self._list.show()

    def show(self):
        # Prevent the call to be recursive because of the mdi_area
        if hasattr(self, '_show_called'):
            BaseWidget.show(self)
            return
        self._show_called = True
        self.mainwindow.mdi_area += self
        del self._show_called

        self._stop = False  # flag used to close the gui in the middle of a loading
        self.read_message_queue()
        if not self._stop:
            self._timer.start(conf.TIMELINE_PLUGIN_REFRESH_RATE)

    def hide(self):
        self._timer.stop()
        self._stop = True

    def before_close_event(self):
        self._timer.stop()
        self._stop = True
        self.session.trialsplot_action.setEnabled(True)

    def __add_event(self, start_timestamp, end_timestamp, track_id, name):

        self._last_event = self._events.add_event(
            start_timestamp,
            end_timestamp,
            track=track_id,
            title=name,
            color=self._list_of_states_colors[track_id % len(
                self._list_of_states_colors)]
        )
        self._events.value = start_timestamp

    def timediff_ms(self, time_f, time_i):
        diff = datetime_now.now()

        diff = time_f - time_i
        elapsed_ms = (diff.days * 86400000) + \
            (diff.seconds * 1000) + (diff.microseconds / 1000)
        return elapsed_ms

    def read_message_queue(self):
        """ Update board queue and retrieve most recent messages """

        try:
            recent_history = self.session.messages_history[self._history_index:]

            for message in recent_history:

                if self._stop:
                    return

                if not isinstance(message, self._events_2_draw):
                    continue

                if isinstance(message, StateOccurrence):
                    if message.state_name not in self._states_names.keys():
                        self._states_names[message.state_name] = len(
                            self._states_names)

                    if not (math.isnan(message.start_timestamp) or math.isnan(message.end_timestamp)):
                        bpod_start = int(round(message.start_timestamp * 1000))
                        bpod_end = int(round(message.end_timestamp * 1000))
                        self.__add_event(
                            bpod_start,
                            bpod_end,
                            self._states_names[message.state_name],
                            message.state_name
                        )

                elif isinstance(message, SessionInfo):
                    if message.content == 'SESSION-STARTED':
                        self._session_start_timestamp = message.pc_timestamp

                elif isinstance(message, EventOccurrence):
                    ts = None  # in case we don't find any valid timestamp, don't add the event to the timeline
                    # check which timestamp will be used. host timestamp wins over pc timestamp

                    if message.pc_timestamp is not None:
                        ts = self.timediff_ms(
                            message.pc_timestamp, self._session_start_timestamp)

                    # proceed if we have a valid timestamp
                    if ts is not None:
                        # create a new event slot in the timeline in case current message is entirely new
                        if message.event_name not in self._states_names.keys():
                            self._states_names[message.event_name] = len(
                                self._states_names)
                        # add a time delta to ts so the event can be shown in the timeline
                        self.__add_event(
                            ts - 10, ts + 10, self._states_names[message.event_name], message.event_name)

                self._history_index += 1
                QEventLoop()

        except RunSetupError as err:
            logger.error(str(err), exc_info=True)
            self._timer.stop()

    @property
    def mainwindow(self):
        return self.session.mainwindow

    @property
    def title(self):
        return BaseWidget.title.fget(self)

    @title.setter
    def title(self, value):
        title = 'Trials-plot: {0}'.format(value)
        BaseWidget.title.fset(self, title)
