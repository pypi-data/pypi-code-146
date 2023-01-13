# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
import os
import uuid
from pybpodgui_api.models.setup.board_task import BoardTask
from pybpodgui_api.models.session import Session
from pybpodgui_api.models.subject import Subject
from pybpodgui_api.utils.generate_name import generate_name

logger = logging.getLogger(__name__)


class SetupBase(object):

    def __init__(self, experiment):
        """
        :ivar Experiment experiment: Experiment to which the Setup belongs to
        """
        self.uuid4 = uuid.uuid4()
        self.name = generate_name([x.name for x in experiment.setups], "setup")
        self.detached = False

        self.experiment = experiment
        self.board_task = self.create_board_task()

        self._sessions = []
        self._subjects = []
        self.board = None
        self.task = None

        self.experiment += self

    ##########################################################################
    ####### PROPERTIES #######################################################
    ##########################################################################

    @property
    def name(self):
        """
        Get and set setup name

        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def subjects(self):
        """
        Get list of subjects

        :rtype: list(Subject)
        """
        return self._subjects

    @property
    def board(self):
        """
        Get and set setup board

        :rtype: Board
        """
        return self.board_task.board

    @board.setter
    def board(self, value):
        if isinstance(value, str):
            value = self.project.find_board(value)

        if self.board_task:
            self.board_task.board = value

    @property
    def task(self):
        """
        Get and set task

        :rtype: Task
        """
        return self.board_task.task

    @task.setter
    def task(self, value):
        if isinstance(value, str):
            value = self.project.find_task(value)

        if self.board_task:
            self.board_task.task = value

    @property
    def experiment(self):
        """
        Get and set the experiment

        :rtype: Experiment
        """
        return self._experiment

    @experiment.setter
    def experiment(self, value):
        self._experiment = value

    @property
    def project(self):
        """
        Get project

        :rtype: Project
        """
        return self.experiment.project

    @property
    def detached(self):
        return self._detached

    @detached.setter
    def detached(self, value):
        self._detached = value

    @property
    def sessions(self):
        """
        Get the list of sessions

        :rtype: list(Session)
        """
        return self._sessions

    @property
    def path(self):
        """
        Get and set setup path

        :rtype: str
        """
        if self.experiment.path is None:
            return None
        return os.path.join(self.experiment.path, 'setups', self.name)

    @property
    def last_session(self):
        """
        Get last created session

        :rtype: Session
        """
        try:
            order_sessions = sorted(self.sessions, key=lambda session: session.started)  # sort by end_date
            return order_sessions[-1]
        except IndexError:
            return None

    @property
    def net_port(self):
        if self.task and self.board:
            if self.task.trigger_softcodes:
                return self.board.net_port
            else:
                return None
        else:
            return None

    @property
    def update_variables(self):
        return self.board_task.update_variables

    ##########################################################################
    ####### FUNCTIONS ########################################################
    ##########################################################################

    def remove(self):
        """
        Remove the setup from the project
        """
        pass

    def create_board_task(self):
        """
        Create a new BoardTask object

        :rtype: BoardTask
        """
        return BoardTask(self)

    def create_session(self):
        """
        Create a new Session object

        :rtype: Session
        """
        return Session(self)

    def clear_subjects(self):
        # we need the copy because we are not allowed to change the same container that we are iterating
        subjects_copy = self.subjects.copy()
        for subj in subjects_copy:
            self -= subj

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.__unicode__()

    def __add__(self, obj):
        if isinstance(obj, Session) and obj not in self._sessions:
            self._sessions.append(obj)
        if isinstance(obj, Subject) and obj not in self._subjects:
            self._subjects.append(obj)
        if isinstance(obj, list):
            self._subjects.extend([x for x in obj if isinstance(x, Subject)])
        return self

    def __sub__(self, obj):
        if isinstance(obj, Session) and obj in self._sessions:
            self._sessions.remove(obj)
        if isinstance(obj, Subject) and obj in self._subjects:
            self._subjects.remove(obj)
        return self
