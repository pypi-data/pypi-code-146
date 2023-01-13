# !/usr/bin/python3
# -*- coding: utf-8 -*-


import os
import datetime
import logging
from confapp import conf

logger = logging.getLogger(__name__)


class SessionBase(object):
    """
    Represents a board running session
    """

    def __init__(self, setup):
        setup += self
        self.uuid4 = None  # the session will only gain a uuid4 after the session is executed

        self.data = None
        self.setup = setup
        self.name = self.__default_name(setup)
        self.creator = ''
        self.setup_name = setup.name
        self.board_name = setup.board.name if setup.board else None
        self.task_name = setup.task.name if setup.task else None
        self.board_serial_port = setup.board.serial_port if setup.board else None
        self.started = datetime.datetime.now()
        self.ended = None
        self.messages_history = []
        self.subjects = []
        self.filepath = None
        self.variables = []
        self.user = None

    def __default_name(self, setup):
        name = conf.PYBPODGUI_API_DEFAULT_SESSION_NAME
        name = name.replace('[datetime]', datetime.datetime.now().strftime('%Y%m%d-%H%M%S'))
        name = name.replace('[project]', setup.experiment.project.name)
        name = name.replace('[experiment]', setup.experiment.name)
        name = name.replace('[setup]', setup.name)
        name = name.replace('[protocol]', setup.task.name if setup.task is not None else 'None')
        name = name.replace('[subjects]', '.'.join([s.name for s in setup.subjects]))
        return name

    ##########################################################################
    ####### PROPERTIES #######################################################
    ##########################################################################

    def __add__(self, value):
        self._messages_history.append(value)
        return self

    def remove(self):
        """
        Remove the session from the project

        """
        pass

    @property
    def setup(self):
        """
        Get and set the setup

        :rtype: Setup
        """
        return self._setup

    @setup.setter
    def setup(self, value):
        self._setup = value

    @property
    def name(self):
        """
        Get and set session name

        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def subjects(self):
        """
        Get and set session name

        :rtype:
        """
        return self._subjects

    @subjects.setter
    def subjects(self, value):
        self._subjects = value

    @property
    def path(self):
        """
        Get and set path name

        :rtype: str
        """
        if self.setup.path is None:
            return None
        return os.path.join(self.setup.path, 'sessions', self.name)

    @property
    def filepath(self):
        return self._filepath

    @filepath.setter
    def filepath(self, value):
        self._filepath = value

    @property
    def variables(self):
        return self._variables

    @variables.setter
    def variables(self, value):
        self._variables = value

    @property
    def setup_name(self):
        """
        Get and set setup name

        :rtype: str
        """
        return self._setup_name

    @setup_name.setter
    def setup_name(self, value):
        self._setup_name = value

    @property
    def board_name(self):
        """
        Get and set board name

        :rtype: str
        """
        return self._board_name

    @board_name.setter
    def board_name(self, value):
        self._board_name = value

    @property
    def task_name(self):
        """
        Get and set the task name

        :rtype: str
        """
        return self._task_name

    @task_name.setter
    def task_name(self, value):
        self._task_name = value

    @property
    def board_serial_port(self):
        """
        Get and set board serial port

        :rtype: str
        """
        return self._board_serial_port

    @board_serial_port.setter
    def board_serial_port(self, value):
        self._board_serial_port = value

    @property
    def started(self):
        """
        Get and set the start datetime of the session

        :rtype: datetime.datetime
        """
        return self._started

    @started.setter
    def started(self, value):
        self._started = value

    @property
    def ended(self):
        """
        Get and set the end datetime of the session

        :rtype: datetime.datetime
        """
        return self._ended

    @ended.setter
    def ended(self, value):
        self._ended = value

    @property
    def messages_history(self):
        """
        Get and set the history of messages

        :rtype: list(BaseMessage)
        """
        return self._messages_history

    @messages_history.setter
    def messages_history(self, value):
        self._messages_history = value

    @property
    def project(self):
        """
        Get the session Project

        :rtype: Project
        """
        return self.setup.project

    @property
    def task(self):
        """
        Get the session Task

        :rtype: Task
        """
        return self.setup.task

    @property
    def is_running(self):
        return self.status == self.STATUS_SESSION_RUNNING
