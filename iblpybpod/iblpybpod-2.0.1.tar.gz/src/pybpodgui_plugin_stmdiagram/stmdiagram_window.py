#!/usr/bin/python3
# -*- coding: utf-8 -*-

""" pycontrolgui_plugin_timeline.trials_plot"""
from pyforms.controls import ControlImage
from pyforms.controls import ControlCombo
from pyforms.basewidget import BaseWidget

from pybpodapi.com.messaging.state_occurrence import StateOccurrence
from pybpodapi.com.messaging.event_occurrence import EventOccurrence
from pybpodapi.com.messaging.event_resume import EventResume
from pybpodapi.com.messaging.session_info import SessionInfo
from pybpodgui_api.exceptions.run_setup import RunSetupError

import logging
import math
import pydot

from datetime import datetime as datetime_now

from confapp import conf

from AnyQt.QtCore import QTimer, QEventLoop

logger = logging.getLogger(__name__)


class StmDiagramWindow(BaseWidget):
    """ Show all boxes live state for an experiment"""

    COL_MSGTYPE = 0
    COL_PCTIME  = 1
    COL_INITTIME  = 2
    COL_FINALTIME = 3
    COL_MSG       = 4
    COL_INFO      = 5

    def __init__(self, session):
        """
        :param session: session reference
        :type session: pycontrolgui.windows.detail.entities.session_window.SessionWindow
        """
        super().__init__(session.name)
        self.session = session

        self._trials = ControlCombo('Trial', changed_event=self.__draw_diagram_evt)
        self._image  = ControlImage('Diagram')

        self.formset = ['_trials', '_image']

        self.__load_trials()
        self.__draw_diagram_evt()

    def __load_trials(self):
        self._trials.clear()

        res = self.session.data.query("TYPE in ['TRIAL']")

        for i, (index, msg) in enumerate( res.iterrows() ):
            
            self._trials.add_item(
                'Trial {0}'.format(i), index
            )
            
   
    def __draw_diagram_evt(self):
        trial_begin = self._trials.value
        trial_end   = None

        if trial_begin:
            trials = self._trials._items
            trials_indexes = sorted(trials.values())

            for trial_index in trials_indexes:
                if trial_index>trial_begin:
                    trial_end = trial_index
                    break

        if trial_end:
            indexes_filter = "index>{0} and index<{1}".format(trial_begin, trial_end)
        else:
            indexes_filter = "index>{0}".format(trial_begin)        

        if trial_end:
            query = "TYPE in ['TRANSITION'] and index>{0} and index<{1}".format(trial_begin, trial_end)
        else:
            query = "TYPE in ['TRANSITION'] and index>{0}".format(trial_begin)

        res = self.session.data.query("TYPE in ['EVENT-SUMMARY']").query(indexes_filter)
        events = []
        for _, msg in res.iterrows():
            events.append( (msg[self.COL_INITTIME], msg[self.COL_INFO]) )
        
        res = self.session.data.query("TYPE in ['TRANSITION']").query(indexes_filter)

        # this time, in graph_type we specify we want a DIrected GRAPH
        graph = pydot.Dot(graph_type='digraph', font='verdana')

        nodes  = {}
        states = res.MSG.unique()
        for state in states:
            node = pydot.Node(state, color='#ff4000')
            graph.add_node(node)
            nodes[state] = node

        prev = None
        curr = None

        curr_event = 0
        for i, (index, msg) in enumerate( res.iterrows() ):
            state = msg[self.COL_MSG]
            begin = msg[self.COL_INITTIME]

            if math.isnan(begin): continue

            curr  = nodes[state]

            for evt_i in range(curr_event, len(events) ):
                evt_end = events[evt_i][0]
                if evt_end<=begin:
                    evt_label  = events[evt_i][1]
                    curr_event = evt_i + 1
                    break

            if prev and curr:
                label = '   {0} ({1})'.format(evt_label, evt_end)
                graph.add_edge( pydot.Edge(prev, curr, label=label, fontsize="10.0", arrowhead='normal') )

            prev = curr

        
        graph.write_png('stm-diagram.png',prog='dot')

        # this is too good to be true!

        self._image.value = 'stm-diagram.png'



    def show(self, detached = False):
        if self.session.is_running and self.session.setup.detached:
            return
        
        # Prevent the call to be recursive because of the mdi_area
        if not detached:
            if hasattr(self, '_show_called'):
                BaseWidget.show(self)
                return
            self._show_called = True
            self.mainwindow.mdi_area += self
            del self._show_called
        else:
            BaseWidget.show(self)
        
        self._stop = False # flag used to close the gui in the middle of a loading
        

    def before_close_event(self):
        self.session.stmdiagram_action.setEnabled(True)






    @property
    def mainwindow(self):
        return self.session.mainwindow

    @property
    def title(self):
        return BaseWidget.title.fget(self)

    @title.setter
    def title(self, value):
        title = 'Stm: {0}'.format(value)
        BaseWidget.title.fset(self, title)
